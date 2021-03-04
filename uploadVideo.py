import pymysql
import os
import hashlib
import sys
import time

def writeHistory(url, file):
    txt = url + file
    md5 = hashlib.md5(txt.encode("utf-8")).hexdigest()
    db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
    cursor = db.cursor()
    add_sql = "INSERT INTO db_poster(history)VALUES ('{}')".format(md5)
    cursor.execute(add_sql)
    db.commit()
    db.close()

def isPosted(url, file):
    txt = url + file
    md5 = hashlib.md5(txt.encode("utf-8")).hexdigest()
    db = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
    cursor = db.cursor()
    find_sql = "SELECT * FROM db_poster WHERE history='{}'".format(md5)
    cursor.execute(find_sql)
    result = cursor.fetchone()
    db.close()
    if result is None:
        result = False
    elif len(result) > 0:
        result = True
    return result

def postVideos(url, dir):
    for file in os.listdir(dir):
        filepath = dir + file
        title = file.replace('.mp4', '')
        description = title
        txt = url + file
        if not isPosted(url, file):
            f = open("uploadVideo.js", "w", encoding='utf-8')
            context = """
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "_token",
              id: "_id",
              stream: fs.createReadStream('_filepath'),
              title:"_title" ,
              description:"_description",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });"""
            context = context.replace('_token', token)
            context = context.replace('_id', id)
            context = context.replace('_filepath', filepath)
            context = context.replace('_title', title)
            context = context.replace('_description', description)
            f.write(context)
            f.close()
            print("Uploading:", file)
            os.system("nodejs uploadVideo.js")
            writeHistory(url, file)
            break
        else:
            print("Exist:", file)


if __name__ == '__main__':
    dir = "./douyinhelper/Download/张项/"
    token = "EAAkv5kR8PuUBAIohE61gNQKNSipCQ1wZCBdGBYbPYDUqBZBGqLOUVaFBG9rZAkvke5WCcJ9kzND6ZCiRhSe3ZCaJVL5eZCWTIrva2h5Uh3QeYVoz7hIShI5U0HVpFbFtLlyK6ZBu2h0edPLUWmKEsWv1W2hGyykXFZAP9u66k4hTbwZDZD"
    id = "91videos"
    # id="1151912901898368"
    # id="jkmovie"
    # id="100480575447454"
    
    db_host = "45.76.170.159"
    db_user = "db_poster"
    db_name = "db_poster"
    db_pass = "ysq1159889481"
    postVideos(id, dir)
