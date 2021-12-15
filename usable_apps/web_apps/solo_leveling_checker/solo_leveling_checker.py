import re
import json
import requests
import bs4
import os
from os import path

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    + '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}


db_path = path.join(
    path.dirname(path.realpath(__file__)), "db.json")

with open(db_path) as json_f:
    json_db = json.load(json_f)

def pl_checker(headers, url, last_ch):

    r = requests.get(url, headers)
    pageSoup = bs4.BeautifulSoup(r.text, 'lxml')
    aElems = pageSoup.select('.chapter-title-rtl a')
    ch_num_link_dic = {}
    regex = re.compile(r'/(\d+$)')

    for aElem in reversed(aElems):
        link = aElem.get('href')
        matchObj = regex.search(link)

        if matchObj and matchObj.group(1) and int(matchObj.group(1)) > last_ch:
            chNum = int(matchObj.group(1))
            ch_num_link_dic[chNum] = link


    return ch_num_link_dic


def eng_checker(headers, url, last_ch):
    r = requests.get(url, headers)
    pageSoup = bs4.BeautifulSoup(r.text, 'lxml')
    aElems = pageSoup.select('.chap_tab a')
    ch_num_link_dic = {}
    regex = re.compile(r'-(\d+)/$')
    for aElem in reversed(aElems):
        link = aElem.get('href')
        matchObj = regex.search(link)

        if matchObj and matchObj.group(1) and int(matchObj.group(1)) > last_ch:
            chNum = int(matchObj.group(1))
            ch_num_link_dic[chNum] = link

    return ch_num_link_dic


def send(chapters, site_name, title, embedColor, webhook):
    if chapters == {}:
        return {}
    embeds = []
    for ch_num, url in chapters.items():
        embed = {
                "author": {'name': site_name},
                "title": title + " ep" + str(ch_num),
                "color": embedColor,
                "url": url
        }
        embeds.append(embed)

    # Split embeds list when is higher than 10, cuz 10 embeds is max limit for webhooks.
    sendedEmbeds = 0
    badRequest = False
    if len(embeds) > 10:
        loopTimes = len(embeds) // 10
        endRange = loopTimes * 10
        for i in range(0, endRange, 10):
            payload = {"embeds": embeds[i: i + 10]}
            try:
                r = requests.post(webhook, json=payload)
                r.raise_for_status()
            except Exception as err:
                print(err)
                badRequest = True
                break
            sendedEmbeds += 10

        # Sending rest of embeds. Required only when embeds divided by 10 is not equal to zero.
        if badRequest is False:
            remainsNumber = len(embeds) % 10
            if remainsNumber != 0:
                startRange = (len(embeds) // 10) * 10
                payload = {"embeds": embeds[startRange:]}
                try:
                    r = requests.post(webhook, json=payload)
                    r.raise_for_status()
                except Exception as err:
                    print(err)
                    badRequest = True
                if badRequest is False:
                    sendedEmbeds += remainsNumber
        # Creating dictionary with sended content from full dictionary when bad request occurs .
        if sendedEmbeds == 0:
            return {}
        if badRequest is True:
            elemCount = 0
            sended_ch = {}

            for ch_num, url in chapters.items():
                sended_ch[ch_num] = url
                elemCount += 1
                if elemCount == sendedEmbeds:
                    break

            return sended_ch

    else:
        payload = {"embeds": embeds}
        try:
            r = requests.post(webhook, json=payload)
            r.raise_for_status()
        except Exception as err:
            print(err)
            return {}

    return chapters


def updateDb(json_db, module_index, sended_ch):
    if sended_ch == {}:
        return
    maxChap = 0

    db_path = path.join(path.dirname(path.realpath(__file__)), "db.json")
    with open(db_path, 'w') as json_f:
        for ch_num in sended_ch:
            if ch_num > maxChap:
                maxChap = ch_num
        json_db[module_index]['last_ch'] = maxChap
        json.dump(json_db, json_f)


webhook = os.environ.get('SOLO_LEVELING_WEBHOOK')

# PL
chapters = pl_checker(headers, json_db[0]['url'], json_db[0]['last_ch'])
sended_ch = send(chapters, json_db[0]['site_name'], json_db[0]['title'], json_db[0]['embed_color'], webhook)
updateDb(json_db, 0, sended_ch)

# ENG
chapters = eng_checker(headers, json_db[1]['url'], json_db[1]['last_ch'])
sended_ch = send(chapters, json_db[1]['site_name'], json_db[1]['title'], json_db[1]['embed_color'], webhook)
updateDb(json_db, 1, sended_ch)