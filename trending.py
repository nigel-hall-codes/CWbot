import pandas as pd
import sqlite3
import datetime
import models
import menu

pathOnServer = "/root/WMScrape/Medigreen.db"
pathForDev = "/Users/Hallshit/newdir/M3digreen/M3digr33n/WeedmapsAnalysis/Medigreen.db"

conn = sqlite3.connect(pathOnServer)
c = conn.cursor()

def qTodf(q):
    q = c.execute(q)
    df = pd.DataFrame(q.fetchall())
    df.columns = [i[0] for i in q.description]
    return df

def newest_products():
    q = "select count(*) from product"
    q = c.execute(q)
    return int(q.fetchall()[0][0] * .80)


def product():
    last_week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("'%Y-%m-%d %H:%M:%S'")
    q = "SELECT * from dispensaryhasproduct where date > %s and productID > %s order by productid DESC" % (last_week, newest_products())
    df = qTodf(q)
    counts = df.groupby('productID').count().sort_values('dispensaryID', ascending=False).head()
    top = counts.head(1).index.values[0]
    name = (c.execute("SELECT name from product where id == %s" % top)).fetchone()[0]
    # df = df[df.productID == top]
    return top, name

def dispensary_holding_product(id):
    q = "SELECT dispensaryid from dispensaryhasproduct WHERE productID == %s" % id
    q = c.execute(q)
    dispensary_id = q.fetchall()
    dispensaries = [x[0] for x in dispensary_id]
    # print(dispensaries)
    dispensaries = models.Dispensary.select().where(models.Dispensary.id << dispensaries)
    return dispensaries

def category(id):
    q = "select categoryID from producthascategory WHERE productID == %s" % id
    q = c.execute(q)
    catID = q.fetchone()[0]
    name = (c.execute("SELECT name from category WHERE id == %s" % catID)).fetchone()[0]
    return name

def product_listing():
    pid, name = product()
    dispensaries = dispensary_holding_product(pid)
    for d in dispensaries:
        cat = category(pid)
        m = menu.Menu(d.slug, d.tipe)
        for c in m.data['categories']:
            if c['items'][0]['category_name'] == cat:
                for item in c['items']:
                    if item['name'] == name:
                        return item


print(product_listing())






