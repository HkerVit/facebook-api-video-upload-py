
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAADZBROPXRHgBAG80dprQ3QVdROZAycaZCRBlQh7ZCk0HZBxhGvqwflEANMlTb20fK8cB6jBnx90ZAXElpaiMd6bjAPsZBAHkXQvKw9zwHdnFs7NHIdXvelbW6PTuZBqoO58B4m5kdJuAYg5JxLGAXxVqZCA9OJmXHlTC68QLSl41bQZDZD",
              id: "182766363336548",
              stream: fs.createReadStream('../douyin-downloader/Download/虫哥说电影/毁童年系列之国产真人版《中华小当家》，原来全都是靠干爹... #宅家dou剧场.mp4'),
              title:"毁童年系列之国产真人版《中华小当家》，原来全都是靠干爹... #宅家dou剧场" ,
              description:"毁童年系列之国产真人版《中华小当家》，原来全都是靠干爹... #宅家dou剧场",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });