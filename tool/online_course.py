from selenium import webdriver
import time
import selenium

driver = webdriver.Chrome('D:\\driver\\chromedriver.exe')
driver.get('https://scnuyjs.yuketang.cn/')

# 请求登录
login_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')
login_btn.click()

# 扫码登录，轮询是否登录
learn_space_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')

while True:
    try:
        img = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/img')
        break
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(5)

learn_space_btn.click()

# 选择课程
course_btn = driver.find_element_by_xpath('//*[@id="pane-student"]/div/div[1]/div/div/div')
course_btn.click()

