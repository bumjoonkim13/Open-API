import os
print(os.path.abspath(""))

import requests
from bs4 import BeautifulSoup


import pandas as pd
pd.options.display.max_rows = 30
pd.options.display.max_columns = 100
from bs4 import BeautifulSoup

import warnings, time
warnings.filterwarnings(action='ignore')
# warning을 무시하는 코드

product_df = pd.read_csv("domeggook_item_list_moksu.csv", encoding="cp949")
product_df

#--- pip install 코드는 한번만 실행하면됩니다 설치 이후 앞에 #을 붙혀 주석처리를 해주시면됩니다. ---#
# !pip install pyautoit
# !pip install selenium
# !pip install webdriver_manager
#--------------------------------------------------------------------------------#

import pandas as pd
# DataFrame을 컨트롤하는 라이브러리

import warnings, os, time, shutil, urllib
# warnings : 파이썬 경고 제어
# os : 경로 또는 파일 제어
# time : 시간 제어(일정시간 delay등)
# shutil : os의 폴더 제어(생성/삭제)
# urlib : 특정 url에서 이미지를 받을때 사용

warnings.filterwarnings(action='ignore')
# 파이썬에서 불필요한 warning은 안뜨게 함

from PIL import Image
# 파이썬에서 이미지를 다룰때 사용(png등을 불러들여서 리사이즈 저장 등)

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Keys.ARROW_DOWN , Keys.ARROW_LEFT , Keys.ARROW_RIGHT, Keys.ARROW_UP , Keys.BACK_SPACE , Keys.CONTROL, Keys.ALT , Keys.DELETE ,
# Keys.ENTER , Keys.SHIFT, Keys.SPACE , Keys.TAB , Keys.EQUALS , Keys.ESCAPE, Keys.HOME , Keys.INSERT , PgUp Key,  Keys.PAGE_UP,
# Keys.PAGE_DOWN , Keys.F1 , Keys.F2 , Keys.F3 , Keys.F4, Keys.F5 , Keys.F6 , Keys.F7 , Keys.F8 , Keys.F9 , Keys.F10, Keys.F11 , Keys.F12
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

driver.get('https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523')
time.sleep(3)

elem = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[1]/input")
elem.send_keys("lwbj313")
time.sleep(0.5)
# ID 입력

elem = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[2]/input")
elem.send_keys("sk125874%%")
time.sleep(0.5)
# PW 입력

elem = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button/span")
elem.click()
time.sleep(3)

# 확인 클릭
driver.get("https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback")
time.sleep(3)
# 2차 로그인 페이지 접속

elem = driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[4]/button")
elem.click()
time.sleep(3)
# 2차 로그인

driver.get("https://domeggook.com/main/")
time.sleep(3)
# 도매꾹 페이지 접속

product_df

driver.find_element("class name", "login").click()
driver.find_element("id", "idInput").send_keys("lwbj313")
driver.find_element("id", "pwInput").send_keys("sk125874$$")
driver.find_element("class name", "formSubmit").click()
time.sleep(10)

for idx in range(0, 8, 1):
    driver.switch_to.window(driver.window_handles[0])
    product_name = product_df.loc[idx, '제품명']
    print(product_name)

    model_no = product_df.loc[idx, '모델명']
    print(model_no)

    driver.get("https://domeggook.com/main/")
    time.sleep(3)
    # 도매꾹 페이지 접속

    elem = driver.find_element("class name", "kwd")
    elem.send_keys(product_name)
    time.sleep(0.5)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)
    # 도매꾹에서 상품명으로 검색

    try:
        elem = driver.find_element("xpath", "/html/body/div[7]/div/div[1]/div[7]/ol/li[1]/div[1]/a").click()
        time.sleep(10)
        # 첫번째 상품 클릭

        driver.switch_to.window(driver.window_handles[1])

        elem = driver.find_element("xpath", "/html/body/div[6]/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/button/b")
        brand_name = elem.text
        print(brand_name)

        try:
            elem = driver.find_element("class name", "lItemPrice")
            price = elem.text
            price = int(price.replace("원", "").replace(",", ""))
            print(price)
        except:
            print("금액추출 실패")

        elem = driver.find_element("xpath", "/html/body/div[6]/div/div/div[2]/div[1]/div/div[1]/div[2]/form/table/tbody/tr/td[2]/div[1]/div[1]/b")
        TITLE = elem.text

        if '사용허용' in TITLE:
            print(TITLE)
        else:
            print(TITLE)
            raise RuntimeError
        # 상세설명 이미지 사용여부

        model_url = current_url = driver.current_url
        response = requests.get(model_url)
        html_content = response.text

        # BeautifulSoup 객체를 사용하여 HTML을 파싱합니다
        soup = BeautifulSoup(html_content, 'html.parser')

        # id가 'lInfoViewItemInfoWrap'인 요소를 찾습니다
        info_wrap = soup.find('div', id='lInfoViewItemInfoWrap')

        # 추출한 데이터를 저장할 딕셔너리를 만듭니다
        data_dict = {}

        # 'lTblCell lTblCellLabel'과 'lTblCell'의 값을 추출하여 딕셔너리에 저장합니다
        for div in info_wrap.find_all('div', class_='lTbl lTblHalf'):
            label = div.find('label', class_='lTblCell lTblCellLabel').text.strip()
            value = div.find('div', class_='lTblCell').text.strip()
            data_dict[label] = value

        # 딕셔너리를 데이터프레임으로 변환합니다
        df = pd.DataFrame.from_dict([data_dict])
        print(df)

        made_in = df["원산지"][0]
        print(made_in)
        model = df["모델명"][0]
        print(model)
        plant = df["제조사"][0]
        print(plant)
        size_mass = df["상품포장 부피/무게"][0]
        print(size_mass)

        # 판매자 정보 get
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'id': 'lSellerInfo'})
        rows = table.find_all('tr')
        data_dict = {}
        #desired_th_texts = ["공급사명", "상호/대표자명", "사업자구분", "사업자등록번호", "사업장소재지", "문의번호", "이메일"]

        for row in rows:
            th = row.find_all('th')  # 변경된 부분: find_all()로 모든 th 태그를 찾음
            td = row.find_all('td')  # 변경된 부분: find_all()로 모든 td 태그를 찾음
            for i in range(len(th)):  # 변경된 부분: 모든 th와 td에 대해 반복
                th_text = th[i].get_text(strip=True) if th[i] else None
                td_text = td[i].get_text(strip=True) if td[i] else None
                if th_text and td_text:
                    data_dict[th_text] = td_text

        # 딕셔너리를 데이터프레임으로 변환
        df = pd.DataFrame.from_dict(data_dict, orient='index', columns=['값'])
        print(df)

        import shutil

        img_folder_path = os.path.abspath("") + product_name +"/smartstore_img"
        # root 경로 + 이미지 폴더 경로

        try:
            shutil.rmtree(img_folder_path)
        except:
            pass
        # 폴더 삭제(초기화)

        os.makedirs(img_folder_path, exist_ok=True)
        # 폴더 다시 생성

        # --- 이미지 저장 ---#
        img_path = os.path.abspath("") + product_name + "/smartstore_img/thumbimg.png"
        # root 경로 + 이미지 경로

        elem = driver.find_element("xpath", "/html/body/div[6]/div/div/div[1]/div[2]/div[1]/table/tbody/tr/td/a/img")  #
        img_url = elem.get_attribute('src')
        # 이미지의 xpath를 경로로 저장

        urllib.request.urlretrieve(img_url, img_path)
        # 이미지를 경로에 다운로드

        # --- 썸네일 사이즈 변환 ---#
        img_path = os.path.abspath("") + product_name + "/smartstore_img/thumbimg.png"
        # root 경로 + 이미지 경로

        image = Image.open(img_path)
        # 저장된 이미지 열기

        resized_image = image.resize((640, 640))
        # 이미지 리사이즈(스마트스토어 썸네일 사이즈)

        resized_image.save(img_path)
        # 리사이즈된 이미지 저장

        # --- page_img1 ---#
        img_path = os.path.abspath("") + product_name + "/smartstore_img/page_img1.png"
        # root 경로 + 이미지 경로

        model_url = current_url = driver.current_url # 현재 페이지 주소 가져오기
        response = requests.get(model_url) #현재 페이지 호출
        html_content = response.text # 호출한 페이지를 text로 변환
        soup = BeautifulSoup(html_content, 'html.parser') # BeautifulSoup 객체를 사용하여 HTML을 파싱합니다
        img_tags = soup.select('#lInfoViewItemContents img') # id가 "lInfoViewItemContents"인 객체 내부에 있는 모든 img 태그 찾기
        i = 0
        if isinstance(img_tags, list): # img가 2개 이상일 경우
            for img_tag in img_tags:
                i = i + 1
                img_src = img_tag['src']  # img 태그의 src 속성 값 가져오기
                img_path = os.path.abspath("") + product_name + "/smartstore_img/page_img" + str(i) + ".png"  # 다운로드 할 경로와 파일명
                urllib.request.urlretrieve(img_src, img_path)  # 이미지를 경로에 다운로드
        else: # img가 1개 일 경우
            i = i+1
            img_src = img_tags['src']  # img 태그의 src 속성 값 가져오기
            img_path = os.path.abspath("") + product_name + "/smartstore_img/page_img" + str(i) + ".png"  # 다운로드 할 경로와 파일명
            urllib.request.urlretrieve(img_src, img_path)  # 이미지를 경로에 다운로드
            pass


        # --- 모든 탭 종료 및 0번째 탭으로 이동 ---#
        for i in range(10):
            if len(driver.window_handles) > 1:
                # driver.window_handles : driver의 tab의 리스트
                # len(driver.window_handles) > 1 : driver tab의 리스트가 2개 이상이면 실행

                driver.switch_to.window(driver.window_handles[1])
                # 1번째 탭으로 이동

                driver.close()
                # 해당 탭 종료
            else:
                break
                # 탭이 하나만 남았으면 break

        driver.switch_to.window(driver.window_handles[0])
        # 0번째 탭으로 이동

        driver.get("https://shopping.naver.com/home")
        time.sleep(3)
        # 네이버 쇼핑 접속

        elem = driver.find_element("xpath", "/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[1]/div/input")
        elem.send_keys(product_name)
        elem.send_keys(Keys.ENTER)
        time.sleep(0.5)
        time.sleep(5)
        # 제품명 검색
        #

        elem = driver.find_element("xpath", "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span[1]")
        cate1 = elem.text
        print(cate1)

        elem = driver.find_element("xpath", "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span[2]")
        cate2 = elem.text
        print(cate2)

        elem = driver.find_element("xpath", "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span[3]")
        cate3 = elem.text
        print(cate3)

        try:
            elem = driver.find_element("xpath", "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span[4]")
            cate4 = elem.text
            print(cate4)
        except NoSuchElementException:
            cate4=''
            pass


        # 카테고리 정보 크롤링

        category_list = [cate1, cate2, cate3, cate4]
        category_list
        # 카테고리를 리스트로 만들기

        # 스마트스토어 업로드

        for idx in range(0, 3):
            driver.get('https://sell.smartstore.naver.com/#/products/create')
            time.sleep(3)
        # 스마트스토어 제품등록 페이지 접속

        try:
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/div/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button/span")
            elem.click()
            time.sleep(1)
        except:
            pass
        # 네이버풀필먼트, 네이버도착보장 유의사항 안내 창 뜨면 꺼줌

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[3]/div/div[2]/div/div/div/category-search/div[1]/div[1]/div/label[2]")
        elem.click()
        time.sleep(1)
        # 카테고리명 선택 클릭

        driver.execute_script("window.scrollTo(0, 10000)")

        for idx in range(1, 31):
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[3]/div/div[2]/div/div/div/category-search/div[3]/div[1]/ul/li[" + str(idx) + "]/a")
            cate1 = elem.text
            elem.send_keys(Keys.TAB, Keys.TAB)
            time.sleep(0.5)
            #print(cate1)

            if cate1 in category_list:
                elem.click()
                break
        time.sleep(2)
        # cate1 클릭

        for idx in range(2, 31):
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[2]/ul/li[" + str(idx) + "]/a")
            cate1 = elem.text
            elem.send_keys(Keys.TAB, Keys.TAB)
            time.sleep(0.5)
            #print(cate1)

            if cate1 in category_list:
                elem.click()
                break
        time.sleep(2)
        # cate2 클릭

        for idx in range(2, 31):
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[3]/ul/li[" + str(idx) + "]/a")
            cate1 = elem.text
            elem.send_keys(Keys.TAB, Keys.TAB)
            time.sleep(0.5)
            #print(cate1)

            if cate1 in category_list:
                elem.click()
                break
        time.sleep(2)
        # cate3 클릭

        for idx in range(2, 31):
            try:
                elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[4]/ul/li[" + str(idx) + "]/a")
                cate1 = elem.text
                elem.send_keys(Keys.TAB, Keys.TAB)
                time.sleep(0.5)
                print(cate1)

                if cate1 in category_list:
                    elem.click()
                    break
            except:
                # print("cate4 없음")
                time.sleep(2)
        # cate4 클릭

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[7]/div/div[2]/div/div/div/div/div/div/input")
        elem.send_keys(product_name)
        time.sleep(0.5)
        # 제품명 입력

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[8]/div/div[2]/div/div[1]/div/div/div[1]/div/div/input")
        elem.clear()
        elem.send_keys(int(price * 1.1))
        time.sleep(0.5)
        # 제품가격 입력

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[10]/div/div[2]/div/div/div/div/div[1]/div/div/input")
        elem.clear()
        elem.send_keys(99)
        time.sleep(0.5)
        # 제품 개수 설정

        driver.execute_script("window.scrollTo(0, 10000)")

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[17]/div[2]/div[1]/div/div")
        elem.click()
        time.sleep(1)
        # 상품 주요정보 클릭

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[17]/div[2]/div[2]/div/ncp-naver-shopping-search-info/div[2]/div/div[1]/div/ncp-brand-manufacturer-input/div/div/div/div/div/div[1]/input")
        elem.clear()
        elem.send_keys(brand_name)
        elem.send_keys(Keys.ENTER)
        time.sleep(0.5)
        # 브랜드

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[17]/div[2]/div[2]/div/ncp-naver-shopping-search-info/div[2]/div/div[2]/div/ncp-brand-manufacturer-input/div/div/div/div/div/div[1]/input")
        elem.clear()
        elem.send_keys(plant)
        elem.send_keys(Keys.ENTER)
        time.sleep(0.5)
        # 제조사

        driver.execute_script("window.scrollTo(0, 10000)")

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/div/div/div")
        elem.click()
        time.sleep(1)
        # 상품정보제공고시

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[2]/div/div/div[1]/div/div[1]")
        elem.click()
        time.sleep(1)
        # 상품군 드랍박스 클릭

        for idx in range(1, 31):
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[2]/div/div/div[1]/div/div[2]/div/div[" + str(idx) + "]")
            TITLE = elem.text
            print(TITLE)
            if TITLE == '기타 재화':
                elem.click()
                break
        # 기타재화 클릭

        if cate4 == '':
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[1]/div/div/input")
            elem.clear()
            elem.send_keys(category_list[-2])
            time.sleep(0.5)
        else:
            elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[1]/div/div/input")
            elem.clear()
            elem.send_keys(category_list[-1])
            time.sleep(0.5)
        # 품명 입력

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[2]/div/div/input")
        elem.clear()
        elem.send_keys(model_no)
        time.sleep(0.5)
        # 모델 입력

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[3]/div/div[1]/label[2]/span")
        elem.click()
        time.sleep(1)
        # 법에 의한 인증, 허가 등을 받았음을 확인할 수 있는 경우 그에 대한 사항

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[4]/div/ncp-brand-manufacturer-input/div/div/div/div/div/div[1]/input")
        elem.clear()
        elem.send_keys(plant)
        elem.send_keys(Keys.ENTER)
        time.sleep(0.5)
        # 제조자(사)

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[18]/div/fieldset/div/div/div[3]/ng-include/div[5]/div/div[2]/input")
        elem.clear()
        elem.send_keys("010-5467-3871")
        time.sleep(0.5)
        # A/S 책임자 또는 소비자 상담 관련 전화번호

        driver.execute_script("window.scrollTo(0, 10000)")

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[2]/div/div/div")
        elem.click()
        time.sleep(1)
        # 배송 탭

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[2]/div[2]/div/div[6]/div/div/div/div/div/div[1]")
        elem.click()
        time.sleep(1)

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[2]/div[2]/div/div[6]/div/div/div/div/div/div[2]/div/div[5]")
        elem.click()
        time.sleep(1)
        # 택배사

        driver.execute_script("window.scrollTo(0, 10000)")

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[3]/div/div/div")
        elem.click()
        time.sleep(1)
        # 반품/교환탭 클릭

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[3]/div[2]/div/ng-include/div/div[2]/div/div/div/div/div/input")
        elem.clear()
        elem.send_keys("3000")
        #elem.send_keys(Keys.ENTER)
        time.sleep(0.5)
        #Alert(driver).accept()  # 팝업창 확인 누르기
        time.sleep(0.5)
        # 반품배송비(편도)

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[19]/div[3]/div[2]/div/ng-include/div/div[3]/div/div/div/div/div/input")
        elem.clear()
        elem.send_keys("6000")
        #elem.send_keys(Keys.ENTER)
        #time.sleep(0.5)
        #Alert(driver).accept()  # 팝업창 확인 누르기
        time.sleep(0.5)
        # 교환배송비(왕복)

        driver.execute_script("window.scrollTo(0, 10000)")

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[20]/div/div/div/div")
        elem.click()
        time.sleep(1)
        # AS특이사항 클릭

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[20]/div/div[2]/div/div[1]/div/div[1]/div/div/input")
        elem.clear()
        elem.send_keys("010-5467-3871")
        time.sleep(0.5)
        # AS 전화번호

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[20]/div/div[2]/div/div[2]/div/textarea")
        elem.clear()
        elem.send_keys("상품 수령후 재판매 가능 상품의 경우 7일 이내 교환 반품 환불이 가능합니다.")
        time.sleep(0.5)
        # AS안내

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[12]/div/div[2]/div/div[1]/div/div/ncp-product-temp-photo-infra-image-upload/div/div[1]/div/ul/li/div/a")
        elem.click()
        time.sleep(1)
        # 대표이미지 클릭

        #### FINDER 창이 뜨기 전에 아래 코드를 실행시켜야 합니다 ###

        img_path = os.path.abspath("") + product_name + "/smartstore_img/thumbimg.png"
        # 이미지 경로

        elem = driver.find_element("xpath", "//input[@type='file']")
        elem.send_keys(img_path)
        # 파일 넣기
        time.sleep(3)

        for idx in range(1, 11):
            driver.execute_script("window.scrollTo(0, " + str(idx * 1000) + ")")
            time.sleep(0.5)
            # 페이지 순차적으로 내리기

            time.sleep(1)
            try:
                elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[2]/fieldset/form/ng-include/ui-view[14]/div/div[2]/div/div/ncp-editor-form/div[1]/div/p[4]/button")
                elem.click()
                time.sleep(1)
                # smart editor one
                break
            except:
                pass
        # SmartEditor One 창 클릭
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[1])

        for i in range(1, 50, 1): # 이미지 등록 반복문
            try:
                # --- page_img1 ---#
                elem = driver.find_element("xpath", "/html/body/ui-view[1]/ncp-editor-launcher/div[2]/div/div[1]/div/header/div[1]/ul/li[1]/button/span[1]")
                elem.click()
                time.sleep(1)
                # 사진 클릭

                #### FINDER 창이 뜨기 전에 아래 코드를 실행시켜야 합니다 ###

                img_path = os.path.abspath("") + product_name + "/smartstore_img/page_img"+str(i)+".png"
                # 이미지 경로

                elem = driver.find_element("xpath", "//input[@type='file']")
                elem.send_keys(img_path)
                # 파일 넣기
                time.sleep(1.5)
                print(i, "이미지를 모두 넣었습니다.")
            except:
                #print(i, "이미지를 모두 넣었습니다.")
                pass
        driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/button/span").click()
        time.sleep(1)
        elem = driver.find_element("xpath", "/html/body/ui-view[1]/ncp-editor-launcher/div[1]/div/button/span[1]")
        elem.click()
        time.sleep(1)
        # 등록

        driver.switch_to.window(driver.window_handles[0])

        elem = driver.find_element("xpath", "/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div[3]/div[2]/div[1]/button[3]/span[1]")
        elem.click()
        time.sleep(1)
        # 저장하기 누르기

        elem = driver.find_element("class name", "btn.btn-default")
        elem.click()
        time.sleep(1)
        # 상품관리
    except Exception as e:
        print("An error occurred:", e)
        print("에러발생 : " + product_name)
        for i in range(10):
            if len(driver.window_handles) > 1:
                # driver.window_handles : driver의 tab의 리스트
                # len(driver.window_handles) > 1 : driver tab의 리스트가 2개 이상이면 실행

                driver.switch_to.window(driver.window_handles[1])
                # 1번째 탭으로 이동

                driver.close()
                # 해당 탭 종료
            else:
                break
                # 탭이 하나만 남았으면 break

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
pass
