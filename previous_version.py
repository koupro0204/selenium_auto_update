# いろんなものをインポート
import re
import zipfile
from pip._vendor import requests
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException,WebDriverException
from bs4 import BeautifulSoup
import urllib.request

# 必要な情報

#実行環境上のChromeブラウザのバージョンの箱
current_version = ""
#ウェブドライバーページ
webdriver_url   = "https://chromedriver.storage.googleapis.com/"
#Windows用のファイル名
file_name       = "chromedriver_win32.zip"

try:
    driver = webdriver.Chrome('chromedriver')
    print('起動に成功。問題なし。')
except(FileNotFoundError,WebDriverException,SessionNotCreatedException) as e:
    if type(e) == SessionNotCreatedException:
        print("WebDriverが古いです。")
        tmp = re.split("\n",str(e))
        tmp = re.split(" ",tmp[1])
        tmp = re.split("\.",tmp[4])
        current_version = tmp[0]+"."+tmp[1]+"."+tmp[2]
        print("chromeのversionは "+current_version)
    elif type(e)==FileNotFoundError or type(e)== WebDriverException:
        print("WebDriverが見つかりません。")

    else:
        print("不明な例外です。")
        print(e)
        exit()
    print('エラーが出たので最新版のWebDriverをダウンロード開始')
    response = requests.get(webdriver_url)
    soup = BeautifulSoup(response.text,"lxml-xml")
    for version in reversed(soup.find_all("Key")):
    
        if((current_version != "" and version.text.startswith(current_version))
        or (current_version == "" and version.text.endswith(file_name))):
            get_version = re.sub("/.*","",version.text)

            file_url = webdriver_url + get_version + "/" + file_name

            save_path = "./download_webdriver.zip"

            print(get_version+' のバージョンをダウンロードします。')
            with  urllib.request.urlopen(file_url) as download_file:
                data = download_file.read()
                with open(save_path, mode='wb') as save_file:
                    save_file.write(data)
            import zipfile

            with zipfile.ZipFile("./download_webdriver.zip") as obj_zip:
                obj_zip.extractall("./")
            try:
                driver = webdriver.Chrome('chromedriver')
                print('起動に成功。問題なし。')
                break
            except(SessionNotCreatedException) as e:
                if type(e) == SessionNotCreatedException:
                    print('失敗。違うバージョンを試します。')
                    print("WebDriverが古いです。")
                    tmp = re.split("\n",str(e))
                    tmp = re.split(" ",tmp[1])
                    tmp = re.split("\.",tmp[4])
                    current_version = tmp[0]+"."+tmp[1]+"."+tmp[2]

driver.quit()
exit()