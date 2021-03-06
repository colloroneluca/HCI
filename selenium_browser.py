import json
import threading
import pyperclip
import selenium
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from playsound import playsound
import speech_recognition as sr
from datetime import datetime
from utilities import start_sound, start_micro, thread_with_exception
class Selenium_Browser():
    def __init__(self):
        self.browser = None
        self.i=2
        pass

    def launch_browser(self):
        self.browser = webdriver.Chrome('chromedriver_linux64_Luca/chromedriver') #Luca = 'chromedriver_linux64_Luca/chromedriver'

        self.browser.maximize_window()
        self.browser.get("https://www.google.com/")

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

    def switch_to_tab(self,direction, closing=False):
        if closing:
            print(self.browser.window_handles)
            self.browser.switch_to.window(self.browser.window_handles[-1])
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

    def check_input_cell(self, obj):
        gesture_help_thread = None
        input_cells = self.browser.find_elements_by_xpath('//input[@type="text" or @type="password"] | //textarea')
        active_element = self.browser.switch_to.active_element
        if self.browser.switch_to.active_element in input_cells:
            self.browser.switch_to.active_element.clear()
            # start speech recognizer
            speech= self.get_speech(obj)

            active_element.send_keys(speech)

        return gesture_help_thread

    def get_speech(self, obj):
        lista = []
        r = sr.Recognizer()
        obj.destroyed = True
        del(obj)
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            start_sound('start_speech.mp3', 1.3)
            f = open("thread_control.txt", "w")
            f.write("0")
            f.close()
            x = threading.Thread(target=start_micro, args=(lista,))
            x.start()
            dest = None
            while dest == None:
                audio = r.listen(source)
                try:
                    dest = r.recognize_google(audio)
                    print("You have said : " + dest)
                except Exception as e:
                    print("Error : " + str(e))
                    dest = None
            f = open("thread_control.txt", "w")
            f.write("1")
            f.close()
            start_sound('close_speech.mp3', 1.3)


        return dest

    def get_browser_screenshot(self):
        current_date_time = ".".join(datetime.now().strftime("%Y-%m-%d %H-%M-%S").split(" "))
        screenshot_name = "BrowserScreenshot/screenshot." + current_date_time + ".png"
        self.browser.save_screenshot(screenshot_name)
        print("{} saved!!!".format(screenshot_name))

    def get_html(self, url):
        self.browser.get("https://en.wikipedia.org")
        html = self.browser.page_source
        print(html)

    def do_stuff(self):
        time.sleep(5)
        self.browser.get("https://facebook.com")
        time.sleep(5)

    def save_user_tabs(self, user):
        tabs_num = len(self.browser.window_handles)
        tabs = []
        open_tabs = user['tabs']
        for x in range(tabs_num):
            self.browser.switch_to.window(self.browser.window_handles[x])
            if self.browser.current_url != "data:," and self.browser.current_url != 'https://www.google.com/' and self.browser.current_url != 'https://github.com/'  :
                tabs.append(self.browser.current_url)

        with open('users.json', 'r+') as f:
            users = json.load(f)

        for x in users:
            if user["id"] == x["id"]:
                users[users.index(x)]["tabs"] = tabs

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, separators=(',', ': '))

    def get_user_tabs(self, user):
        found = False
        for tab in user["tabs"]:
            if tab == 'https://github.com/':
                found = True
        if not found:
            self.open_tab('https://github.com/')

        for tab in user["tabs"]:
            if tab != "https://www.google.com/" or tab!='https://github.com/':
                self.open_tab(tab)


if __name__ == "__main__":
    b = Selenium_Browser()
    b.launch_browser()
    b.get_resorce('https://www.google.com/')
    b.open_tab('https://www.google.com/')
    print("tab", b.get_current_tab())
    time.sleep(3)
    b.switch_to_tab("right2left")
    b.script()
