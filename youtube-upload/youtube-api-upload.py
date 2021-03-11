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
        if not isPosted(url, file):
            playlist="性感舞蹈-Sexy girls"
            cmd="youtube-upload --title='{}'  --description='{}'  --playlist='{}' '{}' ".format(title,description,playlist,filepath)
            print(cmd)
            print("Uploading:", file)
            os.system(cmd)
            writeHistory(url, file)
            break
        else:
            print("Exist:", file)

if __name__ == '__main__':
    dir = "../douyin-downloader/Download/Abby心肝儿/"
    id = "UCq1bOUxwwcUAPkwZ3QFr6QA"
    db_host = "45.76.170.159"
    db_user = "db_poster"
    db_name = "db_poster"
    db_pass = "ysq1159889481"
    postVideos(id, dir)
