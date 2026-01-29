import os
import re
import json
import time
import threading
from datetime import datetime
from queue import Queue
import ctypes
from ctypes import wintypes

class FileInfo:
    def __init__(self, Path, Name, Size, Extension, ModifyTime):
        self.Path = Path
        self.Name = Name
        self.Size = Size
        self.Extension = Extension
        self.ModifyTime = ModifyTime

class FileInfoEncoder(json.JSONEncoder):
    def default(self, Obj):
        if isinstance(Obj, FileInfo):
            return {
                "__type__": "FileInfo",
                "Path": Obj.Path,
                "Name": Obj.Name,
                "Size": Obj.Size,
                "Extension": Obj.Extension,
                "ModifyTime": Obj.ModifyTime
            }
        return super().default(Obj)

def FileInfoDecoder(Dct):
    if "__type__" in Dct and Dct["__type__"] == "FileInfo":
        return FileInfo(Dct["Path"], Dct["Name"], Dct["Size"], Dct["Extension"], Dct["ModifyTime"])
    return Dct

def GetLogicalDrives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    letter = ord('A')
    while bitmask > 0:
        if bitmask & 1:
            drives.append(f"{chr(letter)}:\\")
        bitmask >>= 1
        letter += 1
    return drives

def GetSubdirectories(Path):
    subdirs = []
    try:
        with os.scandir(Path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    subdirs.append(entry.path)
    except:
        pass
    return subdirs

class DiskIndexer:
    def __init__(self, Drive):
        self.Drive = Drive
        self.IndexData = []
        self.ProcessedFiles = 0
        self.TotalFiles = 0
        self.DiscoveredFiles = []
        self.IsRunning = False
        self.IsPaused = False
        self.IsDiscovering = False
        self.Threads = []
        self.Queue = Queue()
        self.DirQueue = Queue()
        self.ProgressCallback = None
        self.FileCallback = None
        self.BatchSize = 100
        self.ProgressUpdateInterval = 500
        self.LastProgressUpdate = 0
        self.Lock = threading.Lock()
        self.ShouldStop = False
        self.DiscoveryComplete = False
        self.CompletionCheckThread = None
        self.DiscoveryProgressCallback = None

    def Start(self, ThreadCount=4, DiscoveryThreads=4):
        if self.IsRunning: return
        self.IsRunning = True
        self.IsPaused = False
        self.ShouldStop = False
        self.DiscoveryComplete = False
        self.LastProgressUpdate = 0
        
        self._DiscoverFiles(DiscoveryThreads)
        
        print("正在快速统计文件总数...")
        while self.IsDiscovering and not self.ShouldStop:
            time.sleep(0.5)
            with self.Lock:
                if self.DiscoveryProgressCallback and self.TotalFiles > 0:
                    self.DiscoveryProgressCallback(self.TotalFiles)
        
        if self.ShouldStop: return
        print(f"文件总数统计完成: {self.TotalFiles}个文件")
        
        self._StartCompletionChecker()
        for _ in range(ThreadCount):
            Thread = threading.Thread(target=self._ProcessQueue)
            Thread.daemon = True
            Thread.start()
            self.Threads.append(Thread)

    def Pause(self):
        self.IsPaused = True

    def Resume(self):
        self.IsPaused = False

    def Stop(self):
        self.ShouldStop = True
        self.IsRunning = False
        self.IsPaused = False
        self.IsDiscovering = False
        if self.CompletionCheckThread and self.CompletionCheckThread.is_alive():
            self.CompletionCheckThread.join()

    def ExportIndex(self, FilePath):
        with open(FilePath, 'w') as F:
            json.dump(self.IndexData, F, cls=FileInfoEncoder)

    def ImportIndex(self, FilePath):
        with open(FilePath, 'r') as F:
            self.IndexData = json.load(F, object_hook=FileInfoDecoder)
        self.ProcessedFiles = len(self.IndexData)

    def CompareWith(self, OtherIndexer):
        CurrentPaths = {F.Path for F in self.IndexData}
        OtherPaths = {F.Path for F in OtherIndexer.IndexData}
        Added = CurrentPaths - OtherPaths
        Removed = OtherPaths - CurrentPaths
        return {"Added": list(Added), "Removed": list(Removed)}

    def Filter(self, MinSize=None, MaxSize=None, NamePattern=None, ExtPattern=None, MinModifyTime=None, MaxModifyTime=None):
        Result = []
        for File in self.IndexData:
            if MinSize is not None and File.Size < MinSize: continue
            if MaxSize is not None and File.Size > MaxSize: continue
            if NamePattern and not re.search(NamePattern, File.Name): continue
            if ExtPattern:
                Ext = File.Extension.lower() if File.Extension else ''
                if not re.search(ExtPattern, Ext, re.IGNORECASE): continue
            if MinModifyTime and File.ModifyTime < MinModifyTime: continue
            if MaxModifyTime and File.ModifyTime > MaxModifyTime: continue
            Result.append(File)
        return Result

    def _DiscoverFiles(self, ThreadCount):
        self.IsDiscovering = True
        self.DiscoveredFiles = []
        self.DirQueue.put(self.Drive)
        
        def ProcessDirs():
            while not self.ShouldStop and (not self.DirQueue.empty() or self.IsDiscovering):
                try:
                    DirPath = self.DirQueue.get(timeout=1)
                    if not DirPath or not os.path.isdir(DirPath):
                        self.DirQueue.task_done()
                        continue
                    
                    fileCount = 0
                    try:
                        with os.scandir(DirPath) as entries:
                            for entry in entries:
                                if self.ShouldStop: break
                                if entry.is_file(follow_symlinks=False):
                                    fileCount += 1
                                    self.DiscoveredFiles.append(entry.path)
                    except:
                        pass
                    
                    with self.Lock:
                        self.TotalFiles += fileCount
                    
                    subdirs = GetSubdirectories(DirPath)
                    for subdir in subdirs:
                        if self.ShouldStop: break
                        self.DirQueue.put(subdir)
                    
                    self.DirQueue.task_done()
                except:
                    if self.ShouldStop: break
        
        for _ in range(ThreadCount):
            Thread = threading.Thread(target=ProcessDirs, daemon=True)
            Thread.start()
        
        def MonitorDiscovery():
            self.DirQueue.join()
            with self.Lock:
                self.DiscoveryComplete = True
                self.IsDiscovering = False
            for path in self.DiscoveredFiles:
                self.Queue.put(path)
        
        threading.Thread(target=MonitorDiscovery, daemon=True).start()

    def _StartCompletionChecker(self):
        def CheckCompletion():
            while not self.ShouldStop and self.IsRunning:
                time.sleep(1)
                with self.Lock:
                    if self.DiscoveryComplete and self.Queue.empty() and self.ProcessedFiles >= self.TotalFiles:
                        self.IsRunning = False
                        break
        self.CompletionCheckThread = threading.Thread(target=CheckCompletion, daemon=True)
        self.CompletionCheckThread.start()

    def _ProcessQueue(self):
        while not self.ShouldStop:
            while self.IsPaused and not self.ShouldStop: time.sleep(0.1)
            try:
                FilePath = self.Queue.get(timeout=1)
                self._ProcessFile(FilePath)
                self.Queue.task_done()
                with self.Lock:
                    self.ProcessedFiles += 1
                    if (self.ProgressCallback and self.TotalFiles > 0 and 
                        (self.ProcessedFiles - self.LastProgressUpdate >= self.ProgressUpdateInterval or 
                         self.ProcessedFiles == self.TotalFiles)):
                        Progress = (self.ProcessedFiles / self.TotalFiles) * 100
                        self.ProgressCallback(Progress, self.ProcessedFiles, self.TotalFiles)
                        self.LastProgressUpdate = self.ProcessedFiles
                    if self.FileCallback and self.ProcessedFiles % self.BatchSize == 0:
                        self.FileCallback(self.ProcessedFiles, self.TotalFiles)
            except: pass

    def _ProcessFile(self, FilePath):
        try:
            Stat = os.stat(FilePath)
            Size = Stat.st_size
            ModifyTime = datetime.fromtimestamp(Stat.st_mtime).isoformat()
            Name = os.path.basename(FilePath)
            Ext = os.path.splitext(Name)[1][1:].lower() if '.' in Name else ''
            File = FileInfo(FilePath, Name, Size, Ext, ModifyTime)
            with self.Lock:
                self.IndexData.append(File)
        except: pass

def ProgressHandler(Progress, Processed, Total):
    print(f"索引进度: {Progress:.2f}% ({Processed}/{Total}个文件)")

def FileCountHandler(Count, Total):
    print(f"已索引文件: {Count}/{Total}个")

def DiscoveryProgressHandler(Count):
    print(f"已发现文件: {Count}个", end='\r')

if __name__ == "__main__":
    Indexer = DiskIndexer("C:\\")
    Indexer.ProgressCallback = ProgressHandler
    Indexer.FileCallback = FileCountHandler
    Indexer.DiscoveryProgressCallback = DiscoveryProgressHandler
    Indexer.BatchSize = 5000
    Indexer.ProgressUpdateInterval = 1000
    
    Indexer.Start(ThreadCount=8, DiscoveryThreads=8)
    
    try:
        while Indexer.IsRunning:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n用户中断，暂停操作")
        Indexer.Pause()
        Save = input("是否保存当前索引? (y/n): ")
        if Save.lower() == 'y':
            Indexer.ExportIndex("c_drive_index.json")
            print("索引已保存")
        Resume = input("是否继续索引? (y/n): ")
        if Resume.lower() == 'y':
            print("继续索引...")
            Indexer.Resume()
            while Indexer.IsRunning: time.sleep(1)
    
    Indexer.Stop()
    print(f"索引完成，共处理{Indexer.ProcessedFiles}/{Indexer.TotalFiles}个文件")
    Filtered = Indexer.Filter(MinSize=1024*1024, ExtPattern=r'^(docx|pdf)$')
    print(f"大于1MB的DOCX和PDF文件共{len(Filtered)}个")
    Indexer.ExportIndex("c_drive_final_index.json")
    print("最终索引已导出")
