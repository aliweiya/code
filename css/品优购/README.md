# TDK SEO优化


```html
<title></title>
<meta name="description" content="">
<meta name="keywords" content="">
```

# 常用模块类命名

| 名称             | 说明        |
| ---------------- | ----------- |
| 快捷导航栏       | shortcut    |
| 头部             | header      |
| 标志             | logo        |
| 购物车           | shopcar     |
| 搜索             | search      |
| 热点词           | hotwords    |
| 导航             | nav         |
| 导航左侧         | dropdown    |
| 导航右侧         | navitems    |
| 页面底部         | footer      |
| 页面底部服务模块 | mod_service |

# Logo SEO优化

1. logo里面首先放一个h1标签，目的是为了提权，告诉搜索引擎，这个地方很重要
2. h1里面放一个链接，可以返回首页
3. 为了搜索引擎收录，链接里要放文字，但是不显示出来
   - 方法一：`text-indent`移动到盒子外面，然后`overflow: hidden`，淘宝的做法
   - 方法二：直接给`font-size: 0`，京东的做法
   - 方法三：`color: transparent`
4. 最后给链接一个`title`属性，这样鼠标放到logo上就可以看到提示文字了。

# 首页制作

## main主体模块制作

- main盒子宽度为980像素，位置距离左边220px（margin-left），给高度就不用清除浮动
- main里面包含左侧盒子，左浮动，`focus`焦点图模块
- `main`里面包含右侧盒子，右浮动，`newsflash`新闻快报模块

