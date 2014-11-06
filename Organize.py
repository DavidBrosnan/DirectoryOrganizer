'''
Created on Jul 26, 2014

@author: David
'''

if __name__ == '__main__':
    pass

import os, shutil

'''
Takes a path name, e.g.:
Takes a single backslash and makes it into 2 backslashes to avoid escape character
C:\\Users
'''

def formatPath(path):
    newPath = ""
    for i in range(len(path)):
        newPath += path[i]
        if path[i] == "\\":
            newPath += "\\"
    return newPath


'''
Reads config file in local directory
#Foldername
filetype(s)
#Foldername
filetype(s)

Sets up a dictionary with foldernames that contain a list of file types
'''
def readSrc():
    with open("config.conf", "r") as inpFile:
        for line in inpFile:
            if line[0:4] == "src=":
                return line[4:].rstrip()

def readDst():
    with open("config.conf", "r") as inpFile:
        for line in inpFile:
            if line[0:4] == "dst=":
                return line[4:].rstrip()

def readFolders():
    
    folders = {}
    currFolder = ""
    with open("config.conf", "r") as inpFile:
        for line in inpFile: 
            if line[0] == "#":
                currFolder = line[1:].rstrip()
                folders[currFolder] = []
            else:
                if line != '\n' and line[0] == ".":
                    folders[currFolder].append(line.rstrip())
                    
    folders["Other"] = [".*"]    
    return folders
                     
'''
Makes directory if Picture, Docs, Exe, etc. doesn't already exist
'''

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def mkdirs(path, diction):
    print("Creating Folders in " + path + " .....")
    for folder in diction.keys():
        #print("DEBUGGING***: Creating: " + folder)
        if not os.path.exists(path + "\\" + folder):
            if not is_empty(diction[folder]):
                os.makedirs(path + "\\" + folder)
                        
def transferFiles(fileList, folderDict, src, dst):
    print("DEBUG: ***** Transfer Files")
    flag = 0
    ext = ""
    curExt = ""
    direc = ""
    for file in fileList:
        print("DEBUG: ***** FOR FILE: " + file)
        flag = 0
        ext = os.path.splitext(file)[1] #grab the extension of the file
        print ("DEBUG: EXT: " + ext)
        if ext == "":
            ext = ".file"
        if ext != curExt: #if the extension we have is not the one we're burning through
            curExt = ext #we have a new extension to go through
            for folder in folderDict.keys(): #For every folder
                if ext in folderDict[folder]:  #if an extension in the folder
                    direc = folder
                    print("DEBUG:******** Move from " + (os.path.join(src, file) + " to " + os.path.join(dst, direc)))
                    shutil.move(os.path.join(src, file), os.path.join(dst, direc))
                    flag = 1
                    
            if flag == 0:
                print("DEBUG:******** Move from " + (os.path.join(src, file) + " to " + os.path.join(dst, "Other")))
                shutil.move(os.path.join(src, file), os.path.join(dst, "Other"))
        else:
            print("DEBUG:****** direct: " + direc)
            print("DEBUG:******** Move from " + (os.path.join(src, file) + " to " + os.path.join(dst, direc)))
            shutil.move(os.path.join(src, file), os.path.join(dst, direc))
            
def cleanUpDir(folderDict, dst):
    
    for folder in folderDict.keys():
        if is_empty(os.listdir(os.path.join(dst, folder))):
            shutil.rmtree(os.path.join(dst, folder))

print ("Select option")
print("1. Read src and dst from file")
print("2. Input src and dst from keyboard")
choice = input()

if(choice == '1'):
    srcPath = readSrc()
    #srcPath = formatPath(srcPath)
    dstPath = readDst()
    #dstPath = formatPath(dstPath)

else:
    srcPath = input("What is the path of the directory you want organized?\n")
    #srcPath = formatPath(srcPath)   
    dstPath = input("What directory do you want it placed in? Leave blank for source folder?\n")
    if dstPath == "":
        dstPath = srcPath
   # else:
      #  dstPath = formatPath(dstPath)
    
subDir = os.listdir(srcPath)
subDir.sort(key=lambda f: os.path.splitext(f)[1])

#for file in subDir:
 #   print (file)
    
files = []
      
for file in subDir:
    if os.path.isfile(os.path.join(srcPath, file)):
        files.append(file)
        
folders = readFolders()
mkdirs(dstPath, folders)

print("DEBUGGING INFORMATION:")
for file in files:
    print (file,)

print("\n")

for folder in folders.keys():
    print (folder)
    
print(srcPath + "\n" + dstPath)

transferFiles(files, folders, srcPath, dstPath)
cleanUpDir(folders, dstPath)
