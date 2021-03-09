
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAADZBROPXRHgBAG80dprQ3QVdROZAycaZCRBlQh7ZCk0HZBxhGvqwflEANMlTb20fK8cB6jBnx90ZAXElpaiMd6bjAPsZBAHkXQvKw9zwHdnFs7NHIdXvelbW6PTuZBqoO58B4m5kdJuAYg5JxLGAXxVqZCA9OJmXHlTC68QLSl41bQZDZD",
              id: "182766363336548",
              stream: fs.createReadStream('../douyin-downloader/Download/虫哥说电影/花式虐女主狗血宅斗神剧《烽火佳人》，不愧是我魏姐#宅家dou剧场.mp4'),
              title:"花式虐女主狗血宅斗神剧《烽火佳人》，不愧是我魏姐#宅家dou剧场" ,
              description:"花式虐女主狗血宅斗神剧《烽火佳人》，不愧是我魏姐#宅家dou剧场",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });