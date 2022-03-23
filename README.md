## BBC Sounds
Download audio programmes from BBC sounds

### Setup
- Install [streamlink](https://streamlink.github.io/install.html)
- Install dependencies
```console
pip install -r requirements.txt
```
### Usage
Specify either ID or URL of the programme
```console
user@pc:~$ python sounds.py
usage: BBC Sounds [-h] [-u URL] [-i ID] -q QUALITY

Description: downloads radio programmes from BBC Sounds

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url of the programme
  -i ID, --id ID        id of the programme
  -q QUALITY, --quality QUALITY
                        quality of the download 
```
