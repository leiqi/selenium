# -*- coding:utf-8 -*-
'''
selenium操作浏览器的基本用法
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 引入keys包
import os,time
# 第一个例子:自动登陆豆瓣
# url = 'https://www.douban.com/accounts/login?source=movie' # 豆瓣的登陆界面网址
# driver = webdriver.Firefox()
# driver.get(url)
# driver.maximize_window() # 浏览器全屏
# driver.find_element_by_id('email').clear() # 找到输入用户名框，并清除默认信息
# driver.find_element_by_id('email').send_keys('××××××××××××') # 输入用户名
# driver.find_element_by_id('password').send_keys(Keys.TAB) # 等同于clear方法，TAB清除密码框的默认信息
# driver.find_element_by_id('password').send_keys('××××××××××××') # 输入密码
# driver.find_element_by_id('password').send_keys(Keys.ENTER) # 定位密码框，输入回车键
# title = driver.find_element_by_class_name('nav-user-account').text # 获取登陆成功后的验证信息，验证是否登陆成功
# print title
# # 第二个例子：自动输入关键词利用百度查找
def baidu_search():
    print("欢迎使用百度搜索助手")
    search_cotent = raw_input('请输入要百度的内容:')
    url = 'http://www.baidu.com'
    driver = webdriver.Firefox()
    driver.get(url)
    search_cotent = search_cotent.decode('utf-8')
    driver.find_element_by_id('kw').send_keys(search_cotent) # 发送关键词
    time.sleep(1) # 休眠1秒
    driver.find_element_by_id('su').click() # 点击搜索按钮
    page =raw_input('请输入要搜索的页面页数')
    page = int(page)
    if page == 1:
        n = raw_input('请输入要搜索第几条结果:(1-10)')
        n = int(n)
        u = driver.find_element_by_xpath('//*[@id="%d"]/h3/a[1]' % n)
        link = u.get_attribute('href')
        print '为您找到的链接为:'
        print link
        driver.find_element_by_xpath('//*[@id="%d"]/h3/a[1]' % n).click() # 点击第n条链接
        print '火狐浏览器页面已跳转，请查看!'
    else:
        driver.find_element_by_xpath('//*[@id="page"]/a[%d]/span[2]' % (page-1)).click() #跳转到第page页
        n = raw_input('请输入要搜索第几条结果:(1-10)')
        n = int(n)
        u = driver.find_element_by_xpath('//*[@id="%d"]/h3/a[1]' % (n+10*(page-1)))
        link = u.get_attribute('href')
        print '为您找到的链接为:'
        print link
        driver.find_element_by_xpath('//*[@id="%d"]/h3/a[1]' % (n+10*(page-1))).click() # 点击第n条链接
        print '火狐浏览器页面已跳转，请查看!'

if __name__ == '__main__':
    baidu_search()





