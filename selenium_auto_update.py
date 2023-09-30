import os
import re
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import urllib.request
import requests
from bs4 import BeautifulSoup

# WebDriverのダウンロード元のURL
WEBDRIVER_BASE_URL = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"

LATEST_VERSION_URL = "https://googlechromelabs.github.io/chrome-for-testing/"

# WebDriverを起動する
def isLaunch(chromedriver_path='chromedriver.exe'):
    service = Service(executable_path=chromedriver_path)
    try:
        driver = webdriver.Chrome(service=service)
        print('起動に成功。問題なし。')
        driver.quit()
        return True
    except (FileNotFoundError, WebDriverException, SessionNotCreatedException) as e:
        print("エラー詳細:", str(e))  # エラーメッセージの詳細を出力
        return e

# 最新のWebDriverのバージョンを取得する関数
def get_latest_webdriver_version():
    response = requests.get(LATEST_VERSION_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    response = requests.get(LATEST_VERSION_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    td_element = soup.find(string="Stable").find_next('td')
    stable_version = td_element.find("code").text
    return stable_version

# 指定されたバージョンのWebDriverをダウンロードする関数
def download_webdriver_version(version):
    file_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/win32/chromedriver-win32.zip"
    save_path = "./download_webdriver.zip"
    print(version + ' のバージョンをダウンロードします。')
    # zipファイルをダウンロード
    with urllib.request.urlopen(file_url) as download_file:
        data = download_file.read()
        with open(save_path, mode='wb') as save_file:
            save_file.write(data)
    # ダウンロードしたzipファイルを解凍
    with zipfile.ZipFile("./download_webdriver.zip") as obj_zip:
        with obj_zip.open('chromedriver-win32/chromedriver.exe') as src, open('./chromedriver.exe', 'wb') as dst:
            dst.write(src.read())
    # zipファイルはいらないので削除 
    os.remove('./download_webdriver.zip')
    print("ダウンロード完了")

# WebDriverのダウンロードと起動を試みる関数
def download_and_launch_webdriver():
    # エラーメッセージから現在のバージョンを取得
    match = re.search(r'(?<=\bchrome=)\d+', str(error))
    if match:
        current_version = match.group()
        print("chromeのversionは " + current_version)
    else:
        print("エラーメッセージからChromeのバージョンを取得できませんでした。最新のバージョンを取得します。")
        current_version = get_latest_webdriver_version()
        if not current_version:
            print("最新のWebDriverのバージョンを取得できませんでした。")
            return

    # バージョン情報の取得とダウンロード
    download_webdriver_version(current_version)
    if isLaunch() is True:
        print("WebDriverの更新と起動に成功しました。")
    else:
        print("更新後のWebDriverの起動に失敗しました。")

# 以下、メインの実行部分
error = isLaunch()
if isinstance(error, (SessionNotCreatedException, FileNotFoundError, WebDriverException)):
    download_and_launch_webdriver()
else:
    print("その他のエラー：" + str(error))
