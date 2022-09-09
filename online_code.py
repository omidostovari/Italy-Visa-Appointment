# !pip install webdriver-manager
# !pip install win10toast
# !pip install playsound
# !pip install captcha_solver
# !pip install selenium
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from captcha_solver import CaptchaSolver, CaptchaSolverError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier # For show windows notification
from playsound import playsound
from dotenv import load_dotenv
from selenium import webdriver
import datetime
import time
import os

# Load .env
load_dotenv('.env')

MONTH = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}
DAY = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
)
USER_MONTH_BIRTH = 'Jun'
USER_YEAR_BIRTH = '1993'
USER_DAY_BIRTH = "27"

USER_PRIORITY = {
    "first":  [13, 14, 15],
    "second": [18, 19, 20],
    "third":  [20, 21, 22],
    "fourth": [11, 12]
}

# Cancel Re-schedule Note
def mfp_close(driver):
    mfp_close_element = driver.find_elements(By.CLASS_NAME, "mfp-close")
    if len(mfp_close_element):
        mfp_close_element[0].click()
    else:
        pass
time_out = True
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
while time_out:
    try:
        driver.get('https://www.ckgsir.com/my-account')
    except:
        time.sleep(13)
        # driver.refresh()
        continue
    break


invalid_login = True
while invalid_login:
    driver.implicitly_wait(5)
    # Fill My Account form
    webReference = driver.find_element(By.NAME, 'webReference')  # TODO NoSuchElementException  Error
    webReference.send_keys(os.getenv("WEB_REFERENCE"))

    # Date
    try:
        dateOfBirth_element = driver.find_element(By.NAME, "dateOfBirth")
        dateOfBirth_element.click()
    except:
        continue
    ui_datepicker_month_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-month")
    ui_datepicker_month_element.click()
    month_element = driver.find_element(By.XPATH, f"//*[@id='ui-datepicker-div']/div/div/select[1]/option[{MONTH[USER_MONTH_BIRTH]}]")
    month_element.click()

    ui_datepicker_year_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-year")
    ui_datepicker_year_element.click()
    year_element = driver.find_element(By.CSS_SELECTOR, f"option[value = '{USER_YEAR_BIRTH}']")
    year_element.click()

    day_element = driver.find_element(By.LINK_TEXT, f"{USER_DAY_BIRTH}")
    day_element.click()
    passportNo = driver.find_element(By.NAME, "passportNo")
    passportNo.send_keys(os.getenv("PASSPORT_NO"))

    cookieOk = driver.find_elements(By.ID, 'cookieOk')
    if len(cookieOk):
        cookieOk[0].click()
    else:
        pass
    captcha_element = driver.find_elements(By.ID, "LoginCaptcha_CaptchaImage")
    if len(captcha_element):
        captcha_element[0].screenshot(f".{os.sep}static{os.sep}{driver.session_id}.png")
        pass
    else:
        print("Captcha not loaded !!")
        while True:
            loading_captcha = driver.find_elements(By.CLASS_NAME,"BDC-ProgressIndicator")
            if len(loading_captcha)<1:
                break
            else:
                time.sleep(5)
                continue

    try:
        solver = CaptchaSolver('2captcha', api_key=os.getenv("CAPTCHA_API_KEY"))
        raw_data = open(f'static{os.sep}{driver.session_id}.png', 'rb').read()
        captcha_text = solver.solve_captcha(raw_data)
        captchaCode = driver.find_element(By.NAME, "captchaCode")
        captchaCode.send_keys(captcha_text)

    except CaptchaSolverError:
        print("Balance Too Low!! \nCaptcha does not solved!!")

    # Button login
    submitButton = driver.find_elements(By.ID, "SubmitButton")
    submitButton[0].click()

    # Check login process valid
    invalid_login_element = driver.find_elements(By.CLASS_NAME, "alignc")
    if len(invalid_login_element):
        print("invalid login!!")
        captcha_Reload = driver.find_element(By.ID,"LoginCaptcha_ReloadIcon")
        captcha_Reload.click()
        continue
    else:
        break

driver.get('https://www.ckgsir.com/book-appointment')
# Vis Application popup
try:

    confirm_yes_element = driver.find_elements(By.ID, "confirm-yes")
    if len(confirm_yes_element):
        confirm_yes_element[0].click()
    else:
        pass
except:
    pass

# Cancel Re-schedule Note
mfp_close(driver)

notifier = ToastNotifier()
visa_app = True
while visa_app:
    date_picker_elements = driver.find_elements(By.CLASS_NAME, "datepicker-days")
    if date_picker_elements:
        date_picker1_available = date_picker_elements[0].find_elements(By.CLASS_NAME, 'regular')
        date_picker2_available = date_picker_elements[1].find_elements(By.CLASS_NAME, 'regular')
        if len(date_picker1_available):
            date_picker1_available[0].click()
            playsound(f".{os.sep}static{os.sep}Successfull-sound.mp3")
            notifier.show_toast(f"-_-_-_-_-_-_-_-\nAvailable!!-_\n-_-_-_-_-_-_-_")
        elif len(date_picker2_available):
            date_picker2_available[0].click()
            playsound(f".{os.sep}static{os.sep}Successfull-sound.mp3")
            notifier.show_toast(f"-_-_-_-_-_-_-_-\nAvailable!!-_\n-_-_-_-_-_-_-_")
        else:
            print("Not available!!")
            time.sleep(30)
            driver.refresh()
            mfp_close(driver)
            continue
        time.sleep(30)
        driver.refresh()
    else:
        time.sleep(30)
        driver.refresh()
        mfp_close(driver)
        continue
driver.close()
#%%
