#!python3
import re, os, pyperclip, shutil


def parsePaths():
    pathsStr = pyperclip.paste()
    if pathsStr == "":
        print("Clipboard is empty")
    paths = pathsStr.splitlines()
    paths = [path[1:-1] for path in paths]
    fileDir = os.path.dirname(paths[0])
    try:
        fileDir = os.path.dirname(paths[0])
    except IndexError:
        print("No paths in clipboard")
        return None
    if not os.path.isdir(fileDir):
        print("Paths in clipoard are invalid.")
        return None
    paths = sorted(paths)
    return paths


while True:
    print("Paste to clipboard subs pathes to rename.")
    input()
    subPaths = parsePaths()
    if subPaths == None:
        continue

    print(
        "Paste to clipboard video pathes.\nSubs will be renamed to videos in alphabetical order."
    )
    input()
    vidPaths = parsePaths()
    if vidPaths == None:
        continue

    if len(vidPaths) != len(subPaths):
        print("Different amount of subs and vids.")
        print("-" * 70)
        continue

    for n in range(len(subPaths)):
        shutil.move(
            subPaths[n],
            os.path.join(os.path.dirname(subPaths[n]), os.path.basename(vidPaths[n]))[
                :-3
            ]
            + subPaths[n][-3:],
        )
        # print(f"Sub path: {subPaths[n]}")
        # print(
        #     f"Vid path: {os.path.join(os.path.dirname(subPaths[n]), os.path.basename(vidPaths[n]))[:-3] + subPaths[n][-3:]}"
        # )

    print("Renamed.")
    print("-" * 70)
