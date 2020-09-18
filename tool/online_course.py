"""
selenium 库的学习和使用

请勿用于商业用途，仅作练习之用。
"""

from selenium import webdriver
import time
import selenium
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()

# 设置用户文件夹，可免登陆
chrome_options.add_argument('--user-data-dir=D:\\driver\\ChromeUserData')
chrome_options.add_argument('--disable-popup-blocking')

# driver 的路径
chrome_driver = 'D:\\driver\\chromedriver.exe'

driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
driver.get('your-link')

time.sleep(5)
text_of_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button/span').text

if text_of_btn != '学习空间':
    # 请求登录
    login_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')
    login_btn.click()

    # 扫码登录，轮询检查头像是否存在，判断是否登录
    while True:
        try:
            img = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/img')
            break
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(5)

learn_space_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')
learn_space_btn.click()

# 等待页面加载出来，否则会找不到元素
while True:
    try:
        # 选择课程，选择第二个课程，手动修改下面的数字吧。
        course_btn = driver.find_element_by_xpath('//*[@id="pane-student"]/div/div[2]/div/div/div/div')
        course_btn.click()

        # 选择成绩单
        grade_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/ul/li[4]')
        grade_btn.click()
        break
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(5)


# 等待页面加载出来，否则会找不到元素
while True:
    # 需要看的列表
    time.sleep(10)
    video_list = driver.find_elements_by_class_name('clearfix.concrete-tr')
    for video in video_list:
        # 检查是否已完成
        complete = video.find_elements_by_class_name('font14.color9b')
        if len(complete) != 0:
            continue

        # 检查是否已解锁
        lock = video.find_elements_by_class_name('el-tooltip.iconfont.icon--suo.color-c8.pointer')
        if len(lock) != 0:
            continue

        # 开始学习课程
        video_btn = video.find_element_by_class_name('cursorpoint.unit-name-hover')
        print('---------------------------------------------------------')
        print('开始学习课程: ' + video_btn.text)
        video_btn.click()
        time.sleep(10)
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        while True:
            # 需要先看一段之后，才会出现进度
            time.sleep(60)
            rate = driver.find_element_by_xpath(
                '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[2]/div/section[1]/div[2]/div/div/span').text
            print(rate)
            if rate == '完成度：100%':
                driver.close()
                print('学习完毕！')
                break
        driver.switch_to.window(handles[0])
    break

