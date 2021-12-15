#! python3
import os, re, shutil, sys

def findIteratorOccur(filesMatches):
    possibleIterators = []
    for j in range(len(filesMatches[0])):
        repeatsCount = 0
        numbers = []
        for i in range(len(filesMatches)):
            try:
                if filesMatches[i][j] in numbers:
                    repeatsCount += 1
                numbers.append(filesMatches[i][j])
            except IndexError:
                pass
        possibleIterators.append(repeatsCount)
        if repeatsCount == 0:
            break
    if min(possibleIterators) > 0:
        return -1
    iteratorOccur = possibleIterators.index(min(possibleIterators)) + 1
    return iteratorOccur

while True:
    print('Type path for subs to rename.')
    path = input()
    if os.path.isdir(path):
        break
    print('Invalid path.')
os.chdir(path)

regex = re.compile(r'\d{1,4}')
vidsMatches = []
subsMatches = []

for fileName in os.listdir(path):
    if fileName.endswith('.ass') or fileName.endswith('.srt'):
        subsMatches.append(regex.findall(fileName))
    if fileName.endswith('.mkv') or fileName.endswith('.mp4'):
        vidsMatches.append(regex.findall(fileName))

if len(vidsMatches) < 2 or len(subsMatches) < 2:
    print('You should have atleast two sub and video files to use program.\n'
          + 'Press any key to leave.')
    input()
    sys.exit()

# Finding subs iterator.
subsIteratorOccurr = findIteratorOccur(subsMatches)
# Finding videos iterator.
vidsIteratorOccurr = findIteratorOccur(vidsMatches)

if subsIteratorOccurr == -1 or vidsIteratorOccurr == -1:
    print('Wrong files in specified folder.\n'
        + 'Maybe there are doubled vids or subs from diffrent groups.\n'
        + 'Press any key to leave.')
    input()
    sys.exit()

subNamesNr = {}
vidNamesNr = {}

for fileName in os.listdir(path):
    if fileName.endswith('.ass') or fileName.endswith('.srt'):
        subMatches = regex.findall(fileName)
        try:
            subNamesNr[subMatches[subsIteratorOccurr - 1]] = fileName
        except IndexError:
            print('Wrong files in specified folder.\n'
                  + 'Maybe there are doubled vids or subs from diffrent groups.\n'
                  + 'Press any key to leave.')
            input()
            sys.exit()

    if fileName.endswith('.mkv') or fileName.endswith('.mp4'):
        vidMatches = regex.findall(fileName)
        try:
            vidNamesNr[vidMatches[vidsIteratorOccurr - 1]] = fileName
        except IndexError:
            print('Wrong files in specified folder.\n'
                  + 'Maybe there are doubled vids or subs from diffrent groups.\n'
                  + 'Press any key to leave.')
            input()
            sys.exit()
            
for k, v in subNamesNr.items():
    if k in vidNamesNr:
        shutil.move(v, vidNamesNr[k][:len(vidNamesNr[k]) - 4] + v[len(v) - 4:len(v)])
        
    
