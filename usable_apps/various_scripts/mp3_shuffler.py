#! python3
# mp3shuffler: random numbering files in program dir by adding
# number as a prefix with format "Number. ".
# If files in directory are already numbered with format "Number. "
# numbers will be randomly renumbered.
# Usages: for example good for old mp3 devices without shuffle option.
# You can just reorder file sorting by adding numbering as a prefix to files with this program.
import shutil, sys, re, random, os

print('You can delete numbering, add or shuffle existing numbering to mp3\'s.')
print('Type 1 if you want add numbering or shuffle existing one.')
print('Type 2 if you want delete numbering from mp3\'s.')
userChoice = input()

if userChoice != '1' and userChoice != '2':
    print('Wrong input.')
    sys.exit()

regex = re.compile(r'^\d+\. ((.*?)(\.mp3|\.flac))$')

mp3Number = 0
# Deleting numbering from all files in program directory.
for filename in os.listdir('.'):
        newFilename = regex.sub(r'\1', filename)
        shutil.move(filename, newFilename)
        if filename.endswith('.mp3') or filename.endswith('.flac'):
            mp3Number += 1
            
# If user choosed  option '2' program ends here, cuz job is already done.          
if userChoice == '2':
    sys.exit()
           
# List of numbers.
numbersList = []
for i in range(mp3Number):
    numbersList.append(i)

# Shuffling list.
random.shuffle(numbersList)

# Adding prefix to files from numbersList.
i = -1
for filename in os.listdir('.'):
    i += 1
    if filename.endswith('.mp3') or filename.endswith('.flac'):
        shutil.move(filename, str(numbersList[i]) + '. ' + filename)
    


