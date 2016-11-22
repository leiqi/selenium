# -*- coding:utf-8 -*-
'''
网易云音乐歌曲<<晴天>>评论抓取
时间:2016/11/20
网页地址:http://music.163.com/#/song?id=186016
截止评论数:1078803
'''
from selenium import webdriver

def get_all_comments(url):
    comments_list = [] # 评论列表
    driver = webdriver.Firefox() # 启用火狐浏览器
    driver.get(url)
    driver.switch_to.frame('g_iframe')
    driver.implicitly_wait(3) # 智能等待3秒
    while True:
        try:
            comments_link = driver.find_elements_by_class_name('cnt f-brk')
            for comment_link in comments_link:
                comment = comment_link.text
                comments_list.append(comment)
        except Exception,e:
            print e

        break
    return comments_list

if __name__ == '__main__':
    url = 'http://music.163.com/#/song?id=186016'
    comments_list = get_all_comments(url)
    for comment in comments_list:
        print comment
    