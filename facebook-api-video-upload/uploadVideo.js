
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAACjQz8d4B0BAGE4QjXZAm1ZCW883t5izEBdPCL41r3ZCNwpfvfgWeIK8vhtJaFWZBXtEj78K3NAXhXdA5wEUNqQMHOEL3usBNZB8AOZAWFcimZC2JwJWZBFxL8NpTjco6cXwZBnVFXC4wDuOmlJyuDLbRHNtoblCe3upDZBizjDjd2u78cPXnPYBR",
              id: "JKCDY",
              stream: fs.createReadStream('../douyin-downloader/Download/虫哥说电影/魔性解读童年古装偶像剧《刁蛮公主》，一部正宗的套着古装外壳的偶像剧～#刁蛮公主.mp4'),
              title:"魔性解读童年古装偶像剧《刁蛮公主》，一部正宗的套着古装外壳的偶像剧～#刁蛮公主" ,
              description:"魔性解读童年古装偶像剧《刁蛮公主》，一部正宗的套着古装外壳的偶像剧～#刁蛮公主",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });