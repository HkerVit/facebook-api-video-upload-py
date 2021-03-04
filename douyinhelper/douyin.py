#!/usr/bin/env python
# encoding: utf-8
import os, sys, requests
import json, re, hashlib, time
import configparser
from retrying import retry
from contextlib import closing
import pymysql

ini_text = '''
[config]
#请用notepad++或者sublimeText编辑，并确保编码类型为GB2312
#用户主页链接可以在抖音用户主页分享-》复制链接，然后粘贴在此，多用户用,分隔（英文状态下的逗号）
user_list=https://v.douyin.com/JWTACSX/,https://v.douyin.com/J76dSXL/,https://v.douyin.com/J76kbWF/
#所有作品保存的根目录
save_dir=./Download/
#用于填充进度条长度，如果进度条过长或过短，可以调整该数值
进度块个数=50
'''
 
class DouYin:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        self.config = configparser.ConfigParser()
        self.shared_list = []
        self.history = []
        self.save_path = './Download/'
        self.block_count = 50
        self.current_download_name = ''
        self.db_host = "45.76.170.159"
        self.db_user = "db_poster"
        self.db_name = "db_poster"
        self.db_pass = "ysq1159889481"
        self.db = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
        self.cursor = self.db.cursor()

    def read_config(self):
        if not os.path.exists('config.ini'):
            print('配置文件不存在，创建默认的配置文件')
            with open('config.ini', 'a+') as f:
                f.write(ini_text)
            print('创建默认配置文件完成')
        try:
            self.config.read('config.ini')
            value = self.config.get('config', 'user_list')
            if not value:
                input('-用户主页列表为空，请先配置再重试，按任意键继续')
                exit(0)
            self.shared_list = value.split(',')
            print('---配置的用户列表为:')
            for url in self.shared_list:
                print(url)
            value = self.config.get('config', 'save_dir')
            if value:
                self.save_path = value
            print('---保存的目录为:' + self.save_path)
            value = self.config.get('config', 'process_num')
            if value:
                self.block_count = int(value)
        except:
            input('读取配置文件失败，请确保配置正确，编码是否为GB2312，请使用SublimeText或NotePad++编辑，按任意键继续')
            exit(0)

    def hello(self):
        return self

    def remove(self):
        if os.path.exists(self.current_download_name):
            os.remove(self.current_download_name)
 
    def get_video_urls(self, sec_uid, max_cursor):
        user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&max_cursor={1}&count=2000'
        i = 0
        result = []
        has_more = False
        while result == [] and i<100:
            i = i + 1
            sys.stdout.write('---解析视频链接中 正在第 {} 次尝试...\r'.format(str(i)))
            sys.stdout.flush()
            user_url = user_url_prefix.format(sec_uid, max_cursor)
            response = self.get_request(user_url)
            html = json.loads(response.content.decode())
            if html['aweme_list'] != []:
                max_cursor = html['max_cursor']
                has_more = bool(html['has_more'])
                result = html['aweme_list']

        nickname = None
        video_list = []
        for item in result:
            if nickname is None:
                nickname = item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '', item['author']['nickname']) else None
 
            video_list.append({
                'desc': re.sub(r'[\/:*?"<>|]', '', item['desc']) if item['desc'] else '无标题' + str(int(time.time())),
                'url': item['video']['play_addr']['url_list'][0]
            })
        return nickname, video_list, max_cursor, has_more
 

    #下载视频
    def video_downloader(self, video_url, video_name):
        size = 0
        video_url = video_url.replace('aweme.snssdk.com', 'api.amemv.com')
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                text = '----[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024)
                self.current_download_name = video_name
                with open(video_name, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        done = int(self.block_count * size / content_size)
                        sys.stdout.write('%s [下载进度]:%s%s %.2f%%\r' % (text, '█' * done, ' ' * (self.block_count - done), float(size / content_size * 100)))
                        sys.stdout.flush()
                os.rename(video_name, video_name+'.mp4')

 
    @retry(stop_max_attempt_number=3)
    def get_request(self, url, params=None):
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response
 
    @retry(stop_max_attempt_number=3)
    def post_request(self, url, data=None):
        if data is None:
            data = {}
        response = requests.post(url, data=data, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def get_sec_uid(self, url):
        rsp = self.get_request(url)
        sec_uid = re.search(r'sec_uid=.*?\&', rsp.url).group(0)
        return sec_uid[8:-1]

    def get_history(self,md5):
        find_sql = "SELECT * FROM download_history_douyin WHERE download_history='{}'".format(md5)
        findres = self.cursor.execute(find_sql)
        if findres == 0:
            res=False
        else:
            res=True
        return res


    def save_history(self, md5):
        find_sql = "SELECT * FROM download_history_douyin WHERE download_history='{}'".format(md5)
        findres = self.cursor.execute(find_sql)
        if findres == 0:
            add_sql = "INSERT INTO download_history_douyin(download_history)VALUES ('{}')".format(md5)
            self.cursor.execute(add_sql)
            self.db.commit()

    
    def disk_space(self,disk):
            st = os.statvfs(disk)
            return st.f_bavail * st.f_frsize/1024//1024//1024
        
    
    
    def run(self):
        self.read_config()
        space=self.disk_space("./")
        print("磁盘剩余空间 ",space," G")
        for url in self.shared_list:
            space=self.disk_space("./")
            if space>1:
               try:
                    print('正在解析下载 ' + url)
                    self.get_video_by_url(url)
               except:
                    print('下载出错，停止 ' + url)
                    pass  
            else:
                print("磁盘剩余空间小于1G")
                break

    def get_video_by_url(self, url):
        max_cursor = 0
        has_more = True
        total_count = 0
        sec_uid = self.get_sec_uid(url)
        if not sec_uid:
            print('获取sec_uid失败')
            return
        print('---获取sec_uid成功: ' + sec_uid)
 
        while has_more:
            nickname, video_list, max_cursor, has_more = self.get_video_urls(sec_uid, max_cursor)
            nickname_dir = os.path.join(self.save_path, nickname)
     
            if not os.path.exists(nickname_dir):
                os.makedirs(nickname_dir)

            page_count = len(video_list)
            total_count = total_count + page_count
            # print('---视频下载中 本页共有{0}个作品 累计{1}个作品 翻页标识:{2} 是否还有更多内容:{3}\r'
            #     .format(page_count, total_count, max_cursor, has_more))

            for num in range(page_count):
                title = video_list[num]['desc']
                title = title.replace('@抖音小助手', '').strip()
                # print('---正在解析第{0}/{1}个视频链接 [{2}]，请稍后...'.format(num + 1, page_count, title))
     
                video_path = os.path.join(nickname_dir, title)
                history_name = nickname + '\\' + title
                md5 = hashlib.md5(history_name.encode('utf-8')).hexdigest()
                md5 = md5.strip() + '\n'
                isDownloaded = self.get_history(md5)
                if isDownloaded:
                    print('---{0} -- 已下载过...'.format(history_name))
                else:
                    print('---{0} -- 开始下载...'.format(history_name))
                    self.video_downloader(video_list[num]['url'], video_path)
                    self.save_history(md5)
                # print('\n')
            print('---本页视频下载完成...\r')

 
if __name__ == "__main__":
    app = DouYin()
    try:
        app.hello().run()
    except KeyboardInterrupt:
        app.remove()
        input('\r\n终止下载，按任意键退出。。。')
        exit(0)