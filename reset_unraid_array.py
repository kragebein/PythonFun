#!/usr/bin/python3
''' Deletes all content from unraid arrays, restores empty folder structure '''
import os, sys, string, math, traceback, json
dumpfile='/tmp/arraydump.json'

paths = ['/drive/drive/Archives/', '/drive/drive/ISOs/']
ext = ['cache', 'cache']
struct = []
total_size = 0
def size(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += size(itempath)
    return total_size
def resetarray(): 
    if not len(struct) >= 1:
        print(f'Folder structure is Empty.. Load {dumpfile} instead.')
        sys.exit(1)
    for x in struct:
        print('Removing {x}...')
        os.remove(x)
        os.makedirs(x)
        print('done.. structure restored')
folders = [i for i in string.ascii_uppercase]
folders.append('0-9')
for index, path in enumerate(paths):
    for folder in folders:
        fullpath = path+folder + '/'
        if not os.path.exists(fullpath):
            break
        items = os.listdir(fullpath)
        if len(items) >= 1:
            for x in items:
                if os.path.isdir(fullpath+x):
                    struct.append(fullpath+x)
            this_size = math.ceil(size(fullpath)/1024/1024/1024)
            total_size += this_size
            print(f'({ext[index]}) {fullpath} contains {len(items)} items - ({this_size} GB)')
with open(dumpfile, 'w') as brrt:
    brrt.write(json.dumps(struct))
    brrt.close()
print(f'Total size is {total_size/1024} TB')
print(f'Total subfolders: {len(struct)}')
if input('Do you want to reset the structure ? [Y/N] ').lower() in ['y','j']:
    resetarray()
else:
    print('Aborting.')