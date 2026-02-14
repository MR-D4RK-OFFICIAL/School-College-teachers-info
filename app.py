from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_teacher_data(eiin):
    options = Options()
    options.add_argument("--headless") # ব্রাউজার না খুলেই কাজ করবে
    driver = webdriver.Chrome(options=options)
    
    # EMIS এর নির্দিষ্ট সার্চ পেজ (উদাহরণস্বরূপ)
    url = "https://www.emis.gov.bd/EMIS/Portal/Reports/TeacherSearch" 
    driver.get(url)
    
    try:
        # EIIN ইনপুট ফিল্ড খুঁজে বের করা (আইডি সাইট অনুযায়ী পরিবর্তন হতে পারে)
        search_field = driver.find_element(By.ID, "txtEIIN") 
        search_field.send_keys(eiin)
        
        # সার্চ বাটনে ক্লিক
        search_btn = driver.find_element(By.ID, "btnSearch")
        search_btn.click()
        
        time.sleep(3) # ডাটা লোড হওয়ার সময় দিন
        
        # রেজাল্ট টেবিল থেকে তথ্য নেওয়া
        rows = driver.find_elements(By.XPATH, "//table[@id='teacherTable']/tbody/tr")
        teacher_list = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            teacher_list.append({
                "name": cols[1].text,
                "designation": cols[2].text,
                "mobile": cols[3].text # যদি মোবাইল নম্বর পাবলিক থাকে
            })
        return teacher_list
    finally:
        driver.quit()
