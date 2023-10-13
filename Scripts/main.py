import configparser
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import openpyxl
import main_links as links


def get_config_info():
    # 설정 파일 읽기
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 설정 파일에서 아이디와 비밀번호 가져오기
    username = config['Credentials']['username']
    password = config['Credentials']['password']

    if username == '' or password == '':
        print("config.ini 파일에 포탈 아이디와 비밀번호를 입력하십시오.")
    else:
        return username, password


def check_login(driver):
    # 로그인 후의 대시보드 페이지로 이동되었는지 확인
    dashboard_url = links.logined_portal  # 대시보드 페이지 URL로 변경해야 합니다.
    if driver.current_url == dashboard_url:
        print("로그인 성공 및 대시보드 페이지로 이동됨")
    else:
        print("로그인 실패 또는 대시보드 페이지로 이동되지 않음")

    return


def portal_login(driver):
    # 포탈 로그인 버튼 클릭.
    login_page_button = driver.find_element(By.CLASS_NAME, "login_btn")
    login_page_button.click()

    # 아디 비번 할당.
    username, password = get_config_info()
    username_field = driver.find_element("id", "loginId")
    password_field = driver.find_element("id", "loginPasswd")

    # 아디 비번 치고 로그인.
    username_field.send_keys(username)
    password_field.send_keys(password)

    # 로그인 버튼 클릭.
    login_button = driver.find_element("id", "loginBtn")
    login_button.click()

    check_login(driver)  # 정상 로그인 되었는지 체크.

    return


def ini_website():
    # 웹 드라이버 초기화.
    options = webdriver.ChromeOptions()  # 크롬창 안띄우게.
    # options.add_argument('headless')

    driver = webdriver.Chrome(options=options)  # 웹 드라이버 초기화.
    return driver


def conn_webpage(driver, link):
    # 홈페이지 연결.
    driver.get(link)


def click_button(driver, xpath, latency):
    btn = driver.find_element(By.XPATH, xpath)
    btn.click()
    driver.implicitly_wait(latency)


def get_semesters(driver):
    # 학기별 성적 탭 얻기.
    temp = []
    for i in range(8):
        i = 2 * i + 1
        try:
            element = driver.find_element(By.XPATH, links.sem_xpath + f"/div[{i}]")
            temp.append(element)
        except:
            print("1.NoSuchElement :", links.sem_xpath + f"/div[{i}]")
            break

    # 마지막 공백 제거.
    if temp[-1].text == "":
        temp = temp[:-1]

    return temp


def get_elements(driver, sem_num):
    hakjeong_list = []
    sub_name_list = []
    score_list = []
    semester_list = []
    retake_list = []

    for i in range(len(sem_num)):
        sem_num[i].click()
        semester_list.append(sem_num[i].text)

        scorepath = links.score_path_front + f"div[{2 * (i + 1)}]/" + links.score_path_back
        for j in range(15):
            if j == 0:
                path = "div"
            else:
                path = f"div[{j}]"
            try:
                # XPATH로 요소 찾기 시도
                hakjeong_num = driver.find_element(By.XPATH, scorepath + f"{path}/div[8]/div/div")
                sub_name = driver.find_element(By.XPATH, scorepath + f"{path}/div[9]/div/div")
                score = driver.find_element(By.XPATH, scorepath + f"{path}/div[11]/div/div")
                retake = driver.find_element(By.XPATH, scorepath + f"{path}/div[12]/div/div")

                # 요소를 찾았을 때 수행할 동작
                hakjeong_list.append(hakjeong_num.text)
                sub_name_list.append(sub_name.text)
                score_list.append(float(score.text))
                semester_list.append("")
                if retake.text == 'R':
                    retake_list.append('O')
                else:
                    retake_list.append("")

            except NoSuchElementException:
                # NoSuchElementException이 발생했을 때 수행할 동작
                # print("NoSuchElement(2) :" + f"{path}")
                semester_list.pop()
                break
    return semester_list, hakjeong_list, sub_name_list, score_list, retake_list


def check_make_df(semester_list, hakjeong_list, sub_name_list, score_list, retake_list):
    # 데이터프레임을 만들 수 있는지 체크.
    if len(hakjeong_list) == len(sub_name_list) == len(score_list) == len(semester_list) == len(retake_list):
        print(f"각 column의 요소는 {len(hakjeong_list)}개이므로, DataFrame 생성 가능.")
    else:
        print("각 clolumn의 요소 개수가 서로 다른 것이 있습니다.")
        print(f"hakjeong_list : {len(hakjeong_list)}\n"
              f"sub_name_list : {len(sub_name_list)}\n"
              f"score_list : {len(score_list)}\n"
              f"semester_list : {len(semester_list)}\n"
              f"retake_list : {len(retake_list)}")


def create_df(semester_list, hakjeong_list, sub_name_list, score_list, retake_list):
    df = pd.DataFrame({
        '학기': semester_list,
        '학정번호': hakjeong_list,
        '교과목명': sub_name_list,
        '학점': score_list,
        '재수강 여부': retake_list
    })

    # 각 학기 당 맨 앞 교과목 중복 제거.
    for i in range(len(semester_list)):
        if semester_list[i] != "":
            df = df.drop(i + 1)

    return df


def input_hakbu(driver):
    select_mirae_field = driver.find_element(By.XPATH, links.hakbu_mirae_xpath)
    select_mirae_field.click()
    select_mirae_field.send_keys(Keys.CONTROL + "A")
    time.sleep(0.1)
    select_mirae_field.send_keys(Keys.BACKSPACE)
    time.sleep(0.1)
    select_mirae_field.send_keys("학부(미래)")


def write_excel(df):
    print("엑셀시트 작성.")
    file_name = '졸업학점계산기.xlsx'
    writer = pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay')
    df.to_excel(writer, sheet_name='score', startcol=0, startrow=1, index=False, header=False)
    writer.close()
    print("엑셀시트 작성완료.")


def main(latency):
    # 웹 드라이버 초기화.
    driver = ini_website()

    # 연세포탈 연결.
    conn_webpage(driver, links.yonsei_portal)
    driver.maximize_window()

    portal_login(driver)  # 포탈 로그인.

    # 학사 페이지 이동.
    conn_webpage(driver, links.haksa_page)
    driver.maximize_window()
    driver.implicitly_wait(latency)

    # 성적 버튼 클릭.
    click_button(driver, links.score_xpath, latency)

    # 전체 성적 조회 버튼 클릭.
    click_button(driver, links.total_score_xpath, latency)

    # 학기별 성적 탭 정보 얻기.
    semesters = get_semesters(driver)

    # 학기별 성적에 대한 칼럼값 얻기.
    semester_list, hakjeong_list, sub_name_list, score_list, retake_list = get_elements(driver, semesters)
    driver.implicitly_wait(latency)

    # 데이터프레임을 만들 수 있는지 체크.
    check_make_df(semester_list, hakjeong_list, sub_name_list, score_list, retake_list)

    # 데이터프레임 생성.
    df = create_df(semester_list, hakjeong_list, sub_name_list, score_list, retake_list)

    # 테이블 표시.
    df = df.reset_index(drop=True)
    pd.options.display.max_rows = None
    print(df)

    # 전체 학점 계산.
    total_credit = df['학점'].sum()

    # 재수강 과목 학점 제거.
    for idx, row in df.iterrows():
        if row['재수강 여부'] == 'O':
            retake_score = row['학점']
            total_credit -= retake_score
        else:
            pass

    print(total_credit)

    # 수강편람 홈페이지 연결.
    conn_webpage(driver, links.lecture_list_page)
    driver.implicitly_wait(latency)
    time.sleep(latency*(2/3))

    # 수강편람에서 과목종별 탐색하는 코드.
    sub_kind_list = []

    for i in range(len(df['학정번호'])):
        if df['학기'][i] != '':
            date = df['학기'][i]
            if "여름학기" in date or "겨울학기" in date:
                year, sem = date[0:4], date[8:12]
            else:
                year, sem = date[0:4], date[8:11]

            input_year_field = driver.find_element(By.XPATH, links.lec_year_xpath)
            input_year_field.click()

            input_year_field.send_keys(Keys.CONTROL + "A")
            time.sleep(0.1)
            input_year_field.send_keys(Keys.BACKSPACE)
            input_year_field.send_keys(year)
            driver.implicitly_wait(latency)

            input_sem_field = driver.find_element(By.XPATH, links.lec_sem_xpath)
            input_sem_field.click()
            input_sem_field.send_keys(Keys.CONTROL + "A")
            time.sleep(0.1)
            input_sem_field.send_keys(Keys.BACKSPACE)
            input_sem_field.send_keys(sem)
            driver.implicitly_wait(latency)
        else:
            pass

        input_hakbu(driver)

        lec_num = df['학정번호'][i][0:7]
        print(lec_num)
        time.sleep(0.1)
        lec_num_field = driver.find_element(By.XPATH, links.lec_num_xpath)
        lec_num_field.click()

        lec_num_field.send_keys(Keys.CONTROL + "A")
        time.sleep(0.1)
        lec_num_field.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
        lec_num_field.send_keys(lec_num)
        driver.implicitly_wait(latency)

        srch_btn = driver.find_element(By.XPATH, links.lec_srch_btn_xpath)
        srch_btn.click()
        driver.implicitly_wait(latency)

        time.sleep(0.2)
        sub_kind = driver.find_element(By.XPATH, links.lec_sub_kind_xpath)
        sub_kind_list.append(sub_kind.text)

    print(len(sub_kind_list))

    df.insert(loc=4, column='과목종별', value=sub_kind_list)
    print(df)

    write_excel(df)
    driver.quit()
