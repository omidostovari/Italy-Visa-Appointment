# !pip install webdriver-manager
# !pip install win10toast
# !pip install playsound
# !pip install captcha_solver
# !pip install selenium
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from captcha_solver import CaptchaSolver, CaptchaSolverError
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from win10toast import ToastNotifier  # For show windows notification
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
WEB_REFERENCE = f'{os.getenv("WEB_REFERENCE")}'
USER_MONTH_BIRTH = f'{os.getenv("USER_MONTH_BIRTH")}'
USER_YEAR_BIRTH = f'{os.getenv("USER_YEAR_BIRTH")}'
USER_DAY_BIRTH = f'{os.getenv("USER_DAY_BIRTH")}'
PASSPORT_NO = f'{os.getenv("PASSPORT_NO")}'

USER_PRIORITY = {
    "first": [13, 14, 15],
    "second": [18, 19, 20],
    "third": [20, 21, 22],
    "fourth": [11, 12]
}


# Cancel Re-schedule Note
def mfp_close(driver):
    mfp_close_element = driver.find_element(By.CLASS_NAME, "mfp-close")
    driver.implicitly_wait(5)
    mfp_close_element.click()
driver = uc.Chrome(use_subprocess=True)
# driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
while True:
    try:
        driver.get('https://www.ckgsir.com/my-account')
        driver.implicitly_wait(60)
    except:
        driver.refresh()
        continue
    else:
        break
playsound(f"static{os.sep}Successfull-sound.mp3")
invalid_login = True
while invalid_login:

    try:
        """ Try to fill My Account form !"""

        # Fill webReference
        webReference = driver.find_element(By.NAME, 'webReference')
        driver.implicitly_wait(5)
        webReference.send_keys(WEB_REFERENCE)

        # Fill date if birthday
        # Click on date of birth element
        dateOfBirth_element = driver.find_element(By.NAME, "dateOfBirth")
        driver.implicitly_wait(5)
        dateOfBirth_element.click()

        # Fill month user birthday
        month_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-month") # TODO WebDriverException
        driver.implicitly_wait(5)
        month_element.click()
        month_element_input = driver.find_element(
            By.XPATH,
            f"//*[@id='ui-datepicker-div']/div/div/select[1]/option[{MONTH[USER_MONTH_BIRTH]}]"
        )
        driver.implicitly_wait(10)
        month_element_input.click()

        # Fill year user birthday
        year_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-year")
        driver.implicitly_wait(5)
        year_element.click()
        year_element_input = driver.find_element(By.CSS_SELECTOR, f"option[value = '{USER_YEAR_BIRTH}']")
        driver.implicitly_wait(5)
        year_element_input.click()

        # Fill day user birthday
        day_element_input = driver.find_element(By.LINK_TEXT, f"{USER_DAY_BIRTH}")
        driver.implicitly_wait(5)
        day_element_input.click()

        # Fill passportNo user birthday
        passportNo = driver.find_element(By.NAME, "passportNo")
        driver.implicitly_wait(5)
        passportNo.send_keys(PASSPORT_NO)

        # Close cookie for screenshot as captcha code
        cookieOk = driver.find_element(By.ID, 'cookieOk')
        driver.implicitly_wait(10)
        cookieOk.click()

        captcha_element = driver.find_element(By.ID, "LoginCaptcha_CaptchaImage")
        driver.implicitly_wait(5)
        captcha_element.screenshot(f".{os.sep}static{os.sep}{driver.session_id}.png")

        # Captcha solver
        solver = CaptchaSolver('2captcha', api_key=os.getenv("CAPTCHA_API_KEY"))
        raw_data = open(f'static{os.sep}{driver.session_id}.png', 'rb').read()
        captcha_text = solver.solve_captcha(raw_data)
        print(captcha_text)
        captchaCode = driver.find_element(By.NAME, "captchaCode")
        driver.implicitly_wait(5)
        captchaCode.send_keys(captcha_text)

        # Button login
        submitButton = driver.find_element(By.ID, "SubmitButton")
        driver.implicitly_wait(10)
        submitButton.click()
        # Check login process valid
        invalid_login_element = driver.find_elements(By.CLASS_NAME, "alignc")
        if len(invalid_login_element):
            print("invalid login!!")
            driver.refresh()
            continue

        # Check login process valid
    except CaptchaSolverError as cs:
        print(f"CaptchaSolverError!! \n{cs}")
        # driver.refresh()
        continue
    except WebDriverException as driver_exception:
        print(f"Web Driver Exception \n{driver_exception}")
        # driver.refresh()

    except NoSuchElementException as not_exist:
        print(f"Element not loaded \n{not_exist}")
        # driver.refresh()

    # If not returned except
    else:
        try:
            # Vis Application confirm yes popup
            confirm_yes_element = driver.find_elements(By.ID, "confirm-yes")
            print(confirm_yes_element)
            if len(confirm_yes_element):
                confirm_yes_element[0].click()
            else:
                driver.implicitly_wait(10)
                confirm_yes_element.click()
            print("Confirmed Yes !!")

            # Redirect to book-appointment
            driver.get('https://www.ckgsir.com/book-appointment')
            print("after book appointment")


            # Cancel Re-schedule Note
            mfp_close(driver)
            print("After Click close Re-schedule !!")
            break
        except NoSuchElementException as not_exist:
            print(f"Element not loaded \n{not_exist}")
            driver.close()
            continue
        except TimeoutException as te:
            print(f"TimeoutException \n{te}!!")
            driver.close()
            continue







notifier = ToastNotifier()
visa_app = True
while visa_app:
    print("Check calender !!")
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
