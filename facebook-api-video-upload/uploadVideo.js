
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAADZBROPXRHgBAG80dprQ3QVdROZAycaZCRBlQh7ZCk0HZBxhGvqwflEANMlTb20fK8cB6jBnx90ZAXElpaiMd6bjAPsZBAHkXQvKw9zwHdnFs7NHIdXvelbW6PTuZBqoO58B4m5kdJuAYg5JxLGAXxVqZCA9OJmXHlTC68QLSl41bQZDZD",
              id: "182766363336548",
              stream: fs.createReadStream('../douyin-downloader/Download/虫哥说电影/魔性解读中二爆笑校园神剧《终极一班》，中二魂爆表了 #终极一班.mp4'),
              title:"魔性解读中二爆笑校园神剧《终极一班》，中二魂爆表了 #终极一班" ,
              description:"魔性解读中二爆笑校园神剧《终极一班》，中二魂爆表了 #终极一班",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });