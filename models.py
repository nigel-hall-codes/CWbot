from peewee import *
import json
import urllib.request

db = SqliteDatabase("cheapweedsf.db")

class Dispensary(Model):
    name = TextField()
    slug = TextField()
    tipe = TextField(default="delivery")
    wmid = IntegerField()
    url = TextField()

    class Meta:
        database = db



def initialize():
    db.connect()
    db.create_tables([Dispensary])

initialize()


# Downloader functions

def download_dispensaries():
    url_two = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=doctors&filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=south-san-francisco&filter%5Bregion_slug%5Bdoctors%5D%5D=san-francisco&page_size=100&size=100'
    sf_url = 'https://api-g.weedmaps.com/wm/v2/listings?filter%5Bplural_types%5D%5B%5D=dispensaries&filter%5Bplural_types%5D%5B%5D=deliveries&filter%5Bregion_slug%5Bdeliveries%5D%5D=san-francisco&filter%5Bregion_slug%5Bdispensaries%5D%5D=san-francisco&page_size=100&size=100'
    dispensaries = json.loads(urllib.request.urlopen(url_two).read().decode('utf-8'))['data']['listings']
    for d in dispensaries:
        print(d)
        dispensary, create = Dispensary.get_or_create(name=d['name'], slug=d['slug'], url=d['web_url'], tipe=d['type'], wmid=d['wmid'])
        dispensary.save()

# download_dispensaries()
