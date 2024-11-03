import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException


def explicit_click(browser, selector: str):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        browser.find_element(By.CSS_SELECTOR, selector).click()
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        print(e)
        time.sleep(0.1)
        try:
            browser.execute_script(f'document.querySelector("{selector}").click();')
        except Exception as e:
            print("JavaScript execute ERROR too")
            print(e)
            return False
    return False


def explicit_fill(browser, selector: str, text: str, keys=None):
    try:
        # 点击元素
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        browser.find_element(By.CSS_SELECTOR, selector).click()
        # 输入文本
        element = browser.find_element(By.CSS_SELECTOR, selector)
        element.clear()  # 清除之前的文本
        element.send_keys(text)  # 输入新文本
        if keys:
            element.send_keys(keys)
    except (TimeoutException, ElementNotInteractableException) as e:
        print(e)
        time.sleep(0.1)
        try:
            # 使用JavaScript来模拟点击和输入
            browser.execute_script(f"document.querySelector('{selector}').click();")
            browser.execute_script(f"document.querySelector('{selector}').value = '{text}';")
        except Exception as e:
            print("JavaScript execute ERROR too")
            print(e)

browser = webdriver.Chrome()
browser.get("http://cscore.buaa.edu.cn/#/problem?ProblemId=334&PieId=1202")
explicit_click(browser, ".v-btn__content .align-center")

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"iframe#loginIframe")))
browser.switch_to.frame('loginIframe')
time.sleep(1)
explicit_fill(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(1) input", "账号")
time.sleep(1)
explicit_fill(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(3) input", "密码")
time.sleep(1)
explicit_click(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(7) input")
try:
    explicit_click(browser, ".v-btn__content .align-center")
except:
    pass

for i in range(655, 1000):
    browser.get(f"http://cscore.buaa.edu.cn/#/problem?ProblemId={i}&PieId=1202")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".v-card__text")))
    time.sleep(2)
    text = browser.execute_script('return document.querySelector(".v-card__text").innerText')
    print(text)
    print(i)
    if text != "加载中，请稍等...":
        screenshot = browser.get_screenshot_as_png()
        with open(f"1202-{i}题目截屏.png","wb") as file:
            file.write(screenshot)
    time.sleep(5)
time.sleep(10000)
