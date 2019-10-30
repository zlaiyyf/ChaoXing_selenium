# coding:utf-8
from selenium import webdriver
# 显示等待
from selenium.webdriver.support.wait import WebDriverWait
# 启动参数
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException,TimeoutException
from scrip import click
import time

class Chaoxing():


    def __init__(self,password,username):
        """
        暂时不考虑其他学校的

        :param password:
        :param username:
        """

        chrome_opt =  Options()  # 创建参数设置对象.
        # chrome_opt.add_argument('–start-maximized')  # 设置浏览器窗口大小.

        chrome_opt.add_argument('--disable-infobars')
        # chrome_opt.add_argument("-–start-maximized")

        chrome_opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(chrome_options=chrome_opt)
        self.username = username
        self.password = password


    def land(self):
        """
        登陆
        :return:
        """

        self.browser.get('http://sxu.fanya.chaoxing.com/portal')
        # self.browser.find_element_by_xpath('//input[@value= "登录"]').click()
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_xpath('//input[@value= "登录"]')).click()
        # ActionChains(driver).click(click_btn)
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_xpath('//input[@id="unameId"]')).send_keys(self.username)
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_xpath('//input[@id="passwordId"]')).send_keys(self.password)
        print('输入账号完成{}'.format(self.username))
        time.sleep(10)

        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_xpath('//input[@value= "登录"]')).click()



    def find_course(self):
        """
        发现课程
        :return:
        """
        self.browser.switch_to.frame('frame_content')
        self.browser.find_elements_by_xpath('//li[@style="position:relative"]')
        course_name = self.browser.find_elements_by_xpath('//h3[@class="clearfix"]')
        click.click_couse(course_name,'创业创新领导力')

        windows = self.browser.window_handles
        self.browser.switch_to.window(windows[-1])
        self.couse()
    def couse(self):
        """
        进入课程
        :return:
        """
        class_num = -1
        while True:

            time.sleep(2)
            class_num = class_num + 1
            class_name_list = self.browser.find_elements_by_xpath('//div[@class="leveltwo"]')
            if class_num == len(class_name_list):
                break
            else:
                print(class_num)
                class_name_num = self.browser.find_elements_by_xpath('//div[@class="leveltwo"]')[class_num].text
                print(class_name_num.split('\n'))
                if '1' == class_name_num.split('\n')[1]:
                    continue
                class_name_tag = self.browser.find_elements_by_xpath('//span[@class="articlename"]')[class_num]
                class_name = class_name_tag.text
                class_name_tag.click()

                print('正在点击{}'.format(class_name))

                time.sleep(2)
                self.view(class_name=class_name)
                continue
    def view(self,class_name):
        """
        看视频
        :param class_name:
        :return:
        """
        # try:
        self.browser.find_element_by_xpath('//span[@title="视频"]').click()
        self.browser.switch_to.frame("iframe")
        time.sleep(5)
        self.browser.switch_to.frame(self.browser.find_element_by_xpath('//iframe[@class="ans-attach-online ans-insertvideo-online"]'))
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_xpath('//div[@id="video"]')).click()


        view_tag = self.browser.find_element_by_xpath('//div[@id="video"]')
        ActionChains(self.browser).move_to_element(view_tag).perform()
        while   True:
            time.sleep(2)

            if self.view_percentage() == '200' :
                self.browser.switch_to.default_content()
                self.browser.find_element_by_xpath('//a[contains(text(), "回到课程")]').click()
                break


    def view_percentage(self):
        """"
                  检查是否看完
        """
        # total_duration = self.browser.find_element_by_xpath('//span[@class="vjs-duration-display"]').text
        # current_duration = self.browser.find_element_by_xpath('//span[@class="vjs-current-time-display"]').text
        view_percentage_tag = self.browser.find_element_by_xpath('//div[@class="vjs-play-progress vjs-slider-bar"]')
        view_percentage = view_percentage_tag.get_attribute('style')
        print('当前进度'+view_percentage)
        self.is_exist_problem()
        """"
        检查是否看完
        """
        if '100%' in view_percentage :
            return '200'

    def is_exist_problem(self):
        try:
            problem_tag_style = WebDriverWait(self.browser, 30, 0.2).until(
                lambda x: x.find_element_by_xpath('//div[@id="ext-comp-1035"]')).get_attribute('style')

            if problem_tag_style == 'overflow: auto;':
                print('有题目')
                input_tag_list = self.browser.find_elements_by_xpath('//input')
                for input_tag in input_tag_list:
                    input_tag.click()
                    self.browser.find_element_by_xpath('//div[@class="ans-videoquiz-submit"]').click()
                    time.sleep(2)
                    if EC.alert_is_present()(self.browser):
                        self.browser.switch_to.alert.accept()
                    else:
                        break
            else:
                pass
        except UnexpectedAlertPresentException:
            print('alert出错')
            self.browser.switch_to.alert.accept()
        except TimeoutException:
            print('TimeoutException')
            pass

if __name__ == '__main__':
    cx = Chaoxing('','')#密码账号
    cx.land()
    cx.find_course()

