"""
selenium 库的学习和使用

请勿用于商业用途，仅作练习之用。

为了能够运行起来：

1. 你需要安装 Chrome 浏览器。
2. 接着还需要下载 Driver，放到一个路径，这个路径在下面的 chrome_driver 变量设置。
3. 手动修改代码第 66 行，选择课程。（我太菜了...

Driver 下载地址：https://chromedriver.chromium.org/

代码写的比较渣，如果运行不了，你可以尝试运行多几次。

已知的几个问题：
1. 登录之后，没有跳转
2. 进入到课程里面，之后没反应了。

遇到上面的问题，重新运行就好了。

出现这几个 Bug 的主要原因是，网页需要时间加载出来。如果我在加载之前就去选择元素，那么是选择不到的。
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
driver.get('https://scnuyjs.yuketang.cn/')

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
time.sleep(5)

# 等待页面加载出来，否则会找不到元素
while True:
    try:
        # 选择课程，选择第一个课程，手动修改下面的数字吧。这个数字从 1 开始，1 对应第一门课。
        course_btn = driver.find_element_by_xpath('//*[@id="pane-student"]/div/div[1]/div/div/div/div')
        course_btn.click()

        time.sleep(5)

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

