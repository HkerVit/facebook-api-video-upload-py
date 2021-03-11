import sys, getopt
import requests
import json
import os
import pymysql

def get_history(bvid):
    find_sql = "SELECT * FROM download_history_bilibili WHERE bvid='{}'".format(bvid)
    findres = cursor.execute(find_sql)
    if findres == 0:
        res = False
    else:
        res = True
    return res

def get_url_list(uid):
    url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    data = json.loads(requests.get(url).text)
    if data["code"] == 0:
        count = data["data"]["page"]["count"]
        page_count = int(count/30) + 1
        for page in range(page_count):
            pn = page + 1
            url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate&jsonp=jsonp"
            page_vdict = json.loads(requests.get(url).text)["data"]["list"]["vlist"]
            for vdict in page_vdict:
                bvid="https://www.bilibili.com/video/"+vdict["bvid"]
                vdict['bvid']=bvid
                vdict['pic']=vdict['pic'].replace("//",'')
                bvidExits=get_history(bvid)
                if not bvidExits:
                    values_list = list(vdict.values())
                    values_list = ["0"] + values_list
                    values = tuple(values_list)
                    add_sql = "INSERT INTO download_history_bilibili  VALUES {}".format(values)
                    cursor.execute(add_sql)
                    db.commit()
                    print("Insert: ", bvid)
                elif bvidExits:
                    print("Exist: ",bvid)


def downloadVideo(uid):
    find_sql = "SELECT * FROM download_history_bilibili WHERE mid='{}'".format(uid)
    cursor.execute(find_sql)
    res=cursor.fetchall()
    for r in res:
        bvid = r[16]
        author=r[10]
        path = "./download/{}/".format(author)
        pathExist=os.path.exists(path)
        if not pathExist:
            os.makedirs(path)
        cmd = "annie -o {} {}".format(path,bvid)
        os.system(cmd)


if __name__ == "__main__":
    db_host = "45.76.170.159"
    db_user = "db_poster"
    db_name = "db_poster"
    db_pass = "ysq1159889481"
    db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
    cursor = db.cursor()
    # get_url_list(15183062)
    downloadVideo(15183062)
    db.close()
