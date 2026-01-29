import maker
import time

indexer = maker.DiskIndexer("C:")

a = time.time()
indexer.ImportIndex("c_drive_final_index.json")
print(time.time() - a)
a = time.time()
Filtered = indexer.Filter(ExtPattern=r'^(doc|docx|pdf|xlsx|xls)$')
print(time.time() - a)
print(f"大于1MB的TXT和PDF文件共{len(Filtered)}个")

i: maker.FileInfo
for i in Filtered:
    print(i.Path)

