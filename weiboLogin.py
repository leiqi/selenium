# -*- coding:utf-8 -*-
'''
利用selenium模拟登陆微博并发送微博
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import codecs
url = 'http://login.weibo.cn/login/' # 手机端微博登陆地址

class weibohelper(object):
    def __init__(self):
        object.__init__(self)
        self.driver = webdriver.Firefox() # 使用火狐浏览器

    # 登陆微博函数
    def weiboLogin(self,username,password):
        self.driver.get(url)
        self.driver.find_element_by_xpath('/html/body/div[2]/form/div/input[1]').send_keys(username) # 用户名
        self.driver.find_element_by_xpath('/html/body/div[2]/form/div/input[2]').send_keys(password) # 密码
        imageCode = self.driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
        Codelink = imageCode.get_attribute('src') # 验证码链接
        print '验证码链接为:'
        print Codelink
        Code = raw_input('请打开链接输入验证码:')
        self.driver.find_element_by_xpath('/html/body/div[2]/form/div/input[3]').send_keys(Code.decode('utf-8'))
        self.driver.find_element_by_xpath('/html/body/div[2]/form/div/input[10]').click() # 点击登录

    # 搜索功能,可以搜索任意明星，访问其主页，打印其粉丝数，关注人数，以及最近微博等
    def find_star_info(self):
        star_name = raw_input('请输入要搜索的明星:')
        star_name = star_name.decode('utf-8')
        self.driver.find_element_by_xpath('/html/body/div[3]/a[4]').click() # 点击搜索按钮
        self.driver.find_element_by_xpath('//*[@name="keyword"]').send_keys(star_name)
        self.driver.find_element_by_xpath('//*[@name="suser"]').click() # 点击找人按钮
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]/a').click() # 点击搜索的第一个链接
        time.sleep(5)
        weibo_numbers = self.driver.find_element_by_xpath('html/body/div[3]/div/span').text # 总微博数目
        he_guanzhu = self.driver.find_element_by_xpath('html/body/div[3]/div/a[1]').text # 他关注的人数
        fans = self.driver.find_element_by_xpath('html/body/div[3]/div/a[2]').text # 粉丝数目
        print '基本信息为:'
        print weibo_numbers
        print he_guanzhu
        print fans
        N = raw_input('请输入要显示的微博数目:')
        N = int(N)
        i = 1
        while i <= N:
            while True:
                try:
                    results_link = self.driver.find_elements_by_class_name('c')
                    n = len(results_link)
                    for k in range(n-2):
                        weibo_text = results_link[k].find_element_by_class_name('ctt').text  # 微博正文内容
                        zan = results_link[k].find_element_by_partial_link_text('赞').text
                        zhuanfa = results_link[k].find_element_by_partial_link_text('转发').text
                        pinglun = results_link[k].find_element_by_partial_link_text('评论').text
                        print u'第%d条微博:%s' % (i,weibo_text)
                        print zan + u"  " + zhuanfa + u"  " + pinglun
                        i += 1
                    self.driver.find_element_by_link_text('下页').click()
                except Exception,e:
                    print e
                    print '已经加载了全部微博!'
                    i = N + 1
                    break


    # 查找最近微博
    def find_recent_weibo(self):
        N = raw_input('请输入要查看前多少页:')
        N = int(N)
        i = 1
        j = 1
        while j <= N:
            results_link = self.driver.find_elements_by_class_name('c')
            n = len(results_link)
            for result_link in results_link[0:(n-2)]:
                print '第%d页，第%d个最近微博:' % (j,i)
                print result_link.text
                i += 1
            j += 1
            self.driver.find_element_by_link_text('下页').click() # 点击下一页

    # 找到我发过的所有微博
    def find_all_my_weibos(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/a[1]').click() # 点击我的微博
        time.sleep(4)
        i = 1
        while True:
            try:
                results_link = self.driver.find_elements_by_class_name('c')
                n = len(results_link)
                for result_link in results_link[0:(n-2)]:
                    result = result_link.text # 一条微博内容
                    print '第%d条微博:' % i
                    print result
                    i += 1
                self.driver.find_element_by_link_text('下页').click()
                time.sleep(3)
            except:
                print '查找完成!'
                break
    # 找到所有我关注的人(昵称)
    def find_all_my_GZDR(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/a[2]').click() #我关注的人
        time.sleep(3)
        i = 1
        while True:
            try:
                users_link = self.driver.find_elements_by_tag_name('table') # 找到所有table标签
                for user_link in users_link:
                    user = user_link.text
                    print '第%d个我关注的人:' % i
                    print user
                    i += 1
                self.driver.find_element_by_link_text('下页').click()# 点击下一页
                time.sleep(3)
            except:
                print '查找完毕!'
                break

    # 找到所有我的粉丝(昵称)
    def find_all_my_fans(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/a[3]').click() #我的粉丝
        time.sleep(3)
        i = 1
        while True:
            try:
                users_link = self.driver.find_elements_by_tag_name('table') # 找到所有table标签
                for user_link in users_link:
                    user = user_link.text
                    print '我的第%d个粉丝:' % i
                    print user
                    i += 1
                self.driver.find_element_by_link_text('下页').click()# 点击下一页
                time.sleep(3)
            except:
                print '查找完毕!'
                break

    # 找到所有微博
    def find_all_weibos(self):
        i = 1
        j = 1
        while True:
            try:
                try:
                    self.driver.find_element_by_link_text('刷新页面').click()
                    time.sleep(3)
                    results_link = self.driver.find_elements_by_class_name('c')
                except:
                    results_link = self.driver.find_elements_by_class_name('c')
                n = len(results_link)
                for k in range(n-2):
                    result = results_link[k].text
                    print '第%d页第%d个微博:' %(j,i)
                    print result
                    i += 1
                j += 1
                self.driver.find_element_by_link_text('下页').click()
                time.sleep(3)
            except:
                print '查找完毕!'
                break




    # 搜索热门微博和热门话题
    def find_hot_weibos(self):
        self.driver.find_element_by_link_text('搜索').click() # 点击搜索
        n = raw_input('请输入 0----搜索热门微博 1----搜索热门话题')
        n = int(n)
        if n == 0:
            self.driver.find_element_by_link_text('热门微博').click()
            self.find_all_weibos()
        else:
            self.driver.find_element_by_link_text('热门话题').click()
            i = 1
            j = 1
            while True:
                try:
                    results_link =self.driver.find_elements_by_class_name('k')
                    n = len(results_link)
                    for k in range(n):
                        result = results_link[k].text
                        print '第%d页第%d个热门话题:' %(j,i)
                        print result
                        i += 1
                    self.driver.find_element_by_link_text('下一页').click()
                    j += 1
                except:
                    print '查找完毕!'
                    break
    # 搜索明星的粉丝，因为明星粉丝众多，少则百万，多则千万，所以一般是搜索部分粉丝，显示其昵称
    def find_star_fans(self):
        star_name = raw_input('请输入要搜索的明星:')
        self.driver.find_element_by_xpath('/html/body/div[3]/a[4]').click() # 点击搜索按钮
        self.driver.find_element_by_xpath('//*[@name="keyword"]').send_keys(star_name.decode('utf-8'))
        self.driver.find_element_by_xpath('//*[@name="suser"]').click() # 点击找人按钮
        self.driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]/a').click() # 点击搜索的第一个链接
        F = self.driver.find_element_by_xpath('/html/body/div[3]/div/a[2]')
        print star_name, #不换行
        print '的粉丝数目为:',
        print F.text
        F.click()
        i = 1
        fans_arr = [] # 用于存放粉丝昵称的数组
        while True:
                try:
                    table_links = self.driver.find_elements_by_tag_name('table')
                    for table_link in table_links:
                        table = table_link.text
                        arr = table.split('\n',1)
                        fan = arr[0] # 粉丝昵称
                        print '第 %d 个粉丝:' % i
                        print fan
                        fans_arr.append(fan +'\n')
                        i += 1
                    self.driver.find_element_by_link_text('下页').click() # 点击下页
                except:
                    print '查找完毕!'
                    break
        with codecs.open('fans.txt',mode='w',encoding='utf-8') as f: # 因为要插入中文，所以必须指明编码方式
            fans_arr = list(set(fans_arr))
            print '共找到%d个粉丝' % len(fans_arr)
            f.writelines(fans_arr)

    # 从某个微博粉丝开始，寻找尽可能多的用户昵称
    def find_users(self):
        all_users = [] # 用于存放全部用户昵称
        i = 1
        j = 1
        start_users = []
        with codecs.open('Weibousers.txt',mode='r',encoding='utf-8') as f:
            users = f.readlines()
            for user in users[198:1000]:
                user = user.strip() # 去换行
                start_users.append(user)

        try:
            while j <= 1:
                k = 1
                start0_users = []
                for start_user in start_users:
                        self.driver.find_element_by_link_text('搜索').click()
                        self.driver.find_element_by_xpath('//*[@name="keyword"]').send_keys(start_user)
                        self.driver.find_element_by_xpath('//*[@name="suser"]').click() # 点击找人按钮
                        try:
                            self.driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]/a').click() # 点击搜索的第一个链接
                            self.driver.find_element_by_xpath('/html/body/div[3]/div/a[2]').click() # 点击粉丝链接
                            while True:
                                try:
                                    users_link = self.driver.find_elements_by_tag_name('table') # 找到所有table标签
                                    for user_link in users_link:
                                        Split = user_link.text
                                        user_arr = Split.split('\n',1)
                                        user = user_arr[0]
                                        print '第%d个用户' % i
                                        all_users.append(user + '\n')
                                        start0_users.append(user)
                                        i += 1
                                    self.driver.find_element_by_link_text('下页').click()# 点击下一页
                                except:
                                    print '第%d个用户查找完毕!' % k
                                    k += 1
                                    break
                            continue
                        except:
                            continue
                start_users = start0_users
                j += 1
        except:
            all_users = list(set(all_users))
        print '共找到%d个用户' % len(all_users)
        with codecs.open('WeiboUsers1.txt',mode='a',encoding='utf-8') as f:
            f.writelines(all_users)


















    #实现发送一条微博的功能
    def send_weibo(self,content): # content为要发送的微博内容
        self.driver.find_element_by_xpath('//*[@rows="2"]').send_keys(Keys.CONTROL,'a') # 全选
        self.driver.find_element_by_xpath('//*[@rows="2"]').send_keys(Keys.CONTROL,'x') # 清除默认微博内容
        self.driver.find_element_by_xpath('//*[@rows="2"]').send_keys(content) # 填写要发送的内容
        self.driver.find_element_by_xpath('//html/body/div[5]/form/div/input[2]').click() # 发布按钮
        print '成功发送了一条微博!'

    # 定时发送微博
    def dingshi_weibo(self,Time,content): # time为间隔小时数目
            time.sleep(Time*60*60) # 休眠时间(秒)
            weibo.send_weibo(content) # 发送微博





















if __name__ == '__main__':
    print '欢迎使用微博助手'
    print '现在开始登陆微博！'
    username = raw_input('请输入用户名:')
    password = raw_input('请输入密码:')
    weibo = weibohelper() # 实例化一个类
    weibo.weiboLogin(username,password) # 登陆微博
    m = raw_input('请选择服务:0 查询明星信息  1 发送一条微博 2 发送一条定时微博 3 查看最近微博 4 查找我的全部微博 5 查找全部我关注的人 6 查找我全部粉丝 7 搜索热门微博和热门话题 8 搜索用户粉丝昵称 9 寻找海量微博用户')
    m = int(m)
    if m == 0:
        print '您选择查询明星信息'
        weibo.find_star_info()
    elif m == 1:
        print '您选择发送一条微博:'
        content = raw_input('请输入要发送的微博内容:')
        weibohelper.send_weibo(content)
    elif m == 2:
        delta_time = raw_input('请选择在多少小时之后发送微博:')
        delta_time = float(delta_time)
        content = raw_input('请输入要发送的内容:')
        content = content.decode('utf-8')
        weibo.dingshi_weibo(delta_time,content) # 发送定时微博
    elif m == 3:
        weibo.find_recent_weibo()
    elif m == 4:
        weibo.find_all_my_weibos()
    elif m == 5:
        weibo.find_all_my_GZDR()
    elif m == 6:
        weibo.find_all_my_fans()
    elif m == 7:
        weibo.find_hot_weibos()
    elif m == 8:
        weibo.find_star_fans()
    else:
        weibo.find_users()



















