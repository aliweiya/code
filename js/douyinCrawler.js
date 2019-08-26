'use strict';

var mysql = require('mysql'),
    connection = mysql.createConnection({
        host: '192.168.9.150',
        user: 'test',
        password: '123456',
        database: 'test',
    })

connection.connect();

function addUser(user){
    /*
     * 添加用户到数据库
     * @param user.userid: 用户id，主键
     * @param user.source: 数据源，可选项为抖音、快手、小红书
     * @param user.nickname: 用户昵称
     * @param user.avator: 头像地址
     * @param user.home_page: 用户主页
     * @param user.address: 用户地址（可选）
     * @param user.gender: 性别
     * @param user.birthday: 生日
     */
    var sqlAddUser = "INSERT INTO user(userid, source, nickname, u_signature, avator, home_page, u_address, gender, birthday) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)";
    var sqlAddUserParams = [user.userid, user.source, user.nickname, user.signature, user.avator, user.home_page, user.address, user.gender, user.birthday];
    connection.query(sqlAddUser, sqlAddUserParams, function(error, result){
        if(error){
            console.log('[INSERT USER ' + user.nickname + 'ERROR] - ' + error.message);
        }
        else{
            console.log('[INSERT USER ' + user.nickname + 'SUCCESS]');
        }
    });
}

function addVideo(video){
    /*
     * 添加视频
     */
    var sqlAddVideo = "INSERT INTO video(vid, source, title, v_url, cover, promotion_title, promotion_cover, promotion_id, promotion_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)";
    var sqlAddVideoParams = [video.vid, video.source, video.title, video.url, video.cover, video.promotion_title, video.promotion_cover, video.promotion_id, video.promotion_url];
    connection.query(sqlAddVideo, sqlAddVideoParams, function(error, result){
        if(error){
            console.log('[INSERT VIDEO ' + video.vid + 'ERROR] - ' + error.message);
        }
        else{
            console.log('[INSERT VIDEO ' + video.vid + 'SUCCESS]');
        }
    });
}

module.exports = {
    *beforeSendResponse(requestDetail, responseDetail){
        if(requestDetail.url.indexOf("aweme/v1/feed/") > 0){
            var body = responseDetail.response.body;
            body = JSON.parse(body);
            for(var index=0; index<body.aweme_list.length; index++){
                var item = body.aweme_list[index]
                if(index == 0){
                    var user = {
                        'source': 'douyin',
                        'userid': item.author.short_id,
                        'nickname': item.author.nickname,
                        'signature': item.author.signature,
                        'avator': item.author.avatar_larger.url_list[0],
                        'home_page': '',
                        'address': '',
                        'gender': item.author.gender === 1 ? '男' : '女',
                        'birthday': new Date(item.author.birthday),
                    }
                    addUser(user);
                }
                var video = {
                    'source': 'douyin',
                    'vid': item.aweme_id,
                    'title': item.desc,
                    'url': item.video.play_addr.url_list[0],
                    'cover': item.video.origin_cover.url_list[0],
                }
                if(item.simple_promotions != undefined || item.simple_promotions != null){
                    var simple_promotions = JSON.parse(item.simple_promotions)[0];
                    console.log(simple_promotions);
                    video.promotion_id = simple_promotions.promotion_id;
                    video.promotion_title = simple_promotions.title;
                    video.promotion_cover = simple_promotions.elastic_images[0].url_list[0];
                    video.promotion_url = '';
                }
                addVideo(video);
            }
        }
    }
}