#!python3
import os, re, pyperclip, sys

while True:
    print('Paste subs path.')
    path = input()
    if os.path.isdir(path):
        break
    print('Wrong path.')
os.chdir(path)

print('Styles will be pasted to program from clipboard. '
        + 'Every style to overwrite should be in new line. '
        + 'Press any key when you copy styles to clipboard.')
input()
clipboard = pyperclip.paste()
styleList = clipboard.split('\r\n')
styleNameRegex = re.compile(r'^Style: .+?,')
styleNames = []
for style in styleList:
    if styleNameRegex.search(style) != None:
        styleNames.append(styleNameRegex.search(style).group(0))
    else:
        print('There is no styles in clipboard or they are in wrong format.')
        print('Press any key to leave.')
        input()
        sys.exit()
        
# Function uses styList from the outside.
def replace(matchObj):
    for i in range(len(styleList)):
        if matchObj.group(0).startswith(styleNames[i]):
            return styleList[i]
    return matchObj.group(0)

styleLineRegex = re.compile(r'^Style: .+')

for fileName in os.listdir(path):
    if fileName.endswith('.ass'):
        file = open(fileName, 'r', encoding="utf-8")
        # fileLines contains all lines before '[Events]' line.
        fileLines = ''
        # secondPartLines contains lines after '[Events]' line. '[Events]' line included.
        secondPartLines = ''
        
        isLineEventsOccur = False
        for line in file.readlines():
            if isLineEventsOccur == False and line.startswith('[Events]'):
                isLineEventsOccur = True
            if isLineEventsOccur:
                secondPartLines += line
            else:
                fileLines += line
        file.close()
        fileLines = fileLines.split('\n')
        secondPartLines = secondPartLines.split('\n')
        
        for i in range(len(fileLines)):
            fileLines[i] = styleLineRegex.sub(replace, fileLines[i])
      
        # Opening file for overwriting with new update content.
        file = open(fileName, 'w', encoding="utf-8")
        file.write('\n'.join(fileLines))
        file.close()
        file = open(fileName, 'a', encoding="utf-8")
        file.write('\n'.join(secondPartLines))
        file.close()
