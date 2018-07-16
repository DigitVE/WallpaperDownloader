from urllib.request import Request, urlopen
from html.parser import HTMLParser
from subprocess import call
import argparse
import requests
import shutil
import sys

class WallpaperDownloader(HTMLParser):


    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.is_wallpaper_downloaded = False
        self.is_wallpaper_set = False

        super().__init__(*args, **kwargs)

        self.feed(self.read_content(self.url))


    def handle_starttag(self, tag, attrs):
        if (tag == "a" and attrs[0][1] == "preview" and not self.is_wallpaper_downloaded):
            self.is_wallpaper_downloaded = True
            print('Start grabbing HTML from:', attrs[1][1])
            self.feed(self.read_content(attrs[1][1]))
        if (tag == "img" and attrs[0][1] == "wallpaper" and not self.is_wallpaper_set):
            self.is_wallpaper_set = True
            r = requests.get('https:'+attrs[1][1], stream=True, headers={'User-agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(attrs[1][1][52:], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            call(["feh", "--bg-fill", attrs[1][1][52:]])
            print('Wallpaper has downloaded as:', attrs[1][1][52:])
            sys.exit(0)


    def read_content(self,url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return str(urlopen(req).read())


parser = argparse.ArgumentParser()
parser.add_argument("url", help="link to wallhaven category")
args = parser.parse_args()

parser = WallpaperDownloader(args.url)
