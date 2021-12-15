#! python3
import requests
import bs4
import os
import urllib
import re
import time
import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")
# logging.disable(logging.CRITICAL)


def dlSingleFile(formElem, cookies, dlPath, headers, rename):
    idValue = formElem.find(attrs={"type": "hidden", "name": "id"}).get("value")
    shValue = formElem.find(attrs={"type": "hidden", "name": "sh"}).get("value")
    singleFileValue = formElem.find(
        attrs={"type": "submit", "name": "single_file"}
    ).get("value")
    actionPath = formElem.get("action")
    siteUrl = "http://animesub.info"

    payload = {"id": idValue, "sh": shValue, "single_file": singleFileValue}
    while True:
        try:
            r = requests.post(
                urllib.parse.urljoin(siteUrl, actionPath),
                data=payload,
                headers=headers,
                cookies=dict(cookies),
            )
            r.raise_for_status
            break
        except Exception:
            print("Problem with downloading single file. Retry after 5 seconds.")
            time.sleep(5)
    try:
        filename = r.headers["Content-Disposition"][
            r.headers["Content-Disposition"].index("=") + 1 :
        ]
    except Exception:
        print("One file from the page not exist.")
        return
    # Changing in filename order from ep_author to author_ep or from startEp_endEp_author to author_startEp_endEp.
    # If there is now ep part, for example in movie, filename is not changed.
    if rename == True:
        filenameRe = re.compile(r"(.+?)(_ep\d+)(_\d+)?(_.+?)(_AnimeSubInfo_id\d+.zip)$")
        matchObj = filenameRe.search(filename)
        if matchObj != None:
            titlePart = matchObj.group(1)
            epStartPart = matchObj.group(2)
            epEndPart = matchObj.group(3)
            authorPart = matchObj.group(4)
            lastPart = matchObj.group(5)
            if epEndPart == None:
                filename = titlePart + authorPart + epStartPart + lastPart
            else:
                filename = titlePart + authorPart + epStartPart + epEndPart + lastPart

    subsZip = open(os.path.join(dlPath, filename), "wb")
    for chunk in r.iter_content(1000000):
        subsZip.write(chunk)
    subsZip.close()


def dlPage(url, dlPath, rename, page=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        + "(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

    if not url.startswith(
        "http://animesub.info/szukaj_old.php?"
    ) and not url.startswith("http://animesub.info/szukaj.php?"):
        print("Given url is wrong.")
        return None

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except Exception as err:
        print("Given url is not valid or not accesible.")
        logging.warning((str(err)))
        if page == None:
            print("Page not downloaded.")
        else:
            print(f"Page {page} not downloaded.")
        return None
    soup = bs4.BeautifulSoup(r.text, "lxml")

    formElems = soup.find_all(attrs={"method": "POST", "action": "sciagnij.php"})
    if formElems == []:
        print("There is no subs to download.")
        return None

    for formElem in formElems:
        dlSingleFile(formElem, dict(r.cookies), dlPath, headers, rename)
    if page == None:
        print("Downloaded.")
    else:
        print(f"Downloaded page: {page}.")

    return soup


def dlPages(url, endPage, dlPath, rename):
    regex = re.compile(".+?.php?")
    matchObj = regex.search(url)
    if matchObj == None:
        print("You should provide url to animesub search.")
        return
    searchMainUrl = matchObj.group(0)
    regex = re.compile(r"od=(\d+)$")
    if regex.search(url) == None:
        startPage = 1
    else:
        startPage = int(regex.search(url).group(1)) + 1
    if startPage >= endPage:
        print("End page should be greater than start page.")
        return
    nextPage = startPage
    while True:
        soup = dlPage(url, dlPath, rename, nextPage)
        if soup == None:
            return
        if nextPage == endPage:
            return
        nextArrowImg = soup.find(attrs={"src": "./pics/zolty/sp.gif"})
        if nextArrowImg == None:
            return
        nextPageElem = nextArrowImg.parent
        url = urllib.parse.urljoin(searchMainUrl, nextPageElem.get("href"))
        nextPage = int(regex.search(url).group(1)) + 1


while True:
    print("Paste path to download:")
    dlPath = input()
    if os.path.isdir(dlPath):
        break
    print("Invalid path.\n")

while True:
    print(
        "\nPaste url with subs to download. You can pass end page optional argument "
        + 'for download from few pages and "norename" argument for no not renaming files.'
    )
    strArguments = input()
    print()
    arguments = strArguments.split(";")
    endPage = None
    rename = True
    if len(arguments) == 1:
        url = arguments[0]
    elif len(arguments) == 2:
        if arguments[1] == "norename":
            rename = False
        else:
            url, endPage = arguments
            try:
                endPage = int(endPage)
            except Exception:
                print('Second argument should be a number or be equal to "norename".')
                continue
    elif len(arguments) == 3:
        url, endPage, rename = arguments
        try:
            endPage = int(endPage)
        except Exception:
            print("Second argument should be a number.")
            continue
        if rename == "norename":
            rename = False
        else:
            print("Third argument is wrong")
            continue
    else:
        print("Wrong number of arguments.")
        continue

    if endPage == None:
        dlPage(url, dlPath, rename)
    else:
        dlPages(url, endPage, dlPath, rename)

