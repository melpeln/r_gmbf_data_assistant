import requests
import urllib.request as ur
import time
import json
from datetime import datetime
from collections import Counter


download_dir = "img/"


def download_reddit(_url, _file_name):
    r = requests.get(_url)
    with open(download_dir + _file_name, "wb") as f:
        f.write(r.content)


def download_imgur(_url, _fpath):
    contents = ur.urlopen(_url)
    with open(download_dir + _fpath, 'wb') as f:
        f.write(contents.read())


def download_gallery_reddit(submission):
    gallery = []
    try:
        for i in submission.media_metadata.items():
            url = i[1]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            gallery.append(url)
            header = {'user-agent': 'python:img-downloader:0.1'}
    except AttributeError as ae:
        print(f'Error found with id {submission.id}!')
        print(ae)

    for i, img in enumerate(gallery):
        req = requests.get(img, headers=header)
        with open(download_dir + submission.id + '_' + str(i) + '.jpg', 'wb') as f:
            f.write(req.content)
            time.sleep(0.5)


class BFpost:

    def __init__(self, _submission, _title_info, _votes,) -> None:
        self.title = _submission.title
        self.url = _submission.url
        self.body_fat = _title_info.body_fat
        self.age = _title_info.age
        self.sex = _title_info.sex
        self.height = _title_info.height
        self.weight = _title_info.weight
        self.votes = Counter(_votes)
        self.info = _title_info
        self.id = _submission.id
        self.file_name = self.id + ".jpg"

        if "imgur" in self.url:
            download_imgur(self.url, self.file_name)
        elif "gallery" in self.url:
            download_gallery_reddit(_submission)
        else:
            download_reddit(self.url, self.file_name)
