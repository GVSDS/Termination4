import os

def ReadFileRangeFromEnd(FilePath, StartLineFromEnd, EndLineFromEnd, BufferSize=1024 * 10, ReturnType=str):
    if StartLineFromEnd < 1 or EndLineFromEnd < 1:
        raise ValueError("Line number must be greater than 0")
    if StartLineFromEnd > EndLineFromEnd:
        raise ValueError("StartLineFromEnd must be less than or equal to EndLineFromEnd")
    LineCount = EndLineFromEnd
    BufferSize = BufferSize * LineCount
    with open(FilePath, 'rb') as FileObj:
        FileObj.seek(0, 2)
        FileSize = FileObj.tell()
        BufferSize = min(BufferSize, FileSize)
        Lines = []
        CurrentPosition = FileSize
        FoundLines = 0
        while CurrentPosition > 0 and FoundLines < LineCount:
            ReadPosition = max(0, CurrentPosition - BufferSize)
            ChunkSize = CurrentPosition - ReadPosition
            FileObj.seek(ReadPosition)
            Chunk = FileObj.read(ChunkSize)
            ChunkLines = Chunk.splitlines()
            ChunkLines = ChunkLines[::-1]
            for Line in ChunkLines:
                if FoundLines < LineCount:
                    Lines.append(Line)
                    FoundLines += 1
                else:
                    break
            CurrentPosition = ReadPosition
        Lines = Lines[::-1]
        StartIndex = max(0, len(Lines) - EndLineFromEnd)
        EndIndex = len(Lines) - StartLineFromEnd + 1
        ResultLines = Lines[StartIndex:EndIndex]
        R = [Line.decode('utf-8', errors='ignore') for Line in ResultLines]
        if ReturnType == str: return '\n'.join(R)
        elif ReturnType == list: return R
        else: raise ValueError("Return Type Error")
TempDir = os.getenv("temp")
LogFile = os.path.join(TempDir, "T.log")

ResultLines = ReadFileRangeFromEnd(LogFile, 1, 300)