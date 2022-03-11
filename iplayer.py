#!/usr/bin/env python3

from future import print_function
import subprocess
import platform
import requests
import argparse

URL = ""
ID =  ""
MIME_TYPE = ""
FILE_META_DATA = {}

def parse_args():
    parser = argparse.ArgumentParser(
        prog="iplayer",
        description="",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--url", type=str, required=False,
        help="url of the content"
    )
    parser.add_argument(
        "--id", type=str, required=False,
        help="id of the content"
    )
    parser.add_argument(
        "--type", type=str, required=True,
        help="type of content (audio/video)"
    )
    args = parser.parse_args()
    if not args.type == "audio" or not args.type == "video":
        print("[+] Invalid MIME type")
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
    MIME_TYPE = args.type

def get_audio_meta_data():
    req = "https://bbc.co.uk/programmes/"
    if URL is not None:
        ID = URL.split("/")[-1]
        req = f"{req}{ID}.json"
    else:
        req = f"{req}{ID}.json"
    resp = requests.get(req)
    FILE_META_DATA = resp.json
    

def get_video_meta_data():
    pass

def download_thumbnail():
    if MIME_TYPE == "audio":
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
        pass
    else:
        pass

def main():
    parse_args()
    if not is_ffmpeg_installed():
        print("[+] ffmpeg is not installed")
        exit(1)
    if MIME_TYPE == "audio":
        get_audio_meta_data()
    else:
        get_video_meta_data()

if __name__ == "__main__":
    main()