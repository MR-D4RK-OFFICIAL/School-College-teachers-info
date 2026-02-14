from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

def get_teacher_data(eiin):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Render-এ চালানোর জন্য ড্রাইভার সেটআপ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://www.emis.gov.bd/EMIS/Portal/Reports/TeacherSearch" 
    
    try:
        driver.get(url)
        time.sleep(2)
        
        # আপনার ইনপুট লজিক
        search_field = driver.find_element(By.ID, "txtEIIN") 
        search_field.send_keys(eiin)
        
        search_btn = driver.find_element(By.ID, "btnSearch")
        search_btn.click()
        
        time.sleep(4) # লোড হওয়ার জন্য একটু বেশি সময় দিন
        
        rows = driver.find_elements(By.XPATH, "//table[@id='teacherTable']/tbody/tr")
        teacher_list = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 1:
                teacher_list.append({
                    "name": cols[1].text,
                    "designation": cols[2].text,
                    "index": cols[3].text
                })
        return teacher_list
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    eiin = request.form.get('eiin')
    if not eiin:
        return jsonify({"error": "EIIN missing"})
    
    data = get_teacher_data(eiin)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
