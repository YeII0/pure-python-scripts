 #! python3
import os
while True:
    print('Paste subs path.')
    path = input()
    if os.path.isdir(path):
        break
    print('Invalid path.')
os.chdir(path)

for fileName in os.listdir(path):
    if fileName.endswith('.ass'):
        print(fileName + ':')
        file = open(fileName, 'r', encoding='utf-8')
        
        for line in file.readlines():
            if line.startswith('PlayResX'):
                print(line[:len(line) - 1])
            elif line.startswith('PlayResY'):
                print(line[:len(line) - 1])
                break
            elif line.startswith('[Events]'):
                break
        file.close()
        print('-----------------------------------------------')
        print()
print('Press any key to leave.')
input()
