#!/usr/bin/env python3

# Author: https://github.com/Tomiwa-Ot
# Description: Download shows from BBC Sounds
# License: GPLv3 (see LICENSE.txt)

from __future__ import print_function
from colorama import Fore
import subprocess
import platform
import requests
import argparse
import shutil

url = ""
id =  ""
quality = ""
file_meta_data = []

HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept-Encoding" : "gzip,deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "max-age=0"
}

def parse_args():
    global url, id, quality
    parser = argparse.ArgumentParser(
        prog="BBC Sounds",
        description="Description: downloads radio programmes from BBC Sounds",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-u", "--url", type=str, required=False,
        help="url of the programme"
    )
    parser.add_argument(
        "-i", "--id", type=str, required=False,
        help="id of the programme"
    )
    parser.add_argument(
        "-q", "--quality", type=str, required=True,
        help="quality of the download"
    )
    args = parser.parse_args()
    if args.quality is None: 
        print("[+] Specify quality --quality (worst/best)")
        exit(1)
    if not (args.quality == "worst" or args.quality == "best"):
        print(Fore.RED + "[!] Invalid quality")
        exit(1)
    quality = args.quality
    if args.url is not None and args.id is not None:
        print("[+] Specify either --url or --id")
        exit(1)
    if args.url is None and args.id is None:
        print("[+] Specify either --url or --id")
        exit(1)
    if args.url is not None and args.id is None:
        url = args.url
    if args.id is not None and args.url is None:
        id = args.id


def get_audio_meta_data():
    global url, id, quality, file_meta_data
    if len(url) > 1:
        id = url.split("/")[-1]
    req_urls = [
        f"https://bbc.co.uk/programmes/{id}.json",
        f"https://www.bbc.co.uk/programmes/{id}/playlist.json",
    ]
    for url in req_urls:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(Fore.RED + f"[!] GET request to {resp.url} failed: {resp.status_code}")
            exit(1)
        file_meta_data.append(resp.json())
    req = f"https://open.live.bbc.co.uk/mediaselector/6/version/2.0/mediaset/pc/vpid/{file_meta_data[0]['programme']['versions'][0]['pid']}"
    resp = requests.get(req, headers=HEADERS)
    # if resp.status_code != 200:
    #     print(Fore.RED + f"[!] GET request to {resp.url} failed: {resp.status_code}")
    #     exit(1)
    # file_meta_data.append(resp.json())
    


def download_thumbnail():
    global id, file_meta_data
    print("[+] Downloading thumbnail ...")
    req = f"https:{file_meta_data[1]['holdingImage']}"
    resp = requests.get(req, headers=HEADERS, stream=True)
    with open(f"{id}.{file_meta_data[1]['holdingImage'].split('.')[-1]}", "wb") as f:
        shutil.copyfileobj(resp.raw, f)
        print(Fore.GREEN + f"[+] Thumbnail saved {id}.{file_meta_data[1]['holdingImage'].split('.')[-1]}")


def download_file(mpd_link):
    global quality, file_meta_data
    cmd = f"streamlink {mpd_link} {quality} -o {file_meta_data[0]['title']}.m4a"
    print(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
    print(Fore.GREEN + "[+] Download complete")


def is_streamlink_installed():
    if platform.system() == "Windows":
        if b"'streamlink' is not recognized as an internal or external command" in subprocess.Popen(
            "streamlink", shell=True, stderr=subprocess.PIPE).stderr.read():
            print(Fore.RED + "[!] streamlink is not installed")
            exit(1)
    else:
        if b"streamlink: not found" in subprocess.Popen(
            "streamlink", shell=True, stderr=subprocess.PIPE).stderr.read():
            print(Fore.RED + "[!] streamlink is not installed")
            exit(1)


def main():
    parse_args()
    is_streamlink_installed()
    get_audio_meta_data()
    download_thumbnail()
    download_file()


if __name__ == "__main__":
    main()
