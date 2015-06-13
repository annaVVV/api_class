__author__ = 'Mike'
import os

#C:\Documents and Settings\Mike\Desktop\Python_git\api_class\homework\createFile.py

def create_file_with_size(file_path, sizeKB):
    f = open(file_path, "wb")
    sizeS = 1073741824 * sizeKB # bytes in 1 KB
    f.write("\0" * 2048)#sizeS
    f.seek(0,2) # move the cursor to the end of the file
    print f.tell()
    print os.path.getsize(file_path)
    f.close()


create_file_with_size("C:\\sample", 1)