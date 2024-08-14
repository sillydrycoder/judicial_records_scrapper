import logging
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import colorama
import json
import os
import re
from sys import platform

colorama.init()

# Configure logging
log_file = 'script.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
    ]
)

logger = logging.getLogger(__name__)


class AutomamtionBot:
    def __init__(self):
        self.search_page_url = "https://www.poderjudicial.es/search/indexAN.jsp"
        self.search_queries = []
        with open ("config.json", "r") as file:
            config = json.load(file)
            self.config = config
        
    def close_chrome_windows():
        current_os = platform.system()
        
        if current_os == "Windows":
            os.system("taskkill /F /IM chrome.exe /T")
        elif current_os == "Darwin":  # macOS
            os.system("pkill -a -i 'Google Chrome'")
        elif current_os == "Linux":
            os.system("pkill chrome")
        else:
            print(f"Unsupported OS: {current_os}")            

    def validate_csv(self):
        logging.info("Validating csv file.")
        if not os.path.exists("entries.csv"):
            logger.error("'entries.csv' not found.")
            logger.info("Make sure 'entries.csv' is in the same directory as the script. Check filename if you have misspeled and a '.csv' extension.")
            return False
        
        with open("entries.csv", "r") as file:
            reader = csv.reader(file)
            for row, entry in enumerate(reader):
                if len(entry) > 5 or len(entry) < 4:
                    logger.error(f"Invalid entry in 'entries.csv' at row {row+1}.")
                    logger.info("Make sure each entry has 4 columns: 'Search String' and three of 'Jurisdiction'.")
                    return False
                for i in range(1, 4):
                    if entry[i] not in self.config["available_jurisdiction"]:
                        logger.error(f"Invalid Jurisdiction in 'entries.csv' at row {row+1}.")
                        logger.info(f"Make sure each jurisdiction is one of {self.config['available_jurisdiction']}.")
                        return False
                        
                    if entry[i] in entry[i+1:]:
                        logger.error(f"Repeated Jurisdiction in 'entries.csv' at row {row+1}.")
                        logger.info("Make sure each jurisdiction is not repeated in same entry.")
                        return False
                self.search_queries.append([entry[0], entry[1], entry[2], entry[3]])
        logging.info("Validated csv file successfully. All entries are valid.")
        return True
        
    def start(self):
        os.system('clear')
        print(colorama.Fore.CYAN + colorama.Style.BRIGHT)
        print(self.config["heading"])
        self.validate_csv()
        for index in range(len(self.search_queries)):
            self.get_total_results(index)  
    
    def get_total_results(self, index):
        
        search_record = self.search_queries[index]
        search_string = search_record[0]
        jurisdiction1 = search_record[1]
        jurisdiction2 = search_record[2]
        jurisdiction3 = search_record[3]
        
        if self.config["use_chromedriver"]:
            service = Service('chromedriver')
        else:
            service = Service()
        service = Service(os.path.join(os.getcwd(), "chromedriver"))
        # Set up Chrome options for downloading
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless=new")
        # Initialize the Chrome driver
        
        
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Initialized Chrome driver successfully.")
        except Exception as e:
            logger.error(f"Error initializing Chrome driver: {e}")
            return

        try:
            # Navigating to URL
            driver.get(self.search_page_url)
            logger.info(f"Navigated to Search page.")
        except Exception as e:
            logger.error("Failed navigating to Search Page")
            driver.quit()
            return

        # Wait for the page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "jurisprudenciasearch"))
            )
            logger.info("Page loaded successfully.")
        except Exception as e:
            logger.error(f"Failed loading page: {e}")
            driver.quit()
            return
        
        # Obtaining Searchbox element
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "frmBusquedajurisprudencia_TEXT"))
            )
            logger.info("SearchBox Located.")
        except Exception as e:
            logger.error(f"Failed to Obtain SearchBox Instance: {e}")
            driver.quit()
            return
        
        # Obtain Criteria Dropdown with data-original-title="Todas"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-original-title='Todas']"))
            )
            logger.info("Criteria Dropdown Located.")
        except Exception as e:
            logger.error(f"Failed to Obtain Criteria Dropdown Instance: {e}")
            driver.quit()
            return
        
        # Locating Submit Button
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "srcjur_search"))
            )
            logger.info("Submit button Located.")
        except Exception as e:
            logger.error(f"Failed to locate Submit button: {e}")
            driver.quit()
            return
        
        

        
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    new_bot = AutomamtionBot()
    new_bot.start()
    