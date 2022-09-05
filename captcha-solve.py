from dotenv import load_dotenv
from bs4 import BeautifulSoup
from captcha_solver import CaptchaSolver
import captcha_solver
import requests
import os

# Load .env
load_dotenv('.env')

# Make session
s = requests.session()

# Request to get login page and captcha
headers = {
    'Host': 'www.ckgsir.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
    'Referer': 'https://www.ckgsir.com/book-appointment'
}
html = s.get('https://www.ckgsir.com/my-account', headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
form = soup.find_all('div', attrs={"class": "form-group"})
captcha_src = soup.find('img', attrs={"class": "BDC_CaptchaImage"})['src']
captcha_link = f"https://www.ckgsir.com/{captcha_src}"
res = s.get(captcha_link)

if not os.path.exists("static"):
    os.mkdir("static")

with open(f'static{os.sep}img.jpg', 'wb') as out_file:
    out_file.write(res.content)

# For use captcha solver we have 2 choice:
# 1- Use https://rapidapi.com/dickyagustin/api/solvemedia-solver (Free but need VPN for use in Iran)
# 2- Use https://pypi.org/project/captcha-solver and https://2captcha.com and pay money for solve 1000 captcha per month


# # Choice 1 snipped code from https://rapidapi.com/dickyagustin/api/solvemedia-solver:
# url = "https://solvemedia-solver.p.rapidapi.com/byImageUrl"
# payload = {"url": "http://127.0.0.1:8000/static/img.jpg"}  # Linked to image that saved to django static dir.
# headers_rapidApi = {
#     "content-type": "application/json",
#     "X-RapidAPI-Key": "147f31d0d7mshfeff868a0b4d1dap1fc5b2jsn307a403f36ec",
#     "X-RapidAPI-Host": "solvemedia-solver.p.rapidapi.com"
# }
# response = requests.request("POST", url, json=payload, headers=headers_rapidApi)
# captcha_text = response.text


#  Choice 2, snipped code from https://pypi.org/project/captcha-solver and use https://2captcha.com
try:
    solver = CaptchaSolver('2captcha', api_key=os.getenv("CAPTCHA_API_KEY"))
    raw_data = open(f'static{os.sep}img.jpg', 'rb').read()
    captcha_text = solver.solve_captcha(raw_data)
    print(captcha_text)
except captcha_solver.CaptchaSolverError:
    print("Balance Too Low!! \nCaptcha does not solved!!")

#%%
