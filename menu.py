import urllib.request
import json
import sys, os
import time
import datetime
from PIL import Image
from models import *


class Menu:
    def __init__(self, slug, tipe):
        url = 'https://api-g.weedmaps.com/wm/web/v1/listings/{}/menu?type={}'.format(slug, tipe)
        page = urllib.request.urlopen(url)
        # print(page.read())
        data = json.loads(page.read().decode('utf-8'))
        self.data = data
        self.categories = data['categories']
        self.items = []
        self.dispensary = Dispensary.get(slug=slug)

        for c in self.categories:
            for i in c['items']:
                # print(i)
                obj = {}
                obj['name'] = i['name']
                obj['category'] = i['category_name']
                obj['prices'] = i['prices']
                obj['url'] = i['image_url']
                self.items.append(obj)

    def todays_deal(self):
        return self.data['listing']['todays_deal']



# print(m.newMenuItems())












