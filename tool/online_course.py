"""
selenium 库的学习和使用

请勿用于商业用途，仅作练习之用。

为了能够运行起来：

1. 你需要安装 Chrome 浏览器。
2. 接着还需要下载 Driver，放到一个路径，这个路径在下面的 chrome_driver 变量设置。

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

# ---------------------------------------- 设置选项开始 ----------------------------------------------------

# 课程地址
course_url = 'https://scnuyjs.yuketang.cn/'

# driver 的路径
chrome_driver = 'D:\\driver\\chromedriver.exe'

# chrome 数据存放路径，加入这个之后，就可以避免每次登录都要扫码啦~
chrome_data_dir = 'D:\\driver\\ChromeUserData'

# 要学习的课程号。从主页点击学习空间，进入了之后，有几门课。如果设置为 1，就学习第 1 门课。
course_id = '1'
# ---------------------------------------- 设置选项结束 ----------------------------------------------------


# ---------------------------------------- 元素路径开始 ----------------------------------------------------

# 主页那里的按钮上的文字，如果未登录，那么取值为“登 录”；如果登录，那么取值为“学习空间”
main_page_btn_text_xpath = '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button/span'

# 主页那里的“登录”按钮/“学习空间”按钮
main_page_btn_xpath = '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button'

# 主页的头像
main_page_img_xpath = '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/img'

# 学习空间中的课程按钮
learn_space_course_btn_xpath = '//*[@id="pane-student"]/div/div[' + course_id + ']/div/div/div/div'

# 课程中，成绩单栏目
course_grade_btn_xpath = '//*[@id="app"]/div[2]/div[2]/div[3]/div/ul/li[4]'

# 视频列表的 class 定位器
course_grade_video_list_class = 'clearfix.concrete-tr'

# 视频列表中，是否完成的 class 定位器
video_list_complete_class = 'font14.color9b'

# 视频列表中，是否锁定的 class 定位器
video_list_lock_class = 'el-tooltip.iconfont.icon--suo.color-c8.pointer'

# 视频列表中，视频按钮的 class 定位器
video_list_btn_class = 'cursorpoint.unit-name-hover'

# 视频中完成度
video_rate_xpath = '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[2]/div/section[1]/div[2]/div/div/span'
# ---------------------------------------- 元素路径结束 ----------------------------------------------------


def find_element(driver, method, content, wait=True):
    """
    简单的封装一下。等待元素被加载出来之后，再获取。
    method 需要正确填写，否则会找不到这个元素

    find_elements_by_class_name 允许找不到，这就麻烦了
    """
    while True:
        try:
            get_element = getattr(driver, method)
            res = get_element(content)
            if method != 'find_elements_by_class_name' or len(res) != 0:
                return res
        except selenium.common.exceptions.NoSuchElementException:
            if wait:
                time.sleep(5)
            else:
                return None


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-data-dir=' + chrome_data_dir)
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
driver.get(course_url)

text_of_btn = find_element(driver, 'find_element_by_xpath', main_page_btn_text_xpath).text

# 如果已经登录，那么那个按钮显示的内容是“学习空间”
if text_of_btn != '学习空间':
    while True:
        # 请求登录
        login_btn = find_element(driver, 'find_element_by_xpath', main_page_btn_xpath)
        login_btn.click()

        # 扫码登录，轮询检查头像是否存在，判断是否登录
        img = find_element(driver, 'find_element_by_xpath', main_page_img_xpath, False)
        if img is not None:
            break
        time.sleep(3)

# 找到学习空间并点击
learn_space_btn = find_element(driver, 'find_element_by_xpath', main_page_btn_xpath)
learn_space_btn.click()

# 找到课程按钮并点击
course_btn = find_element(driver, 'find_element_by_xpath', learn_space_course_btn_xpath)
course_btn.click()

# 找到成绩单并点击
grade_btn = find_element(driver, 'find_element_by_xpath', course_grade_btn_xpath)
grade_btn.click()

# 找到视频列表。这里有个 bug，元素选择的方式会选择到后面的作业，不过也没关系啦
video_list = find_element(driver, 'find_elements_by_class_name', course_grade_video_list_class)

# 遍历每个视频，检查是否完成，是否解锁，如果都否，那么开始学习。
for video in video_list:
    # 检查是否已完成
    complete = video.find_elements_by_class_name(video_list_complete_class)
    if len(complete) != 0:
        continue

    # 检查是否已解锁
    lock = video.find_elements_by_class_name(video_list_lock_class)
    if len(lock) != 0:
        continue

    # 开始学习课程
    video_btn = find_element(video, 'find_element_by_class_name', video_list_btn_class)
    print('---------------------------------------------------------')
    print('开始学习课程: ' + video_btn.text)
    video_btn.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    while True:
        rate = find_element(driver, 'find_element_by_xpath', video_rate_xpath).text
        print(rate)
        if rate == '完成度：100%':
            driver.close()
            print('学习完毕！')
            break

        # 休息一下，不要询问的太频繁
        time.sleep(10)
    driver.switch_to.window(handles[0])
    time.sleep(2)

