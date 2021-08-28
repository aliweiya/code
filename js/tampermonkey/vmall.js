// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.vmall.com/*
// @icon         https://www.google.com/s2/favicons?domain=vmall.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let click_cnt = 0;

    function click() {
        let button = document.getElementById('pro-operation').children[0];
        console.log(`clicking ${click_cnt}`);
        button.click();
        click_cnt++;
    }

    // Your code here...
    let url = document.location.href;
    if (url.indexOf('product') > 0){
        let confirmResult = confirm("当前处于商品详情页面，是否开始抢购？");
        if (confirmResult) {
            setInterval(click, 10);
        }
    }
    else if (url.indexOf('order') > 0) {
        console.log('当前处于订单提交页面');
        let submitButton = document.getElementById("checkoutSubmit");
        submitButton.click();
    }
})();