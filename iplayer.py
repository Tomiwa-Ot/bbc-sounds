#!/usr/bin/env python3

from future import print_function
import subprocess
import platform
import requests
import argparse

URL = ""
ID =  ""
PROG_TYPE = ""
FILE_META_DATA = {}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"

def parse_args():
    parser = argparse.ArgumentParser(
        prog="iplayer",
        description="",
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
    parser.add_argument(
        "--type", type=str, required=True,
        help="type of programme (audio/video)"
    )
    args = parser.parse_args()
    if not args.type == "audio" or not args.type == "video":
        print("[+] Invalid programme type")
        exit(1)
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
    PROG_TYPE = args.type

def get_audio_meta_data():
    req = "https://bbc.co.uk/programmes/"
    if URL is not None:
        ID = URL.split("/")[-1]
        req = f"{req}{ID}.json"
    else:
        req = f"{req}{ID}.json"
    resp = requests.get(req)
    FILE_META_DATA = resp.json
    req = f"https://open.live.bbc.co.uk/mediaselector/6/version/2.0/mediaset/pc/vpid/{FILE_META_DATA['versions'][0]['pid']}"
    resp = requests.get(req)
    FILE_META_DATA.update(resp.json)

def get_video_meta_data():
    pass

def download_thumbnail():
    if PROG_TYPE == "audio":
        req = f"https:{FILE_META_DATA['holdingImage']}"
        resp = requests.get(req)
        with open(f"iplayer/{ID}.{FILE_META_DATA['holdingImage'].split('.')[-1]}", "rb") as f:
            f.write(resp._content)
            f.close()
    else:
        pass

def download_file(mpd_link):
    pass

def is_ffmpeg_installed():
    if platform.system() == "Windows":
        if b"'ffmpeg' is not recognized as an internal or external command" in subprocess.Popen(
            "ffmpeg", shell=True, stderr=subprocess.PIPE).stderr.read():
            print("[+] ffmpeg is not installed")
            exit(1)
    else:
        if b"ffmpeg: not found" in subprocess.Popen(
            "ffmpeg", shell=True, stderr=subprocess.PIPE).stderr.read():
            print("[+] ffmpeg is not installed")
            exit(1)

def main():
    parse_args()
    is_ffmpeg_installed()
    if PROG_TYPE == "audio":
        get_audio_meta_data()
    else:
        get_video_meta_data()
    download_file()

if __name__ == "__main__":
    main()