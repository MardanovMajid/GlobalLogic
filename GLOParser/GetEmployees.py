from selenium import webdriver
import ruamel.yaml as yaml
import pandas as pd 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import sys

for i in range(1, len(sys.argv)):
    yamlPath = sys.argv[i]

with open(yamlPath) as info:
      info_dict = yaml.load(info, Loader=yaml.Loader)

# credentials
username = info_dict['username']
password = info_dict['password']
mainURL = info_dict['mainURL']
driverPath = info_dict['driverPath']
csvPath = info_dict['csvPath']

manager_first_name = info_dict['managerFirstName']
manager_last_name = info_dict['managerLastName']

s = Service(driverPath)
driver = webdriver.Chrome(service=s)
driver.get(mainURL)

#wait for login page
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"login")))
UNBox = driver.find_element(By.ID,"login")
UNBox.send_keys(username)
PWBox = driver.find_element(By.ID,"password")
PWBox.send_keys(password)

#sign in and wait for profile  downloaded
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.btn-block[type='submit']"))).click()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div.content > div > div > div:nth-child(3) > div > div.sidebar.left-side.pull-left > div:nth-child(1) > div > div > div.profile-widget-content > h2")))

# type manager full name
driver.find_element(By.CSS_SELECTOR,"#advance-search-link").click()
driver.find_element(By.CSS_SELECTOR,"#manager").send_keys(manager_first_name+' '+manager_last_name)

#select manager and press serach
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-id-1"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_advanced_search"))).click()

#driver.get("https://glo.globallogic.com/search/advanced?advanced_search%5Becode%5D=&advanced_search%5Bemail%5D=&advanced_search%5Bdisplayname%5D=&advanced_search%5Bmanager_id%5D=45010&advanced_search%5Bmanager_type%5D=reporting_manager&advanced_search%5Bhierarchy_number%5D=all&advanced_search%5Blocation%5D%5B%5D=27&advanced_search%5Bjob_family_id%5D%5B%5D=Select+All&advanced_search%5Bjob_family_id%5D%5B%5D=3&advanced_search%5Bjob_family_id%5D%5B%5D=21&advanced_search%5Bjob_family_id%5D%5B%5D=31&advanced_search%5Bjob_family_id%5D%5B%5D=16&advanced_search%5Bjob_family_id%5D%5B%5D=9&advanced_search%5Bjob_family_id%5D%5B%5D=15&advanced_search%5Bjob_family_id%5D%5B%5D=20&advanced_search%5Bjob_family_id%5D%5B%5D=32&advanced_search%5Bjob_family_id%5D%5B%5D=35&advanced_search%5Bjob_family_id%5D%5B%5D=1&advanced_search%5Bjob_family_id%5D%5B%5D=17&advanced_search%5Bjob_family_id%5D%5B%5D=4&advanced_search%5Bjob_family_id%5D%5B%5D=22&advanced_search%5Bjob_family_id%5D%5B%5D=19&advanced_search%5Bjob_family_id%5D%5B%5D=23&advanced_search%5Bjob_family_id%5D%5B%5D=27&advanced_search%5Bjob_family_id%5D%5B%5D=6&advanced_search%5Bjob_family_id%5D%5B%5D=30&advanced_search%5Bjob_family_id%5D%5B%5D=10&advanced_search%5Bjob_family_id%5D%5B%5D=7&advanced_search%5Bjob_family_id%5D%5B%5D=11&advanced_search%5Bjob_family_id%5D%5B%5D=33&advanced_search%5Bjob_family_id%5D%5B%5D=12&advanced_search%5Bjob_family_id%5D%5B%5D=34&advanced_search%5Bjob_family_id%5D%5B%5D=28&advanced_search%5Bjob_family_id%5D%5B%5D=5&advanced_search%5Bjob_family_id%5D%5B%5D=24&advanced_search%5Bjob_family_id%5D%5B%5D=29&advanced_search%5Bjob_family_id%5D%5B%5D=13&advanced_search%5Bjob_family_id%5D%5B%5D=25&advanced_search%5Bjob_family_id%5D%5B%5D=14&advanced_search%5Bjob_family_id%5D%5B%5D=8&advanced_search%5Bjob_family_id%5D%5B%5D=18&advanced_search%5Bjob_family_id%5D%5B%5D=26&advanced_search_designation=&advanced_search_corporate_directory=&advanced_search_team=&advanced_search%5Bdate_pick_day%5D=1&advanced_search%5Bdate_pick_month%5D=1&advanced_search%5Bsearch_birthday_by%5D=birthday_month_option&advanced_search%5Bbirthday_month%5D=&advanced_search%5Bexact_date%5D=&advanced_search%5Bsearch_by_date%5D=range&advanced_search%5Bdate_from%5D=&advanced_search%5Bdate_to%5D=&advanced_search%5Bphone%5D=&advanced_search%5Bvoip_extension%5D=&advanced_search%5Binterests%5D=")

#wait for full user list is appeared
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"user_list")))

# get users profile url list
elems = driver.find_elements(By.CSS_SELECTOR,"a.card-pic.pull-left.pull-left")

#user_list > div > div:nth-child(1)
all_links = [elem.get_attribute('href') for elem in elems]
links = [*set(all_links)]

l_primary_skills =[]
l_secondary_skills =[]
l_profile_urls=[]
l_fullnames=[]

#run crowler for each profile url
for profile_url in links:              
    driver.get(profile_url)
    #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#profile-layer > div > div > div.col-sm-8.user-info > div > h2 > a")))
    fullname = driver.find_element(By.CSS_SELECTOR,"#profile-layer > div > div > div.col-sm-8.user-info > div > h2 > a").text
    try:
     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "career_link"))).click()
     primary_skill = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#skills_mappings_view > div.row > div:nth-child(1) > div > div > p"))).text
     secondary_skill = driver.find_element(By.CSS_SELECTOR,"#skills_mappings_view > div.row > div:nth-child(2) > div > div > p").text
    
    except : 
     primary_skill = ""
     secondary_skill = ""
     
# populate array with parsed data     
    l_fullnames.append(fullname)
    l_primary_skills.append(primary_skill)
    l_secondary_skills.append(secondary_skill)
    l_profile_urls.append(profile_url)

#export populated array to csv file
d = {'Full Name': l_fullnames,'Primary Skills':l_primary_skills,'Secondary Skills':l_secondary_skills,'Profile URL':l_profile_urls}
pd.DataFrame(d).to_csv(csvPath, index=None)
driver.close()



