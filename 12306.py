import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Qiangpiao(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='G:\Google\Chrome\Application\chromedriver.exe')
        # 登录界面 输入账号密码，
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        # 登录成功页面
        self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
        # 查找车次的页面 输入出发地 目的地 出发日
        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init?"
        # 乘客信息的页面
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"


    def wait_input(self):
        self.from_station = input('出发站:')
        self.to_station = input('目的地:')
        # 时间格式必须是：yyyy-MM-dd的方式
        self.depart_time = input('出发时间:')
        # 如果有多个乘客，需要使用英文“，”来隔开
        self.passengers = input('乘客姓名:').split(",")
        self.trains = input('车次:').strip(',')

    # 实现登录的操作
    def _login(self):
        self.driver.get(url=self.login_url)
        # 显示等待
        # 隐式等待 直到转到此网址
        WebDriverWait(self.driver,1000).until(
            EC.url_to_be(self.initmy_url)
        )
        print("登录成功")

    # 订票的函数
    def _order_ticket(self):
        # 1.跳转到查余票的界面
        self.driver.get(self.search_url)
        # 2.等待出发地是否输入正确
        WebDriverWait(self.driver,1000).until(
            # 文本呈现在这个值当中
            EC.text_to_be_present_in_element_value((By.ID,"fromStationText"),self.from_station)
        )
        # 3.等待目的地是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"toStationText"),self.to_station)
        )
        # 4.等待出发日期是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"train_date"),self.depart_time)
        )
        # 5.等待查询按钮是否可用
        WebDriverWait(self.driver,1000).until(
            EC.element_to_be_clickable((By.ID,'query_ticket'))
        )
        # 6.如果能够被点击了，那么久找到这个查询按钮，执行点击事件
        searchBtn = self.driver.find_element_by_id("query_ticket")
        searchBtn.click()

        # 7.在点击了查询按钮以后，等待车次信息是否显示出来了
        WebDriverWait(self.driver,1000).until(
            EC.presence_of_all_elements_located((By.XPATH,".//tbody[@id='queryLeftTable']/tr"))
        )

        # 8.找到所有没有datatrain属性的tr标签，这些标签是存储了车次信息
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")

        for tr in tr_list:
            train_number = tr.find_element_by_class_name('number').text
            # print(train_number)
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[8]").text
                if left_ticket == "有" or left_ticket.isdigit:
                    # print('有票')
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()

                    # 等待是否来到了确认乘客的页面
                    WebDriverWait(self.driver,1000).until(
                        EC.url_to_be(self.passenger_url)
                    )
                    WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.XPATH,'.//ul[@id = "normal_passenger_id"]/li'))
                    )
                    # 9.找到所有常用联系人
                    passanger_labels = self.driver.find_elements_by_xpath('.//ul[@id="normal_passenger_id"]/li/label')

                    for passanger_label in passanger_labels:
                        name = passanger_label.text
                        if name in self.passengers:
                            passanger_label.click()

                            # 获取提交订单的按钮
                            submitBotton = self.driver.find_element_by_id('submitOrder_id')
                            submitBotton.click()
                            # 显示等待确人订单对话框是否出现
                            WebDriverWait(self.driver, 1000).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'dhtmlx_wins_body_outer')))
                            # # 显示等待确认按钮是否加载出现，出现后执行点击操作
                            WebDriverWait(self.driver, 1000).until(
                                EC.presence_of_element_located((By.ID, 'qr_submit_id')))
                            ConBotton = self.driver.find_element_by_id('qr_submit_id')
                            ConBotton.click()
                            while ConBotton:
                                ConBotton.click()
                                ConBotton = self.driver.find_element_by_id('qr_submit_id')
                            return

    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()

if __name__ == '__main__':
    spider = Qiangpiao()
    spider.run()