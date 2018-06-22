import instabot
from PIL import Image
import os
import trim


class Post:
    def __init__(self, caption, img_path):
        self.caption = caption
        self.hashtags = "#whocares"
        self.img_path = img_path

    def format_img(self):
        fmt = self.img_path.split(".")[-1]
        img_name = "".join(self.img_path.split(".")[:-1])
        fmt = fmt.lower()
        if fmt != "jpg":
            img = Image.open(self.img_path)
            rgb_im = img.convert('RGB')
            rgb_im.save('{}.jpg'.format(img_name))
            os.remove(self.img_path)
        fmt = '.jpg'
        self.img_path = img_name + fmt
        trim.trim(self.img_path)

    def resize(self):
        img = Image.open(self.img_path, 'r')
        w, h = img.size
        if w / h < 0.80:
            img = img.resize((int((h * 0.81)), h), Image.ANTIALIAS)
            img.save(self.img_path)

    def launch(self):
        b = instabot.Bot()
        b.login(username="cheapweed_sf", password="shutupPb0y")
        self.format_img()
        self.resize()
        b.upload_photo(self.img_path, self.caption)
        b.logout()


