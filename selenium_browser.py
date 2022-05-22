import pyperclip
import selenium
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from playsound import playsound
import speech_recognition as sr
from datetime import datetime

class Selenium_Browser():
    def __init__(self):
        self.browser = None
        pass

    def launch_browser(self):
        self.browser = webdriver.Chrome('chromedriver_linux64_Luca/chromedriver') #Luca = 'chromedriver_linux64_Luca/chromedriver'
        self.browser.maximize_window()

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

    # Non utilizzata per ora
    def get_active_tab_url(self):
        pyautogui.press('f6')
        pyautogui.hotkey('ctrl', 'c')
        url = pyperclip.paste()
        return url

    def check_input_cell(self):
        input_cells = self.browser.find_elements_by_xpath('//input[@type="text" or @type="password"] | //textarea')

        if self.browser.switch_to.active_element in input_cells:
            self.browser.switch_to.active_element.send_keys("")
            # start speech recognizer
            speech = self.get_speech()
            self.browser.switch_to.active_element.send_keys(speech)
        return

    def get_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            playsound('./1.mpeg')
            audio = r.listen(source)
            playsound('./2.mpeg')
            try:
                dest = r.recognize_google(audio)
                print("You have said : " + dest)
            except Exception as e:
                print("Error : " + str(e))
                dest = None
        return dest

    def get_browser_screenshot(self):
        current_date_time = ".".join(datetime.now().strftime("%Y-%m-%d %H-%M-%S").split(" "))
        screenshot_name = "BrowserScreenshot/screenshot." + current_date_time + ".png"
        self.browser.save_screenshot(screenshot_name)
        print("{} saved!!!".format(screenshot_name))

    def script(self):
        """js = 'alert("Hello World")'
        x = open('keyboard/index.js').read()
        self.browser.execute_script(x)"""
        pass

    def get_html(self, url):
        self.browser.get("https://en.wikipedia.org")
        html = self.browser.page_source
        print(html)

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
    b.script()
