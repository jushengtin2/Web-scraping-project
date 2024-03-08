from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.by import By
chrome_options = webdriver.ChromeOptions()
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from selenium.webdriver.support import expected_conditions as EC
import re



def call():  
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")           #不会显示用户界面
    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://warrant.kgi.com/EDWebSite/Views/StrategyCandidate/MarketStatistics.aspx'  
    driver.get(url)
        
    time.sleep(0.5)
    
    elements = driver.find_elements(By.TAG_NAME, 'input')
    for element in elements:
        if element.get_attribute("value")=="divRankInFrontByDealVolume":  #轉到可以跳躍的表格網址
            element.click()


    twenty_big_list = []
    money= []


    for i in range(20):    #找出目前前20名的編號

        wait = WebDriverWait(driver, 10)
        xpath = f'//*[@id="grdRankInFrontByDealVolume"]/tr[{i+1}]/td[3]/a'
        link = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        href_value = link.get_attribute('href')[-10:]   #編號在最後七碼但我發現有八碼的
        href_value = re.sub(r'\D', '', href_value)
        twenty_big_list.append(href_value)   
        
        
        xpath = f'//*[@id="grdRankInFrontByDealVolume"]/tr{[i+1]}/td[8]'
        link = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        money.append(link.text) 
      
    
    result=[]
    
    xpath = '//*[@id="lbRankInFrontByDealVolumeDate"]' 
    timee = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    the_time = timee.text

    i=0
    for item in twenty_big_list[:11] :

        url = f'https://warrant.kgi.com/EDWebSite/Views/WarrantAnalyzer/WarrantAnalyzerIframe.aspx?Insnbr={item}' 
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        rate = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'auto-style8')))
        
        
        if(float(rate[6].text[:4])<=10.0):
            name_num = driver.find_element(by=By.ID, value='warrantData')
            rows = name_num.find_elements(by=By.CLASS_NAME, value='it-fix')

            name_num2 = driver.find_element(by=By.ID, value='underlyingData')
            rows2 = name_num2.find_elements(by=By.CLASS_NAME, value='it-fix')
            
            for cell in rows:   #權證代碼 權證名稱 權證成交價 權證成交量(張) 權證成交值(元)
                number_name = [cell.text.split(" ")[ii] for ii in [0, 1, 6, 7] ]
                
            for cell in rows2:
                number_name2 = cell.text.split(" ")[:2]
            temp_result = number_name + number_name2 
            #print(item+" "+ str(name_num[:2]))
            temp = temp_result[-2:]  # 获取最后两个元素
            temp_result[2:2] = temp  # 在索引2的位置插入
            del temp_result[-2:]  # 删除原来最后两个元素的位置
            
            temp_result.append(money[i])
            result.append(temp_result)

        
        i=i+1
    
    return result, the_time

window =tk.Tk()
window.minsize(600,400)


def show_hello():
    final_result, the_time = call()

    formatted_result = "\n".join(str(d) for d in final_result)
    label3.config(text = the_time)
    label6.config(text = formatted_result)


frame = tk.Frame(window)
label1 = tk.Label(window,height=1)
label2 = tk.Label(window, text="")
button = tk.Button(window, text="流通在外比例<=10%", command=show_hello, padx=30, pady=30)


label3 = tk.Label(window, text="")
label4 = tk.Label(window, text="")
label5 = tk.Label(window, text="權證代碼 權證名稱 標的代碼 標的名稱 權證成交價 權證成交量(張) 權證成交值(元)")
label6 = tk.Label(window, text="")
label7 = tk.Label(window, text="")
label8 = tk.Label(window, text="")
label9 = tk.Label(window, text="")
label10 = tk.Label(window, text="")


label1.pack()
label2.pack()
button.pack()
label3.pack()
label4.pack()
label5.pack()
label6.pack()
label7.pack()
label8.pack()
label9.pack()
label10.pack()



window.mainloop()

