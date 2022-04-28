import selenium
from selenium import webdriver
import time


class Selenium_Browser():
    def __init__(self):
        self.browser = None
        pass

    def launch_browser(self):
        self.browser = webdriver.Chrome('./chromedriver_linux64_Luca/chromedriver')

    def get_resorce(self, url):
        self.browser.get(url)

    def open_tab(self, url=None):
        self.browser.execute_script("window.open('');")
        self.browser.switch_to.window(self.browser.window_handles[-1])
        if url != None:
            self.browser.get(url)

    def get_current_tab(self):

        current_tab = self.browser.current_window_handle

        tabs = self.browser.window_handles

        index = tabs.index(current_tab)

        return index

    def switch_to_tab(self,direction):
        current_tab = self.get_current_tab()
        if direction == 'left2right':

            try:
                self.browser.switch_to.window(self.browser.window_handles[current_tab+1])
            except:
                pass
        elif direction == 'right2left':
            try:
                self.browser.switch_to.window(self.browser.window_handles[current_tab-1])
            except:
                pass





    def do_stuff(self):
        time.sleep(5)
        self.browser.get("https://facebook.com")
        time.sleep(5)

if __name__ == "__main__":
    b = Selenium_Browser()
    b.launch_browser()
    b.get_resorce('https://www.google.com/')
    b.open_tab('https://www.google.com/')
    print("tab", b.get_current_tab())
    time.sleep(3)
    b.switch_to_tab("right2left")