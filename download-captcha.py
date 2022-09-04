import requests
from bs4 import BeautifulSoup

s = requests.session()
headers = {
    'Host' : 'www.ckgsir.com',
    'Connection' : 'keep-alive',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'en-US,en;q=0.9,fa;q=0.8',
    'Referer':'https://www.ckgsir.com/book-appointment'
}
html = s.get('https://www.ckgsir.com/my-account',headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
form = soup.find_all('div', attrs={"class":"form-group"})
captcha_src = soup.find('img', attrs={"class":"BDC_CaptchaImage"})['src']
captcha_link = f"https://www.ckgsir.com/{captcha_src}"
res = s.get(captcha_link)
with open('img.jpg', 'wb') as out_file:
    out_file.write(res.content)
print(captcha_link)

