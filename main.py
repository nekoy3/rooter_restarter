from selenium import webdriver
from selenium.webdriver import ChromeOptions
import chromedriver_binary
import datetime
import time
import requests
import subprocess

options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.add_argument('--disable-gpu')  # ページによって必要な場合がある模様

#グローバルIP取得用
def get_gip_addr():
        res = requests.get('https://ifconfig.me')
        return res.text

#タイムスタンプを付与した文字列を返す
def log(string):
    return "[" + str(datetime.datetime.now()) + "]: " + string + "\n"

#ログ出力用
f = open('restart_router.log', 'a')
f.write(log("restarting router..."))

#開くページのURL
url = "http://admin:qtnetbbiq@192.168.0.1/index_reset.html"
driver = webdriver.Chrome(options=options)
f.write(log("getting url..."))

try:
    driver.get(url)
except:
    f.write(log("getting url failed."))
    driver.quit()
    exit()
else:
    f.write(log("succeed getting url!"))

driver.quit()

#ルーター再起動した後pingで接続確認を2分間行う
f.write(log("process sleeping..."))
time.sleep(5)
for i in range(115):
    r = subprocess.run(["ping", "8.8.8.8", "-c", "2", "-w", "300"], stdout=subprocess.PIPE)
    #print(r.stdout.decode("cp932"))
    #print(r.returncode)

    if r.returncode == 0:
        f.write(log("internet connection succeed!"))
        break
    time.sleep(1)
else:
    f.write(log("internet connection timeout."))
    exit()

#2分間繋がらなければelseに入りtimeoutとしてexitする
#繋がればip_addr.txtにグローバルIPを出力して処理終了

addr = get_gip_addr()
f.write(log("my ip address: " + addr))
f.close()

i = open('ip_addr.txt', 'w')
i.write(addr)
i.close()