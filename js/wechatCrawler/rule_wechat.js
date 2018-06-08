'use strict';

// 使用anyproxy爬取微信公众号文章和评论

var cheerio  = require('cheerio'),
    mongo    = require('mongodb'),
    url      = ":3717/",
    dbname   = 'mongodb://dds-bp1dfb31d5fbb4741703-pub.mongodb.rds.aliyuncs.com',
    dbport   = 3717,
    collname = 'crawler',
    dbuser   = 'ugc',
    dbpass   = 'a1b2c3d4',
    db       = new mongo.Db(dbname, new mongo.Server(dbname, dbport, {}), {});

db.authenticate(dbuser, dbpass, function(err, res){
  console.log(err);
})

function fix_url(url){
  return url.replace(/\\\//g, '\\').replace(/amp;/g, '')
}

function get_history_url(items){
  for (var index=0; index<items.length; index++){
    // console.log(items[index]['comm_msg_info']);
    var app_msg_ext_info = items[index]['app_msg_ext_info']
    console.log(app_msg_ext_info['title'], fix_url(app_msg_ext_info['content_url']));
    var multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list'];
    for(var j=0; j<multi_app_msg_item_list.length; j++){
      console.log(multi_app_msg_item_list[j]['title'], fix_url(multi_app_msg_item_list[j]['content_url']));
    }
  }
}

module.exports = {

  summary: 'the rule for wechatCrawler',

  /**
   *
   *
   * @param {object} requestDetail
   * @param {object} responseDetail
   */
  *beforeSendResponse(requestDetail, responseDetail) {
    if (requestDetail.url.indexOf("https://mp.weixin.qq.com/mp/profile_ext?action=home") === 0){
      // 历史消息页面
      // 正则匹配出msgList
      var body = responseDetail.response.body
      var regex_str = /(var\smsgList\s=\s\')(.+?\})(\';)/m;
      var content = regex_str.exec(body)[2];
      content = content.replace(/&quot;/g,'"');
      content = JSON.parse(content);
      var items = content['list'];
      get_history_url(items);
    }
    else if (requestDetail.url.indexOf("https://mp.weixin.qq.com/mp/profile_ext?action=getmsg") === 0){
      // 历史消息页面加载的数据
      var body = responseDetail.response.body;
      var content = JSON.parse(body);
      console.log(content['general_msg_list']);
      var items = JSON.parse(content['general_msg_list']);
      var items = items['list'];
      get_history_url(items);
    }
    else if (requestDetail.url.indexOf("https://mp.weixin.qq.com/s?") === 0){
      // 文章内容
      // 通过正则匹配查找标题
      var body = responseDetail.response.body
      var regex_str = /(document\.write\(\"<span class=\'rich_media_title_ios\'>)(.+?)(<\/span>\"\);)/m;
      var title = regex_str.exec(body)[2];
      // 解析内容，获取文章
      var $ = cheerio.load(body);
      var content = $('#js_content').text();
      console.error(title, content);
    }
    else if (requestDetail.url.indexOf("https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment") === 0){
      // 评论
      var body = responseDetail.response.body;
      var json = JSON.parse(body);
      var comments = json['elected_comment'];
      for (var index=0; index<comments.length; index ++){
        console.log(comments[index]['nick_name'], comments[index]['content']);
      }
    }
  },

  /**
   *
   *
   * @param {any} requestDetail
   * @param {any} error
   * @returns
   */
  *onError(requestDetail, error) {
    return null;
  },


  /**
   *
   *
   * @param {any} requestDetail
   * @param {any} error
   * @returns
   */
  *onConnectError(requestDetail, error) {
    return null;
  },
};
