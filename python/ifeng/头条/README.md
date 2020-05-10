混淆后的js文件只能放到浏览器里执行，nodejs会报错，目前找不到是那个值未定义，我就先放在浏览器里，用selenium控制执行。

如果直接用selenium执行js的话，返回的sign是不能用的，猜测可能是检测了调用堆栈，目前没有找到解决方案。

因此，我开了一个服务，浏览器获取任务，计算sign，然后返回，主要流程如下：
1. home页引用计算sign的js，然后等这个文件执行完，就可以调用`window.byted_acrawler.sign`计算
2. 接收别的请求，然后转发到浏览器，等浏览器计算完，再把计算完成的sign返回

开启服务：

```bash
python server.py
```

在浏览器中访问：

```
http://127.0.0.1:8888/sign?url=https%3A//www.toutiao.com/toutiao/api/pc/feed/%3Fcategory%3Dpc_profile_ugc%26utm_source%3Dtoutiao%26visit_user_id%3D4377795668%26max_behot_time%3D0%26t%3D1586874840391
```