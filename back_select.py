import selenium
import warnings
warnings.filterwarnings("ignore")
import time
from selenium import webdriver
import csv
import time
import datetime
import base64
import requests
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

def WebConduct():
    time.sleep(40)

    file = open('save.csv', 'r', newline='')
    rows = csv.DictReader(file)

    for row in rows:
        student_id = row['studentid']
        password = row['password']
        Date = row['Date']
        which_one = row['Time']
        choice = which_one.split(' ')
        email = row['email']
        place = row['place']
        number = row['num']
    file.close()

    parts = Date.split('/')
    string = parts[0]+'-'+parts[1]+'-'+parts[2]+' 08:00:00'
    delta = datetime.timedelta(days =-7)
    target = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    dealtime = (target+delta).strftime("%Y %b %d %I:%M:%S")    
    localtime = time.localtime()
    tran = time.strftime("%Y %b %d %I:%M:%S", localtime)
                     
    while tran<dealtime:
        localtime = time.localtime()
        tran = time.strftime("%Y %b %d %I:%M:%S", localtime)   

    driver = webdriver.Chrome('.\chromedriver.exe')
    URL = 'https://ntupesc.ntu.edu.tw/facilities/'
    driver.get(URL)

    '''
    新體首頁
    '''
    # 按x
    p1_x = driver.find_element_by_xpath('/html/body/div/div[1]/button/span[1]')
    p1_x.click()
    
    # 學生登入
    p1_enter=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tcTab_tpValidator_HypLinkStu"]/p')
    p1_enter.click()

    '''
    登入頁
    '''
    # 輸入帳號
    p2_acc = driver.find_element_by_xpath('//*[@id="myTable"]/td/input')
    p2_acc.send_keys(student_id)
    
    # 輸入密碼
    p2_pw = driver.find_element_by_xpath('//*[@id="myTable2"]/td/input')
    p2_pw.send_keys(password)
    
    # 按enter
    p2_enter = driver.find_element_by_xpath('//*[@id="content"]/form/table/tbody/tr[3]/td[2]/input')
    p2_enter.click()


    '''
    選擇頁
    '''
    # 按x
    p3_x = driver.find_element_by_xpath('/html/body/div/div[1]/button/span[1]')
    p3_x.click()

    # 把教室選擇列表叫出來
    p3_down = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tcTab_tpValidator_DropLstPlace"]')
    p3_down.click()

    # 教室列表
    switch = {'3F羽球室':1, '1F羽球室':2, 'B1桌球室':3, 'B1壁球室':4, 'B109教室(桌球)':5}
    which = switch.get(place)
    p3_name = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tcTab_tpValidator_DropLstPlace"]/option['+str(which)+']')
    p3_name.click()

     # 輸入想選的日期
    p3_date = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tcTab_tpValidator_DateTextBox"]')
    p3_date.send_keys(Date)

    # 按enter
    p3_enter = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tcTab_tpValidator_Button1"]')
    p3_enter.click()
    
    '''
    時間表
    '''
    # 按x
    p4_x = driver.find_element_by_xpath('/html/body/div/div[1]/button/span[1]')
    p4_x.click()
    
    '''
    點選時間，格式要對
    '''
    
    # 時間
    if choice[1]=='8:00':
        t = 2
    elif choice[1]=='9:00':
        t = 3
    elif choice[1]=='10:00':
        t = 4
    elif choice[1]=='11:00':
        t = 5
    elif choice[1]=='12:00':
        t = 6
    elif choice[1]=='13:00':
        t = 7
    elif choice[1]=='14:00':
        t = 8
    elif choice[1]=='15:00':
        t = 9
    elif choice[1]=='16:00':
        t = 10
    elif choice[1]=='17:00':
        t = 11
    elif choice[1]=='18:00':
        t = 12
    elif choice[1]=='19:00':
        t = 13
    elif choice[1]=='20:00':
        t = 14
    elif choice[1]=='21:00':
        t = 15
    else: 
        print('時間輸入格式錯誤')

    # 星期幾
    switch = {'Sun':2, 'Mon':2, 'Tue':3, 'Wed':4, 'Thu':5, 'Fri':6, 'Sat':7}
    w = switch.get(choice[0])
    
    # 製作xpath
    xp = '/html/body/form/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr[2]/td/table[2]'+'/tbody/tr['+str(t)+']/td['+str(w)+']/img'

    # 選定時間日期
    p4_choose = driver.find_element_by_xpath(xp)
    p4_choose.click()
    
    # 按x
    p5_x = driver.find_element_by_xpath('/html/body/div/div[1]/button/span[1]')
    p5_x.click()
    
    p5_email = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtEmail"]')
    p5_email.clear()
    p5_email.send_keys(email)
    
    p5_num = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtPlaceNum"]')
    p5_num.clear()
    p5_num.send_keys(number)
    
    img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_imgValidateCode"]'))

    with open("captcha.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))
    
    model = models.load_model('cnn_model.h5')
    
    def split_digits_in_img(img_array):
        x_list = []
        for i in range(4):
            step = img_cols // 4
            x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
        return x_list
    
    img_filename = 'captcha.png'
    img = load_img(img_filename, color_mode='grayscale')
    img_array = img_to_array(img)
    img_rows, img_cols, _ = img_array.shape
    x_list = split_digits_in_img(img_array)
    
    varification_code = []
    for i in range(4):
        confidences = model.predict(np.array([x_list[i]]), verbose=0)
        result_class = np.argmax(confidences, axis = 1)
        varification_code.append(result_class[0])
        result = ''
        for i in varification_code:
            if i > 9:
                result+= chr(i+55)
            else:
                result+= str(i)

    p5_cap = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtValidateCode"]')
    p5_cap.send_keys(result)

    p5_click = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnOrder"]')
    p5_click.click()

    time.sleep(60)
   
if __name__ == '__main__':
    WebConduct()