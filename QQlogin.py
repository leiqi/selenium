# -*- coding:utf-8 -*-
'''
利用selenium模拟登陆QQ(邮箱)并且做一些有意思的事情
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# 打印数组
def print_arr(arr):
    n = len(arr)
    for i in range(n):
        print arr[i]

# 获得我的好友动态信息
def get_mypage_info(driver):
    # 当前页面所有好友昵称
    nick_names_link = driver.find_elements_by_class_name('f-nick')
    nick_names = []
    for nick_name_link in nick_names_link:
        nick_name = nick_name_link.text
        nick_names.append(nick_name) # 获得昵称数组


    # 具体信息
    info_details_link = driver.find_elements_by_class_name('info-detail')
    info_details = []
    for info_detail_link in info_details_link:
        info_detail = info_detail_link.text
        info_details.append(info_detail)

    # 说说的文字部分
    text_details_link = driver.find_elements_by_class_name('f-info')
    text_details = []
    for text_detail_link in text_details_link:
        text_detail = text_detail_link.text
        text_details.append(text_detail)

    # 配图以及转发说说文字内容及图片(如果有的话)
    qz_summarys = driver.find_elements_by_xpath('//*[@class="f-wrap"]/div/div[2]') # 配图以及转发信息皆包含在这个当中
    Images_src = [] # 每个用户的配图信息数组
    zhuanfa_texts = [] # 用于存放转发信息
    for qz_summary in qz_summarys:
        imgs = qz_summary.find_elements_by_tag_name('img') # 找到所有的img标签
        imgs_src = [] # 保存所有img 的url地址
        for img in imgs:
            img_src = img.get_attribute('src')
            imgs_src.append(img_src)
        Images_src.append(imgs_src) # 逐个添加用户配图信息

        try:
            zhuanfa_text_link = qz_summary.find_element_by_class_name('txt-box') # 转发内容
            zhuanfa_text = zhuanfa_text_link.text # 获得转发内容
        except:
            zhuanfa_text = 0
        zhuanfa_texts.append(zhuanfa_text)

    # 回复详情
    comments_list = []
    comments_list_link = driver.find_elements_by_class_name('comments-list')
    for comment_list_link in comments_list_link:
        comment_list = comment_list_link.text
        comments_list.append(comment_list)
    # 回复基本情况(评论人数，点赞人数等)
    comments_basic_info = []
    comments_basic_info_link = driver.find_elements_by_class_name('f-detail')
    for comment_basic_info_link in comments_basic_info_link:
        comment_basic_info = comment_basic_info_link.text
        comments_basic_info.append(comment_basic_info)

    n = len(nick_names) # 获得信息数量
    print '共为您找到 %d 位好友动态:' % n
    for i in range(n):
        print '第 %d 位好友动态信息:' % (i+1)
        print '空间昵称:' + nick_names[i].encode('utf-8')
        print '发表说说详细信息:' + info_details[i].encode('utf-8')
        print '回复、点赞基本信息:' + comments_basic_info[i].encode('utf-8')
        try:
            print '回复具体信息:' + comments_list[i].encode('utf-8')
        except:
            print '回复具体信息:暂无回复'
        print '说说文字内容:' + text_details[i].encode('utf-8')
        Image_src = Images_src[i] # 配图信息
        zhuanfa_content = zhuanfa_texts[i]
        if zhuanfa_content == 0:
            zhuanfa_boolean = False # 非转发
        else:
            zhuanfa_boolean = True # 有转发
        if zhuanfa_boolean == False:
            print '非转发'
            print '配图地址为:'
            print_arr(Image_src)
        else:
            print '有转发'
            print '转发内容为:' + zhuanfa_content.encode('utf-8')
            print '配图地址为:'
            print_arr(Image_src)


def get_myLYB(driver):
    LYB_link = driver.find_element_by_xpath('//*[@class="head-nav-menu"]/li[4]/a')
    LYB_link.click() # 点击跳转到留言板页面

# 得到留言板信息
def get_LYB_info(driver):
    # 留言板用户基本信息
    LYB_users_info_link = driver.find_elements_by_class_name('tit')
    LYB_users_info = []
    for LYB_user_info_link in LYB_users_info_link:
        LYB_user_info = LYB_user_info_link.text
        LYB_users_info.append(LYB_user_info)

    # 用户留言具体内容
    LYB_users_content = []
    LYB_users_content_link = driver.find_elements_by_class_name('cont')
    for LYB_user_content_link in LYB_users_content_link:
        LYB_user_content = LYB_user_content_link.text
        LYB_users_content.append(LYB_user_content)

    print_arr(LYB_users_info)
    print_arr(LYB_users_content)
def YWXG_info(driver):
    # 获得用户基本信息
    basic_infos_link = driver.find_elements_by_class_name('f-user-info')
    basic_infos = []
    for basic_info_link in basic_infos_link:
        basic_info = basic_info_link.text
        basic_infos.append(basic_info)

    # 起始回复的内容
    start_HFs = []
    start_HFs_link = driver.find_elements_by_class_name('txt-box')
    for start_HF_link in start_HFs_link:
        start_HF = start_HF_link.text
        start_HFs.append(start_HF)
    # 回复详情
    comments_list = []
    comments_list_link = driver.find_elements_by_class_name('comments-list')
    for comment_list_link in comments_list_link:
        comment_list = comment_list_link.text
        comments_list.append(comment_list)
    # 回复基本情况(评论人数，点赞人数等)
    comments_basic_info = []
    comments_basic_info_link = driver.find_elements_by_class_name('f-detail')
    for comment_basic_info_link in comments_basic_info_link:
        comment_basic_info = comment_basic_info_link.text
        comments_basic_info.append(comment_basic_info)

    n = len(basic_infos) # 获得信息条数
    print '共获得了%d条与我相关回复信息' % n
    for i in range(n):
        print '第%d条回复信息:' % (i+1)
        print '用户基本信息:' + basic_infos[i].encode('utf-8')
        print '起始回复内容:' + start_HFs[i].encode('utf-8')
        try:
            print '回复基本情况:' + comments_basic_info[i].encode('utf-8')
        except:
            print '回复基本情况:暂无信息'
        try:
            print '回复详情:' + comments_list[i].encode('utf-8')
        except:
            print '回复详情:暂无信息'


class QQ_zone(object):
    def __init__(self):
        object.__init__(self)

    # QQ空间登陆
    def QQ_login(self):
        # url = 'https://mail.qq.com/cgi-bin/loginpage' # QQ邮箱登陆地址
        url = 'http://qzone.qq.com/' # 空间登录地址
        driver = webdriver.Firefox() # 使用火狐浏览器
        driver.get(url)
        driver.switch_to.frame('login_frame') # 注意QQ登陆需要切换框架，切换到输入密码框架
        driver.find_element_by_id('switcher_plogin').click()
        u1 = driver.find_element_by_class_name('uinArea')
        u1.find_element_by_id('u').clear()
        u1.find_element_by_id('u').send_keys('919987476') # 输入用户名
        u2 = driver.find_element_by_class_name('pwdArea')
        u2.find_element_by_id('p').clear()
        u2.find_element_by_id('p').send_keys('hcc19952100..00')# 输入密码
        driver.find_element_by_id('login_button').click() # 点击登陆按钮
        return driver



if __name__ == '__main__':
    qq = QQ_zone()
    driver = qq.QQ_login()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[-1]) # 跳转到登陆以后的页面
    windows_handle1 = driver.current_window_handle # 首页的窗口句柄
    print '欢迎QQ空间助手!'
    n = raw_input('请选择输入:0----查看最近好友动态 1-----查看特别关心好友动态 2-----与我相关 3----那年今日')
    n = int(n)
    if n == 0:
        js="var q=document.documentElement.scrollTop=10000" # 将浏览器滚动条拉到底端
        driver.execute_script(js)
        get_mypage_info(driver)
    elif n == 1:
        driver.find_element_by_link_text("特别关心").click()
        js="var q=document.documentElement.scrollTop=10000" # 将浏览器滚动条拉到底端
        driver.execute_script(js)
        get_mypage_info(driver)
    elif n == 2:
        driver.find_element_by_link_text("与我相关").click()
        js="var q=document.documentElement.scrollTop=10000" # 将浏览器滚动条拉到底端
        driver.execute_script(js)
        YWXG_info(driver)
    elif n == 3:
        driver.find_element_by_link_text("那年今日").click()
        js="var q=document.documentElement.scrollTop=10000" # 将浏览器滚动条拉到底端
        driver.execute_script(js)
        get_mypage_info(driver)
































