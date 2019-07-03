import os
dirs = r"D:\test_project\amtproject\testcase"

for root ,dirs, files in os.walk(dirs):
    print('root:%s'%root)
    print(dirs)
    print(files)

