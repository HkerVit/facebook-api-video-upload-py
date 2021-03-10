
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAADZBROPXRHgBAG80dprQ3QVdROZAycaZCRBlQh7ZCk0HZBxhGvqwflEANMlTb20fK8cB6jBnx90ZAXElpaiMd6bjAPsZBAHkXQvKw9zwHdnFs7NHIdXvelbW6PTuZBqoO58B4m5kdJuAYg5JxLGAXxVqZCA9OJmXHlTC68QLSl41bQZDZD",
              id: "182766363336548",
              stream: fs.createReadStream('../douyin-downloader/Download/虫哥说电影/魔性解读土嗨蹦迪神剧《封神英雄榜》 这部剧是太雷人#封神英雄榜.mp4'),
              title:"魔性解读土嗨蹦迪神剧《封神英雄榜》 这部剧是太雷人#封神英雄榜" ,
              description:"魔性解读土嗨蹦迪神剧《封神英雄榜》 这部剧是太雷人#封神英雄榜",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });