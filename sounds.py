#!/usr/bin/env python3

# Author: https://github.com/Tomiwa-Ot
# Description: Download shows from BBC Sounds
# License: GPLv3 (see LICENSE.txt)

from future import print_function
from colorama import Fore
import subprocess
import platform
import requests
import argparse
import shutil

URL = ""
ID =  ""
FILE_META_DATA = {}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  \
            "AppleWebKit/537.36 (KHTML, like Gecko)" \
            "Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
HEADERS = {
    "User-Agent" : USER_AGENT,
    "Accept-Encoding" : "gzip,deflate"
}

def parse_args():
    parser = argparse.ArgumentParser(
        prog="iplayer",
        description="Description: downloads radio programmes from BBC Sounds",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--url", type=str, required=False,
        help="url of the programme"
    )
    parser.add_argument(
        "--id", type=str, required=False,
        help="id of the programme"
    )
    args = parser.parse_args()
    if args.url is not None and args.id is not None:
        print("[+] Specify either --url or --id")
        exit(1)
    if args.url is None and args.id is None:
        print("[+] Specify either --url or --id")
        exit(1)
    if args.url is not None and args.id is None:
        URL = args.url
    if args.id is not None and args.url is None:
        ID = args.id


def get_audio_meta_data():
    req = "https://bbc.co.uk/programmes/"
    if URL is not None:
        ID = URL.split("/")[-1]
        req = f"{req}{ID}.json"
    else:
        req = f"{req}{ID}.json"
    # check if request fails
    resp = requests.get(req, headers=HEADERS)
    FILE_META_DATA = resp.json
    req = f"https://open.live.bbc.co.uk/mediaselector/6/version/2.0/mediaset/pc/vpid/{FILE_META_DATA['versions'][0]['pid']}"
    resp = requests.get(req, headers=HEADERS)
    FILE_META_DATA.update(resp.json)


def download_thumbnail():
    print("[+] Downloading thumbnail ...")
    req = f"https:{FILE_META_DATA['holdingImage']}"
    resp = requests.get(req, headers=HEADERS, stream=True)
    with open(f"iplayer/{ID}.{FILE_META_DATA['holdingImage'].split('.')[-1]}", "wb") as f:
        shutil.copyfileobj(resp.raw, f)
        print(Fore.GREEN + f"[+] Thumbnail saved {ID}.{FILE_META_DATA['holdingImage'].split('.')[-1]}")


def download_file(mpd_link):
    # option of best and worse
    cmd = f"streamlink {mpd_link} -o {FILE_META_DATA['']}.m4a"
    print(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
    print(Fore.GREEN + "[+] Download complete")


def is_streamlink_installed():
    if platform.system() == "Windows":
        if b"'ffmpeg' is not recognized as an internal or external command" in subprocess.Popen(
            "streamlink", shell=True, stderr=subprocess.PIPE).stderr.read():
            print(Fore.RED + "[!] ffmpeg is not installed")
            exit(1)
    else:
        if b"ffmpeg: not found" in subprocess.Popen(
            "ffmpeg", shell=True, stderr=subprocess.PIPE).stderr.read():
            print(Fore.RED + "[!] ffmpeg is not installed")
            exit(1)


def main():
    parse_args()
    is_streamkink_installed()
    get_audio_meta_data()
    download_file()


if __name__ == "__main__":
    main()
