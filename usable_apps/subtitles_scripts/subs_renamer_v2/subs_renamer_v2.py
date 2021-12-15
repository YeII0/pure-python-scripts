import os, re, shutil

def advRename(path):
    while True:
        print('Which number occurence is episode number in subs?')
        subNumOccurrence = input()
        print('Which number occurence is episode number in videos?')
        vidNumOccurrence = input()
        if subNumOccurrence.isdigit() and vidNumOccurrence.isdigit():
            subNumOccurrence = int(subNumOccurrence)
            vidNumOccurrence = int(vidNumOccurrence)
            break
        print('Wrong input. Occurrences should be a numbers.')
        
    regex = re.compile(r'\d{1,4}')
    subNamesNr = {}
    vidNamesNr = {}
    
    for fileName in os.listdir(path):
        if fileName.endswith('.ass') or fileName.endswith('.srt'):
            subNumbers = regex.findall(fileName)
            if len(subNumbers) < subNumOccurrence:
                print('Amount of number occurrences in vids or subs files is lower than specified.')
                return False
            else:
                subNamesNr[subNumbers[subNumOccurrence - 1]] = fileName
        if fileName.endswith('.mkv') or fileName.endswith('.mp4'):
            vidNumbers = regex.findall(fileName)
            if len(vidNumbers) < vidNumOccurrence:
                print('Amount of number occurrences in vids or sub files is lower than specified.')
                return False
            else:
                vidNamesNr[vidNumbers[vidNumOccurrence - 1]] = fileName
                
    for k, v in subNamesNr.items():
        if k in vidNamesNr:
            shutil.move(v, vidNamesNr[k][:len(vidNamesNr[k]) - 4] + v[len(v) - 4:len(v)])

while True:
    print('Type path for subs to rename.')
    path = input()
    if os.path.isdir(path):
        break
    print('Invalid path.')
os.chdir(path)

while True:
    isDone = advRename(path)
    if isDone != False:
        break


