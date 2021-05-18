
import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import pandas as pd
import traceback

#ブラウザの自動更新（Chrome）
def setup_class(cls):
        cls.driver =webdriver.Chrome(ChromeDriverManager().install())

# Chromeを起動する関数

logtime = datetime.datetime.now()

with open('logfile.csv','a',encoding='utf-8') as f:
            f.write(str(logtime))


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    
    # 検索窓に入力
    #　検索
    driver.get('https://tenshoku.mynavi.jp/list/kw'+input('検索条件を指定')+'/?jobsearchType=14&searchType=18')
    

    a=1

    # ページ終了まで繰り返し取得
    while a < 3:

        exp_name_list = []

        # 検索結果の一番上の会社名を取得
        name_list= driver.find_elements_by_class_name("cassetteRecruit__name")

        # 検索結果から初年度年収を取得
        exp_money_list = []
        money_list = driver.find_elements_by_class_name("tableCondition__body")

        for name,money in zip(name_list,money_list):

            exp_name_list.append(name.text)
            exp_money_list.append(money.text)

            with open('logfile.csv','a',encoding='utf-8') as f:
                f.write(str(1+exp_name_list.index(name)))

            #CSVファイルに出力
            df = pd.DataFrame([exp_name_list,exp_money_list])
            df.to_csv(r'C:\Users\Taisei\Documents\Program~\kadai02\data02.csv',header = False,index=True)
        
        #次のページに遷移する

        try:
            url=driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div/nav[1]/ul/li['+str(a)+']/a').get_attribute("href")
            driver.get(url)
        except:
            with open('logfile.csv','a',encoding='utf-8') as f:
                f.write(traceback.format_exc())

            break


        a+=1
    




        


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()

