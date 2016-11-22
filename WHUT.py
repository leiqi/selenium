# -*- coding:utf-8 -*-
'''
selenium模拟登陆理工教务处
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 引入keys包
import os,time
# 第一个例子:自动登陆豆瓣
url = 'http://sso.jwc.whut.edu.cn/Certification//toIndex.do' # 教务处地址
driver = webdriver.Firefox() # 使用火狐浏览器
driver.get(url)
driver.maximize_window() # 浏览器全屏

driver.find_element_by_xpath('//*[@id="textfield"]').clear()
driver.find_element_by_xpath('//*[@id="textfield"]').send_keys('0121314670302') # 学号
driver.find_element_by_xpath('//*[@id="textfield2"]').clear()
driver.find_element_by_xpath('//*[@id="textfield2"]').send_keys('12345abcde') # 密码
driver.find_element_by_xpath('//*[@id="imageField"]').click() # 点击登陆按钮
driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/ul/li[7]/a').click() # 学生成绩管理

# 查询成绩信息
driver.find_element_by_xpath('//*[@id="sidebar"]/div[2]/div[2]/ul/li[1]/ul/li[1]/div/a').click() # 点击有效成绩信息查询按钮










