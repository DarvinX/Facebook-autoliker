from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

import pickle
from time import sleep
from os import getcwd

class Bot:

    def __init__(self,driverPath=getcwd()+"/webdriver/geckodriver", headless=True, debug=False):
        self.driverPath = driverPath
        self.debug = debug
        self.headless = headless
        print(headless)
        self.url = "https://www.facebook.com"

        #start up
        self.launch()


    def launch(self):
        #custom useragent for fetching mobile version of facebook
        userAgent = "Mozilla/5.0 (Linux; Android 4.2.1; en-us;\
                Nexus 5 Build/JOP40D) AppleWebKit/535.19 (\
                KHTML, like Gecko) Chrome/18.0.1025.166 \
                Mobile Safari/535.19"

        # set options for mobile view
        options = Options()
        options.set_capability("deviceName", "iPhone")
        options.set_preference("general.useragent.override",
                               userAgent)
        # open window only for debugging
        print(self.headless)
        if self.headless:
            self.msg("headless mode")
            options.add_argument('-headless')

        # launch the browser
        #TODO: Add support for other browsers
        self.driver = Firefox(
            executable_path=self.driverPath,
            options=options)
        self.wait = WebDriverWait(self.driver, timeout=100)
        self.msg("initiated")
        self.driver.get(self.url)
        self.msg("opening site "+str(self.url))

    def msg(self, text):
        if self.debug:
            print(text)

    def waitFor(self, path, by=By.XPATH):
        return self.wait.until(
            expected.visibility_of_element_located((by, path))
        )

    def click(self, path, by=By.XPATH):
        sleep(2)
        self.waitFor(path, by).click()

    def sendKeys(self, path, key, by=By.XPATH):
        sleep(2)
        self.waitFor(path, by).send_keys(key)

    def scrollDown(self, steps=1):
        sleep(2)
        for i in range(0, steps):
            self.buttonpress(Keys.PAGE_DOWN)

    def buttonpress(self, key):
        self.sendKeys('/html/body', key)

    def login(self, username, password):
        self.msg("logging in..")
        self.sendKeys('//*[@id="m_login_email"]', username)
        self.sendKeys('//*[@id="m_login_password"]', password + Keys.ENTER)
        self.click(
            '/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[3]/div[2]/form/div')
        self.msg("logged in")

    def openpage(self, url):
        self.driver.get(url)

    def reload(self):
        self.driver.get(self.url)
        self.msg("page reloading "+self.url)
        
    def quit(self):
        self.msg("quiting window")
        self.driver.quit()