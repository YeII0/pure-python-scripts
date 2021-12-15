#! python3
import os, re, operator
while True:
    print('Past path.')
    path = input()
    if os.path.isdir(path):
        break
    print('Wrong path')
os.chdir(path)

regexStyleName = re.compile(r'^Style: (.+?),')


allStylesOccurNumber = {}   # Dictionary with styles occurrences summed from every subs file.
dictOfStyleDicts = {}   # Dictionary for saving stylesOccurNumber dictionaries from every subs file.
                        # Key - file name, Value - dictionary which Key is style name and Value is
                        # number of style occurrences.

for fileName in os.listdir():
    if fileName.endswith('.ass'):
        stylesOccurNumber = {} # Dictionary with styles occurrences from one subs file.
        file = open(fileName, 'r', encoding='utf-8')

        # Loop for finding style names.
        for line in file.readlines():
            if regexStyleName.search(line) != None:
                style = regexStyleName.search(line).group(1)
                stylesOccurNumber[style] = 0
                # Adding styles from every subs files.
                if style not in allStylesOccurNumber:
                    allStylesOccurNumber[style] = [0, 0]
            elif line.startswith('[Events]'):
                break
        file.close()    

        # Loop for finding counting styles occurrences.
        file = open(fileName, 'r', encoding='utf-8')
        isStyleOccurInFile = False  # Boolean for checking if style occur atleast once in current file.
        for line in file.readlines():
            for style in stylesOccurNumber:
                regexDialogueStyle = re.compile(
                    r'^Dialogue: \d{1,2},\d:\d\d:\d\d\.\d\d,\d:\d\d:\d\d\.\d\d,' + style + ',')
                if regexDialogueStyle.search(line) != None:
                    stylesOccurNumber[style] += 1
                    allStylesOccurNumber[style][0] += 1
        file.close()

        # Loop for counting number of files in which style appears atleast once.
        for style, occurs in stylesOccurNumber.items():
            if occurs > 0:
                allStylesOccurNumber[style][1] += 1

        # Adding dictionaries to list. Data will be printed at the end from this list.
        dictOfStyleDicts[fileName] = stylesOccurNumber

# rowMaxLength is used for print formatting.
rowMaxLength = [len(max((k for k in allStylesOccurNumber.keys()), key=len)),
                len(str(max(v[0] for v in allStylesOccurNumber.values()))),
                len(str(max(v[1] for v in allStylesOccurNumber.values())))]

if rowMaxLength[0] < len('Style'):
    rowMaxLength = len('Style')
if rowMaxLength[1] < len('Summed style'):
    rowMaxLength[1] = len('Summed style')
if rowMaxLength[2] < len('Num of files'):
    rowMaxLength[2] = len('Num of files')

# Printing summed styles occurences from every subs file.
lineLength = rowMaxLength[0] + rowMaxLength[1] + rowMaxLength[2] + 6
print('Summed occurrences from every subs file: \n')
print('-' * lineLength)
print('Style'.ljust(rowMaxLength[0]) + ' | ' + 'Summed style'.ljust(rowMaxLength[1])
      + ' | ' + 'Num of files'.ljust(rowMaxLength[2]))
print(''.ljust(rowMaxLength[0]) + ' | ' + 'occurs'.ljust(rowMaxLength[1])
      + ' | ' + 'with style'.ljust(rowMaxLength[2]))
print('-' * lineLength)

sortedAllStylesNumbs = sorted(allStylesOccurNumber.items(), key=operator.itemgetter(1), reverse=True)
for k, v in sortedAllStylesNumbs:
    print(k.ljust(rowMaxLength[0]) + ' | ' + str(v[0]).rjust(rowMaxLength[1]) + ' | '
          + str(v[1]).rjust(rowMaxLength[2]))
print('-' * lineLength)
print()

# Printing style occurrences from every file in order.
lineLength = rowMaxLength[0] + rowMaxLength[1] + 3
for fileName, stylesOccurNumber in dictOfStyleDicts.items(): 
    print(fileName + ':')
    print('-' * lineLength)
    print('Style'.ljust(rowMaxLength[0]) + ' | ' + 'Summed style'.ljust(rowMaxLength[1]))
    print('-' * lineLength)
    sortedStylesNumbs = sorted(stylesOccurNumber.items(), key=operator.itemgetter(1), reverse=True)
    for k, v in sortedStylesNumbs:
        print(k.ljust(rowMaxLength[0]) + ' | ' + str(v).rjust(rowMaxLength[1]))
    print('-' * lineLength)
    print()

print('Press any key to leave.')
input()

        
    
