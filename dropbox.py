import csv,argparse, sys, time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options    
from selenium.webdriver.common.by import By
import re

def download_all(url: str, storage_path: str, starting_number = -1) -> None:
    """
    Downloading all the files in the url provided

    Args:
        url (str): url to scrap
        storage_path (str): base storage path
    """

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument('--disable-site-isolation-trials')
    prefs = {'download.default_directory' : storage_path
            ,'profile.default_content_settings.popups': 0}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(ChromeDriverManager(version='102.0.5005.27').install(),options=chrome_options)
    time.sleep(1)
    driver.get(url)
    time.sleep(2)
    past_len = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        category_list = driver.find_elements(By.CLASS_NAME, "mc-table-row")

        if (past_len == len(category_list)):
            break
        else:
            past_len = len(category_list)    

    download_file_links, folder_links = get_links(driver, starting_number)
    print("Total files in path: ", url, " : ",  len(download_file_links), " and folder ", len(folder_links))
    download_links(download_file_links,driver)
    print("Download for url: ", url, " done.")
    if (len(download_file_links)>0):
        time.sleep(4) 
    driver.quit()
    for file_name, url in folder_links.items():
        download_all(url, storage_path+"/"+file_name)

def get_links(driver:webdriver, starting_number=-1):
    """
    Get all the download links in the current driver page

    Args:
        dict (_type_): _description_

    Returns:
        _type_: (list, dictionary) for download_links and folder_links
    """
    download_links = []
    folder_links = {} 
    table_body = driver.find_element(By.CLASS_NAME, "mc-table-body")
    category_list = table_body.find_elements(By.CLASS_NAME, "mc-table-row")

    for k in category_list:
        try:
            link = k.find_element(By.TAG_NAME, "a").get_attribute("href")
            position = link.find("Audio/")
            if (position>=0 and int(link[position+6: position+10])>=starting_number):    
                if(re.search(".txt|.TXT|.wav|.pdf|.docx|.zip|.XLSX|.xlsx|.TextGrid|.m4a",link)):
                    download_links.append(link.replace("dl=0", "dl=1"))
                else:
                    folder_name = k.find_element(By.CLASS_NAME, "mc-media-cell-text").text
                    folder_links[folder_name] = link
        except:
            continue
    return download_links, folder_links

def download_links(links, driver, pause_time = 8, starting_number = 4193):
    for link in links:  
        driver.get(link)        
        if(re.search(".txt|.TXT|.pdf|.docx|.XLSX|.TextGrid",link)):
            time.sleep(4)  
        elif(re.search(".wav|.zip|.m4a",link)):
            time.sleep(pause_time)
        else:
            time.sleep(pause_time)
            

def main(argv=sys.argv[1:]):
    base_url = "https://www.dropbox.com/scl/fo/d1a3m52yc5ddxdh3a8xnu/h/IMDA%20-%20National%20Speech%20Corpus%20(Additional)/PART6/Call%20Centre%20Design%203/Audio?dl=0&subfolder_nav_tracking=1"
    storage_path = "/home/coe-ml-server/Downloads/additional_files/PART6/Call Centre Design 3/Audio"
    download_all(base_url, storage_path,1839)
main()
