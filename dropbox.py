import csv,argparse, sys, time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options    
from selenium.webdriver.common.by import By

def get_download_links(url,driver):
    links = []
    driver.get(url)
    time.sleep(5)    
    past_len = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        category_list = driver.find_elements(By.CLASS_NAME, "mc-table-row")

        if (past_len == len(category_list)):
            break
        else:
            past_len = len(category_list)    
    print("Total length: ",  past_len)
    category_list = driver.find_elements(By.CLASS_NAME, "mc-table-row")
    
    for k in category_list:
        try:
            link = k.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(link.replace("dl=0", "dl=1"))
        except:
            continue
    return links

def download(links,driver, last_download_number = -1):
    found_location = (last_download_number < 0)
    for link in links:
        if (not found_location):
            position = link.find("SPEAKER") 
            if (position>0):
                position += 7
                file_number = link[position: position +4]
                if (int(file_number) == last_download_number):
                    found_location = True
                    continue
                else:
                    continue
        driver.get(link)    
        time.sleep(20)

def main(argv=sys.argv[1:]):
    url = argv[0]
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument('--disable-site-isolation-trials')
    prefs = {'download.default_directory' : '/home/coe-ml-server/Downloads/PART1/DATA/CHANNEL1/WAVE'
            ,'profile.default_content_settings.popups': 0}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(ChromeDriverManager(version='102.0.5005.27').install(),options=chrome_options)
    time.sleep(5)
    download_links = get_download_links(url, driver)
    download(download_links,driver)

    # url = argv[1]
    # chrome_options = Options()
    # chrome_options.add_argument("user-data-dir=selenium")
    # chrome_options.add_argument('--disable-site-isolation-trials')
    # prefs = {'download.default_directory' : '/home/coe-ml-server/Downloads/PART1/DATA/CHANNEL1/WAVE'
    #         ,'profile.default_content_settings.popups': 0}
    # chrome_options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(ChromeDriverManager(version='102.0.5005.27').install(),options=chrome_options)
    # time.sleep(5)
    # download_links = get_download_links(url, driver)
    # download(download_links,driver)


    # time.sleep(100000)
    # driver.quit()

main()
