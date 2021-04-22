#!/usr/bin/python

import sys
import os
import requests
import errno
from bs4 import BeautifulSoup

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def fillDownloadListWithObjects(list,URL):
    r= requests.get(URL+"/objects/")
    soup = BeautifulSoup(r.text,features="html.parser")

    for link in soup.findAll(["a"]):
        if link.get("href") == "" or link.get("href") == "../" or link.get("href") == "./" or link.get("href") == "info/" or link.get("href") == "info/" or link.get("href") == "pack":
            continue
        item = "objects/"+link.get("href")
        r2= requests.get(URL+"/"+item)
        soup2 = BeautifulSoup(r2.text,features="html.parser")
        for link2 in soup2.findAll(["a"]):
            if link2.get("href") == "" or link2.get("href") == "../" or link2.get("href") == "./":
                continue
            item2 = item+""+link2.get("href")
            list.append(item2)
    return list

# create PATH and fill file
def writeFile(filename,content):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "wb") as f:
        for chunk in content.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def __main__():
    if len(sys.argv) != 3:
        print("Usage : " + sys.argv[0]+" [src : URL] [dst : FOLDER]")
        exit()
    
    # important git queue

    downloadQueue = [
        "HEAD", 
        "objects/info/packs", 
        "description", 
        "config", 
        "COMMIT_EDITMSG", 
        "index", 
        "packed-refs", 
        "refs/heads/master", 
        "refs/remotes/origin/HEAD", 
        "refs/stash",
        "logs/HEAD", 
        "logs/refs/heads/master", 
        "logs/refs/remotes/origin/HEAD", 
        "info/refs", 
        "info/exclude", 
        "refs/wip/index/refs/heads/master", 
        "refs/wip/wtree/refs/heads/master"
    ]

    # fill with commit structure
    fillDownloadListWithObjects(downloadQueue,sys.argv[1])

    # download files
    for item in downloadQueue:
        res = requests.get(sys.argv[1]+"/"+item,stream=True)
        if res.status_code == 200:
            print(bcolors.OKGREEN+"[+] Downloaded :" +item +bcolors.ENDC)
            writeFile(sys.argv[2]+"/.git/"+item,res)
        else:
            print(bcolors.FAIL+"[-] Downloaded :" +item+bcolors.ENDC)
    
__main__()