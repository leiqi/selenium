# -*-coding:utf-8 -*-
'''
使用bs4，利用搜狗微信搜索接口根据微信公众号名称获取其id，
并自动填充至excel
'''

import xlwt,xlrd
from bs4 import BeautifulSoup
import urllib2,urllib
import sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 引入keys包



# 根据微信公众号名称搜索id
def GetIdBySougou(content):
    content1 = urllib.quote_plus(content.encode("utf-8"))
    url = "http://weixin.sogou.com/weixin?type=1&query="+content1+"&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=611024&sst0=1477387447287&lkt=1%2C1477387446213%2C1477387646214"  # 搜狗微信搜索入口url
    url = "http://weixin.sogou.com/weixin?type=1&query=%E8%8E%86%E7%94%B0%E5%BE%AE%E5%9F%8E%E4%BA%8B&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=2115&sst0=1477389259646&lkt=1%2C1477389258378%2C1477389258378"
    html = urllib2.urlopen(url).read() # 网页源码
    soup = BeautifulSoup(html,"html.parser")
    title_links = soup.find_all("h3")
    Id_links = soup.find_all("label")
    n = 0
    flag = False
    for title_link in title_links:
        title = title_link.text
        n += 1
        if title == content:
            flag = True
            break
    if flag == True:
        Id = Id_links[n-1].get_text()
    else:
        Id = None
    return Id

# 利用selenium模拟浏览器获取id
def GetIdBySelenium(contents_list,i):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Weixin')
    ws.write(0,0,u"公众号名称")
    ws.write(0,1,"Id")
    driver = webdriver.Firefox()
    url = "http://weixin.sogou.com/"
    driver.get(url)
    count = 1
    try:
        for content in contents_list[0:len(contents_list)]:
            flag = False
            n = 0
            if count == 1:
                driver.find_element_by_xpath('//*[@id="upquery"]').send_keys(contents_list[0]) # 发送关键词
                driver.find_element_by_xpath('//*[@id="searchForm"]/div[2]/input[3]').click() # 点击搜索公众号
                time.sleep(3)
            else:
                driver.find_element_by_xpath('//*[@id="upquery"]').clear() # 清除搜索框
                driver.find_element_by_xpath('//*[@id="upquery"]').send_keys(content) # 发送关键词
                driver.find_element_by_xpath('//*[@id="searchForm"]/div/input[2]').click() # 点击搜索公众号
                time.sleep(3)
            try:
                titles = driver.find_elements_by_tag_name("h3")
                Ids = driver.find_elements_by_tag_name("label")
                for title in titles:
                    if title.text == content:
                        flag = True
                        break
                    n += 1
                if flag == True:
                    Id = Ids[n].text
                    ws.write(count,0,contents_list[count-1])
                    ws.write(count,1,Id)
                    print "成功找到第%d个公众号" % count
                    count += 1
                else:
                    ws.write(count,0,contents_list[count-1])
                    print "查找公众号失败!"
                    count += 1
            except:
                print "查找失败!"
                ws.write(count,0,contents_list[count-1])
                count += 1
        wb.save("Weixin%s.xls" % str(i))
    except:
        wb.save("Weixin%s.xls" % str(i))
    driver.close()
    driver.quit() # 退出浏览器



# 从excel获取公众号名称并储存到列表
def GetWeixinhaoName():
    data = xlrd.open_workbook("F:/Wexin1460.xls")
    table = data.sheets()[0] # 获取sheet1工作表
    ColValues = table.col_values(0)  # 获取第一列的值
    return ColValues # 返回列表

# 将公众号按地区分类
# Lists为公众号名称，省市列表
# Lists[0]为公众号名称，Lists[1]为省名称，Lists[2]为市名称
# 空缺的项(市名称)用0代替填充
def SortArea(Lists):
    StandardLists = GetAreaInfo()  # 得到标准的ID、区、市、省信息，储存为列表形式
    # StandardLists[0]为ID名，StandardLists[1]为区县级名称，StandardLists[2]为市级名称，StandardLists[3]为省级名称
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Area')
    ws.write(0,0,u"公众号名称")
    ws.write(0,1,u"省份")
    ws.write(0,2,u"地市")
    ws.write(0,3,u"注册区县ID")
    ws.write(0,4,u"注册区县")
    ws.write(0,5,u"注册市")
    ws.write(0,6,u"注册省")
    ws.write(0,7,u"受众区县ID")
    ws.write(0,8,u"受众区县")
    ws.write(0,9,u"受众市")
    ws.write(0,10,u"受众省")
    n = 1 # 计数
    for i in range(len(Lists[0])):
        Province = Lists[1][i] #省名称
        Shi = Lists[2][i] # 市名称
        if Shi != "":
            for j in range(len(StandardLists[0])):
                if (StandardLists[3][j] == Province and StandardLists[2][j] == Shi and StandardLists[1][j] == u"市辖区"):
                    ws.write(i+1,0,Lists[0][i])
                    ws.write(i+1,1,Lists[1][i])
                    ws.write(i+1,2,Lists[2][i])
                    ws.write(i+1,3,StandardLists[0][j]) # 注册区县ID
                    ws.write(i+1,4,u"市辖区")
                    ws.write(i+1,5,Shi)
                    ws.write(i+1,6,Province)
                    ws.write(i+1,7,int(StandardLists[0][j])-1) # 受众区域id
                    ws.write(i+1,8,Shi)
                    ws.write(i+1,9,Shi)
                    ws.write(i+1,10,Province)
        else:
            for j in range(len(StandardLists[0])):
                if (StandardLists[1][j] == Province):
                    ws.write(i+1,0,Lists[0][i])
                    ws.write(i+1,1,Lists[1][i])
                    ws.write(i+1,2,Lists[2][i])
                    ws.write(i+1,7,StandardLists[0][j]) # 受众区域id
                    ws.write(i+1,8,Province)
                    ws.write(i+1,9,Province)
                    ws.write(i+1,10,Province)
        print "第%d个公众号查找成功!" % n
        n += 1
    wb.save("Area.xls") # 保存excel

# 获取公众号名称、省市信息
def GetLists():
    Lists = []
    data = xlrd.open_workbook("F:/Wexin1460.xls")
    table = data.sheets()[0] # 获取sheet1工作表
    ID = table.col_values(0)
    ID = ID[1:len(ID)] # ID
    Shen = table.col_values(3)
    Shen = Shen[1:len(Shen)] # 省
    Shi = table.col_values(4)
    Shi = Shi[1:len(Shi)] #市
    Lists.append(ID)
    Lists.append(Shen)
    Lists.append(Shi)
    return Lists

# 获取对比的省市区的标准信息
def GetAreaInfo():
    StandardLists = []
    data = xlrd.open_workbook("F:/Province.xls")
    table = data.sheets()[0] # 获取sheet1工作表
    ID = table.col_values(0)  # 获取第一列的值为ID
    ID = ID[1:len(ID)]
    Qu = table.col_values(1) # 区列
    Qu = Qu[1:len(Qu)]
    Shi = table.col_values(2) # 市列
    Shi = Shi[1:len(Shi)]
    Shen = table.col_values(3) # 省列
    Shen = Shen[1:len(Shen)]
    StandardLists.append(ID)
    StandardLists.append(Qu)
    StandardLists.append(Shi)
    StandardLists.append(Shen)
    return StandardLists













if __name__ == '__main__':
    '''
    ColValues = GetWeixinhaoName() # 公众号名称列表
    n = 1429
    i = 1
    while(n<len(ColValues)):
        print "第%d次任务开始" % i
        GetIdBySelenium(ColValues[n:n+100],i)
        n += 100
        i += 1
        '''
    Lists = GetLists()
    SortArea(Lists)














