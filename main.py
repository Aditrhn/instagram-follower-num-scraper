from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd

# Buat beberapa list yang akan kita gunakan seperti username, names, account, followers, dan followings
username = ['bankbri_id', 'lifeatbri', 'narasiodata']
names = []
accounts = []
followers = []
followings = []

# Pattern regex untuk mengambil nama pemilik akun
pattern = r'^([^()]+)'

for uname in username:
    # Menajalankan webdriver dan membuka link akun
    browser = webdriver.Edge()
    browser.get('https://www.instagram.com/'+uname)
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Mengambil sumber html dan melakukan parsing menggunakan BeautifulSoup
    source = browser.page_source
    data = BeautifulSoup(source, 'html.parser')

    # Mengambil data nama pemilik akun dari tag <meta> dengan property 'og:title'
    title = data.find('meta', property='og:title').get('content')
    # Mengambil data nama pemiliki menggunakan regex
    name = re.match(pattern, title).group().rstrip()
    names.append(name)

    # Mengambil informasi follower, following, serta beberapa deskripsi dari akun
    desc = data.find('meta', property='og:description').get('content').split(',')
    
    accounts.append('https://www.instagram.com/'+uname)
    followers.append(desc[0])
    followings.append(desc[1])

# Membentuk dataframe yang berisi informasi akun yang telah di scrape
data = {'Name':names, 'Instagram_account':accounts, 'Follower':followers, 'Following':followings}
df = pd.DataFrame(data)

browser.close()

df.head()