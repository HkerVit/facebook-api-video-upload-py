
            const fs = require('fs');
            const fbUpload = require('facebook-api-video-upload');
            const args = {
              token: "EAAkv5kR8PuUBAIohE61gNQKNSipCQ1wZCBdGBYbPYDUqBZBGqLOUVaFBG9rZAkvke5WCcJ9kzND6ZCiRhSe3ZCaJVL5eZCWTIrva2h5Uh3QeYVoz7hIShI5U0HVpFbFtLlyK6ZBu2h0edPLUWmKEsWv1W2hGyykXFZAP9u66k4hTbwZDZD",
              id: "91videos",
              stream: fs.createReadStream('./douyinhelper/Download/张项/无标题1614824203.mp4'),
              title:"无标题1614824203" ,
              description:"无标题1614824203",
            };
            fbUpload(args).then((res) => {
              console.log('res: ', res);
            }).catch((e) => {
              console.error(e);
            });