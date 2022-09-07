# !pip install webdriver-manager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from captcha_solver import CaptchaSolver, CaptchaSolverError
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium import webdriver
import datetime
import time
import os


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

# Load .env
load_dotenv('.env')

invalid_login = True
while invalid_login:
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    driver.get('https://www.ckgsir.com/my-account')

    # Fill My Account form
    webReference = driver.find_element(By.NAME, 'webReference')
    webReference.send_keys(os.getenv("WEB_REFERENCE"))

    # Date
    dateOfBirth_element = driver.find_element(By.NAME, "dateOfBirth")
    dateOfBirth_element.click()

    ui_datepicker_month_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-month")
    ui_datepicker_month_element.click()
    month_element = driver.find_element(By.XPATH, f"//*[@id='ui-datepicker-div']/div/div/select[1]/option[{MONTH['Jun']}]")
    month_element.click()

    ui_datepicker_year_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-year")
    ui_datepicker_year_element.click()
    year_element = driver.find_element(By.CSS_SELECTOR, "option[value = '1993']")
    year_element.click()

    day_element = driver.find_element(By.LINK_TEXT, f"{27}")
    day_element.click()
    passportNo = driver.find_element(By.NAME, "passportNo")
    passportNo.send_keys(os.getenv("PASSPORT_NO"))

    cookieOk = driver.find_element(By.ID, 'cookieOk')
    cookieOk.click()

    captcha_element = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
    captcha_element.screenshot(f".{os.sep}static{os.sep}img.png")
    try:
        solver = CaptchaSolver('2captcha', api_key=os.getenv("CAPTCHA_API_KEY"))
        raw_data = open(f'static{os.sep}img.png', 'rb').read()
        captcha_text = solver.solve_captcha(raw_data)
        captchaCode = driver.find_element(By.NAME, "captchaCode")
        captchaCode.send_keys(captcha_text)
    except CaptchaSolverError:
        print("Balance Too Low!! \nCaptcha does not solved!!")

    # Button login
    submitButton = driver.find_elements(By.ID, "SubmitButton")
    if submitButton:
        submitButton[0].click()
    else:
        pass

    # Check login process valid
    invalid_login_element = driver.find_elements(By.LINK_TEXT, "Invalid Captcha.")
    if invalid_login_element:
        continue
    else:
        break

# Vis Application popup
confirm_yes_element = driver.find_elements(By.ID, "confirm-yes")
if confirm_yes_element:
    confirm_yes_element[0].click()
else:
    pass
# Cancel Re-schedule Note
mfp_close_element = driver.find_elements(By.CLASS_NAME, "mfp-close")
if mfp_close_element:
    mfp_close_element[0].click()
else:
    pass
visa_app = True
while visa_app:
    date_picker_elements = driver.find_elements(By.CLASS_NAME, "datepicker-days")
    if date_picker_elements:
        date_picker1_available = date_picker_elements[0].find_elements(By.CLASS_NAME, 'regular-day-info')
        date_picker2_available = date_picker_elements[1].find_elements(By.CLASS_NAME, 'regular-day-info')
        if len(date_picker1_available):
            date_picker1_available[0].click()
        elif len(date_picker2_available):
            date_picker2_available[0].click()
        else:
            print(f"{datetime.datetime.now()}:\tAppointment Not Available!!")
        time.sleep(30)
    else:
        continue
driver.close()
