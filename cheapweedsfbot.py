from models import *
from instabot import Bot
import random
from menu import Menu
from PIL import Image
import urllib.request
import os
import trim
import schedule
import time
import post
import trending


class CheapWeedBot:
    def __init__(self):
        self.caption = "nothing"
        self.post_dir = 'postsToBeUploaded/'


    def dispensary(self):
        dispensary = Dispensary.get(name="Proven SF")
        return dispensary

    def random_dispensary(self):
        dispensaries = Dispensary.select()
        selection = random.randint(1, len(dispensaries)-1)
        return dispensaries[selection]
        # return

    def deal_of_day(self):
        deal = None
        while deal is None:
            d = self.random_dispensary()
            menu = Menu(d.slug, d.tipe)
            deal = menu.todays_deal()

        return deal

    def download_images(self, urls, name):
        paths = []
        for i, url in enumerate(urls):
            if i == 0:
                title = name + 'bg'
            else:
                title = name
            base_dir = "postsToBeUploaded/"
            fmt = url.split(".")[-1]
            fmt = fmt.lower()
            urllib.request.urlretrieve(url, '{}{}.{}'.format(base_dir, title, fmt))
            if fmt not in ["JPG", "jpg"]:
                img = Image.open('{}{}.{}'.format(base_dir, title, fmt))
                rgb_im = img.convert('RGB')
                rgb_im.save('{}{}.jpg'.format(base_dir, title))
                os.remove('{}{}.{}'.format(base_dir, title, fmt))
            fmt = '.jpg'
            path = "postsToBeUploaded/" + title + fmt
            paths.append("postsToBeUploaded/" + title + fmt)
            trim.trim(path)

        return tuple(paths)

    def post_trending_product(self):
        top, name = trending.product()
        product = trending.product_listing()
        selling_dispensaries = trending.dispensary_holding_product(top)
        dString = ""
        for d in selling_dispensaries:
            dString += d.name + " | "
        print(dString)
        fmt = product['image_url'].split(".")[-1]
        img_path = self.post_dir + str(product['listing_id']) + "." + fmt
        urllib.request.urlretrieve(product['image_url'], "{}{}.{}".format(self.post_dir, str(product['listing_id']), fmt))
        pricesString = ""
        prices = product['prices']
        for p in prices:
            if prices[p] == 0:
                continue
            else:
                pricesString += "${}0 per {}.".format(prices[p], p)
        caption = "Check out this new trending product | {} | {} | Currently selling at {}".format(product['name'], pricesString, dString)
        p = post.Post(caption, img_path)
        p.launch()



    def create_post(self):
        deal = self.deal_of_day()
        print(deal)
        dispensary = deal['dispensary']['name']
        deal_image = deal['picture_urls']['large']
        avatar_image = deal['dispensary']['avatar_url']
        rating = "%.2f" % (deal['dispensary']['rating'])
        license_type = deal['dispensary']['license_type']
        listing_type = deal['dispensary']['listing_type']
        phone = deal['dispensary']['phone_number']
        bg_path, avatar_path = self.download_images([deal_image, avatar_image], dispensary)
        title = deal['title']
        img = Image.open(avatar_path, 'r')
        basewidth = 200
        wpercent = (0.85)
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(avatar_path)
        background = Image.open(bg_path, 'r')
        bg_w, bg_h = background.size
        bgbasewidth = 800
        bgwpercent = (0.85)
        bghsize = int((float(background.size[1]) * float(bgwpercent)))
        print( bghsize/ bgbasewidth)
        if bg_w / bg_h < 0.80:
            background = background.resize((bgbasewidth, bghsize), Image.ANTIALIAS)
            print(int(bg_w * .10))
            img.resize((int(bg_w * .05), int(bg_h*0.05)), Image.ANTIALIAS)
        offset = ((0) // 2, (0) // 2)
        background.paste(img, offset)
        background.save('post.jpg')
        hashtags = "#medibles #hightimes #sanfrancisco #710society #cannabiscommunity #cheapweed" \
                   "#marijuana #stoner #delivery #dispensary"
        self.caption = "Today's deal comes from {} | {} | Phone: {} | Rating: {} | License type: {} | {} " \
                       "{}".format(dispensary, title, phone, rating, license_type, listing_type, hashtags)


    def post_to_ig(self):
        self.create_post()
        b = Bot()
        b.login(username="CheapWeed_sf", password='shutupPb0y')
        post = 'post.jpg'
        b.upload_photo(post, caption=self.caption)
        b.logout()




def randomMinute():
    m = random.randint(30,59)
    randMin = m

randMin = random.randint(30,59)

if __name__ == '__main__':

    b = CheapWeedBot()
    # b.post_to_ig()
    schedule.every().day.at("19:{}".format(str(randMin))).do(b.post_to_ig)
    schedule.every().friday.at("20:{}".format(str(randMin))).do(b.post_trending_product())
    while True:
        schedule.run_pending()
        print("Running")
        time.sleep(60)
#



#
# b = CheapWeedBot()
# b.post_to_ig()




