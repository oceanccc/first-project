# coding = utf8
import requests,pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from pyquery import PyQuery as pq
from pymongo import MongoClient
from time import sleep
 
driver = webdriver.Chrome()
# 设置最大化('/html/body/div[2]/div[3]/div[4]/a/i')
driver.maximize_window()
driver.get('https://www.xin.com/quanguo/')
wait = WebDriverWait(driver,10)
sleep(2)

js="var q=document.documentElement.scrollTop=350"
driver.execute_script(js)
a=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/a')
ActionChains(driver).move_to_element(a).perform()
sleep(1)

b=driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[4]/div/div/dl/dd/a')
b[0].click()


#下一页
def next_page():
    sleep(2)
    js="var q=document.documentElement.scrollTop=3700"
    driver.execute_script(js)
    p=driver.find_elements_by_xpath('//div[@id="search_container"]/div[2]/a')
    goods()
    if p[-1].text == '下一页':
        p[-1].click()
        return next_page()
    else:
        print('本类车型爬取完毕已抓取完毕')
        for i in b:
            driver.find_element_by_xpath('//div[@id="search_search"]').send_keys(i.text)
            driver.find_element_by_xpath('//div[@id="switchCarShop"]/a').click()
            return next_page()

#页面跳转
def goods():
    sy=driver.current_window_handle
    a=driver.find_elements_by_xpath('//div[@id="search_container"]/div[1]/ul/li')
    for i in a:
        i.click()
        a=driver.window_handles
        driver.switch_to.window(a[1])
        sleep(10)
        try:
            get_goods()
        except:
            pass
        driver.close()
        driver.switch_to.window(a[0])
   
#获取页面信息
def get_goods():
    #车型号名称
    xh=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/span')[0].text
    #价格
    price=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/p/span[1]/b')[0].text
    #新车含税价格
    xc_price=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/p/span[2]/span[1]/b')[0].text
    #购车方式及首付月供
    yg=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/span[2]')[0].text
    #车辆核实员
    hsy=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/a/span[2]/span[1]')[0].text
    #上架时间
    sjsj=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/a/span[2]/span[2]')[0].text
    #上牌时间
    spsj=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[1]/span[2]')[0].text
    #车辆年限
    clnx=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[1]/span[1]')[0].text
    #表显里程
    lc=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[2]/a')[0].text
    #排放标准
    pfbz=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[3]/span[1]')[0].text
    #排量
    pl=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[4]/span[1]')[0].text
    #所在城市
    city=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/ul/li[5]/span[1]')[0].text
    #使用性质
    syxz=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[1]/dd[3]/span[2]')[0].text
    #年检到期时间
    nj_time=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[1]/dd[4]/span[2]')[0].text
    #保险到期时间
    dq_time=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[1]/dd[5]/span[2]')[0].text
    #保养情况
    by=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[1]/dd[6]/span[2]')[0].text
    #车辆厂商
    cs=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[1]/span[2]/a')[0].text
    #车辆级别
    jb=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[2]/span[2]/a')[0].text
    #车辆颜色
    color=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[3]/span[2]/a')[0].text
    #车身结构
    jg=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[4]/span[2]/a')[0].text
    #整备质量
    zl=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[5]/span[2]')[0].text
    #轴距
    zj=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[2]/dd[6]/span[2]')[0].text
    #发动机
    fdj=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[3]/dd[1]/span[2]')[0].text
    #变速器
    bsq=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[3]/dd[2]/span[2]/a')[0].text
    #燃油类型
    rylx=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[3]/dd[4]/span[2]')[0].text
    #驱动方式
    qdfs=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[3]/dd[5]/span[2]')[0].text
    #综合油耗
    yh=driver.find_elements_by_xpath('//div[@id="cd_m_clxx"]/div[3]/dl[3]/dd[6]/span[2]')[0].text
    #图片
    pictor=driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[1]/img')[0].get_attribute('src')
    
    print('车型号名称：'+xh)
    print('价格：'+price)
    print('新车含税价格：'+xc_price)
    print('购车方式及首付月供：'+yg)
    print('车辆核实员：'+hsy)
    print('上架时间：'+sjsj)
    print('上牌时间：'+spsj)
    print('车辆年限：'+clnx)
    print('表显里程：'+lc)
    print('排放标准：'+pfbz)
    print('排量：'+pl)
    print('所在城市：'+city)
    print('使用性质：'+syxz)
    print('年检到期时间：'+nj_time)
    print('保险到期时间：'+dq_time)
    print('保养情况：'+by)
    print('车辆厂商：'+cs)
    print('车辆级别：'+jb)
    print('车辆颜色：'+color)
    print('车身结构：'+jg)
    print('整备质量：'+zl)
    print('轴距：'+zj)
    print('发动机：'+fdj)
    print('变速器：'+bsq)
    print('燃油类型：'+rylx)
    print('驱动方式：'+qdfs)
    print('综合油耗：'+yh)
    print('图片：'+pictor)
    print('==============================================================================')

next_page()
    










