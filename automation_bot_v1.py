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
from bs4 import BeautifulSoup
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
        self.cookie = None
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
        print("Validating csv file...")
        logging.info("Validating csv file.")
        if not os.path.exists("entries.csv"):
            print("entries.csv not found.")
            print("See script.log for more information.")
            logger.error("'entries.csv' not found.")
            logger.info("Make sure 'entries.csv' is in the same directory as the script. Check filename if you have misspeled and a '.csv' extension.")
            return False
        
        with open("entries.csv", "r") as file:
            reader = csv.reader(file)
            for row, entry in enumerate(reader):
                if len(entry) > 5 or len(entry) < 4:
                    print(f"Invalid entry in 'entries.csv' at row {row+1}.")
                    print("See script.log for more information.")
                    logger.error(f"Invalid entry in 'entries.csv' at row {row+1}.")
                    logger.info("Make sure each entry has 4 columns: 'Search String' and three of 'Jurisdiction'.")
                    return False
                for i in range(1, 4):
                    if entry[i] not in self.config["available_jurisdiction"]:
                        print(f"Invalid Jurisdiction in 'entries.csv' at row {row+1}.")
                        print("See script.log for more information.")
                        logger.error(f"Invalid Jurisdiction in 'entries.csv' at row {row+1}.")
                        logger.info(f"Make sure each jurisdiction is one of {self.config['available_jurisdiction']}.")
                        return False
                        
                    if entry[i] in entry[i+1:]:
                        print(f"Repeated Jurisdiction in 'entries.csv' at row {row+1}.")
                        print("See script.log for more information.")
                        logger.error(f"Repeated Jurisdiction in 'entries.csv' at row {row+1}.")
                        logger.info("Make sure each jurisdiction is not repeated in same entry.")
                        return False
                    self.search_queries.append([
                        entry[0], 
                        entry[1], 
                        entry[2], 
                        entry[3], 
                        entry[4] if len(entry) == 5 and entry[4] else None
                    ])
        logging.info("Validated csv file successfully. All entries are valid.")
        print("Validated csv file successfully.")
        print(f"Total {len(self.search_queries)} entries found.")
        return True
    
    def obtain_cookie(self):
        
        # Initialize the Chrome driver
        if self.config["use_chromedriver"]:
            print("Using custom chromedriver because 'use_chromedriver' is set to True in config.json.")
            if os.path.exists("chromedriver"):
                service = Service('chromedriver')
            else:  
                print("chromedriver not found in the current directory.")
                print("Please download chromedriver and place it in the current directory.")
                print("See why are you dealing this: https://github.com/tensor35/judicial_records_scrapper/issues/1#issue-2465488039")
                print("See script.log for more information.")
                logger.error("chromedriver not found in the current directory.")
                logger.info("Please download chromedriver and place it in the current directory.")
                logger.info("Download chromedriver from https://chromedriver.chromium.org/downloads")
                print("Exiting...")
                return False
        else:
            service = Service()
        # Set up Chrome options for downloading
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        
        
        try:
            self.driver= webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Initialized chromedriver successfully.")
            print("Initialized chromedriver successfully.")
        except Exception as e:
            logger.error(f"Error initializing chromedriver: {e}")
            print("Error initializing chromedriver.")
            print("See script.log for more information")
            print("If it says: 'Unable to obtain chromedriver', Visit; https://github.com/tensor35/judicial_records_scrapper/issues/1#issue-2465488039.")
            print("Exiting...")
            return False
        
        try:
            # Navigating to URL
            self.driver.get(self.search_page_url)
            logger.info(f"Navigated to Search page.")
        except Exception as e:
            logger.error("Failed navigating to Search Page")
            self.driver.quit()
            return False
        
        # get the cookie named JSESSIONID
        cookie = self.driver.get_cookie("JSESSIONID")
        if cookie:
            logger.info(f"Cookie JSESSIONID: {cookie}")
            self.cookie = cookie["value"]
        else:
            logger.error("Failed to get cookie JSESSIONID.")
            self.driver.quit()
            return False
        
        self.driver.quit()
        return True
    
    def clear(self):
        os.system('clear')
        print(colorama.Fore.CYAN + colorama.Style.BRIGHT)
        print(self.config["heading"])
        
    def start(self):
        self.clear()
        print("Welcome to the Automation Bot.")
        print("For good GUI Experiece, Please maximize the terminal window.")
        input("Press Enter to continue...")
        self.clear()
        print("If you need any information, please refer to official git repo.")
        print("In case of any issues/error, See script.log and report to developer or create an issue on git repo.")
        input("Press Enter to Start the bot...")
        self.clear()
        
        # Validating csv file
        if( not self.validate_csv()):
            print("Make sure 'entries.csv' exists and is valid.")
            print("Exiting...")
            return
        
        self.obtain_cookie()
        
        input("All set. Press Enter to start the bot.")
        self.clear()
        for index in range(len(self.search_queries)):
            if self.cookie == None:
                self.obtain_cookie()
            print(self.search_queries[index])
            if self.search_queries[index][4] != None:
                continue
            print(index)
            result = self.get_total_results(index)  
            print("Result: ", result)
            if result == False:
                continue
            self.search_queries[index][4] = result
            with open("entries.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.search_queries)


        print("All queries completed.")

    
    def get_total_results(self, index):
        
        search_record = self.search_queries[index]
        search_string = search_record[0]
        jurisdiction1 = search_record[1]
        jurisdiction2 = search_record[2]
        jurisdiction3 = search_record[3]
        
        print("Searching for: ", search_string, " in jurisdictions: ", jurisdiction1 + ", " + jurisdiction2 + ", " + jurisdiction3+":" , end=" ")
    
        import requests

        # Define the URL and parameters
        url = 'https://www.poderjudicial.es/search/search.action'
        params = {
            'action': 'query',
            'sort': 'IN_FECHARESOLUCION:decreasing',
            'recordsPerPage': 10,
            'databasematch': 'AN',
            'start': 1,
            'TEXT': f'{search_string}',
            'JURISDICCION': f'|{jurisdiction1}||{jurisdiction2}||{jurisdiction3}'
        }

        # Define the headers
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'JSESSIONID={self.cookie}',
            'Host': 'www.poderjudicial.es',
            'Origin': 'https://www.poderjudicial.es',
            'Referer': 'https://www.poderjudicial.es/search/indexAN.jsp',
            'Sec-CH-UA': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Sec-CH-UA-Mobile': '?1',
            'Sec-CH-UA-Platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Send the POST request
        response = requests.post(url, data=params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the number of results
            numhits_div = soup.find('div', class_='col-md-5 numhits hidden-xs')
            if numhits_div:
                # Extract the number of results
                results_text = numhits_div.get_text(strip=True)
                # Extract only the number using regular expressions
                import re
                match = re.search(r'\d+', results_text)
                if match:
                    num_results = match.group()
                    print(f'{num_results}')
                else:
                    print('Number of results not found in the response.')
                    return False
            else:
                print(0)
                return "0"
        elif(response.status_code == 403):
            print("Failed to retrieve content. Status Code: 403")
            print("Cookie might have expired. Trying to obtain new cookie...")
            self.cookie = None
            return False
           
        else:
            print(f'Failed to retrieve content. Status Code: {response.status_code}')
            return False
        
        return num_results       

        
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    new_bot = AutomamtionBot()
    new_bot.start()
    
    
    
    
    
    
    #  Reload the page
        # self.driver.refresh()
        
        
        # # Wait for the page to load
        # try:
        #     WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "jurisprudenciasearch"))
        #     )
        #     logger.info("Page loaded successfully.")
        # except Exception as e:
        #     logger.error(f"Failed loading page: {e}")
        #     return
        
        
        
        # # # Obtaining Searchbox element
        # # try:
        # #     search_box = WebDriverWait(self.driver, 10).until(
        # #         EC.presence_of_element_located((By.ID, "frmBusquedajurisprudencia_TEXT"))
        # #     )
        # #     logger.info("SearchBox Located.")
        # # except Exception as e:
        # #     logger.error(f"Failed to Obtain SearchBox Instance: {e}")
        # #     return
        
        # # # Obtain Criteria Dropdown with data-original-title="Todas"
        # # try:
        # #     dropdown = WebDriverWait(self.driver, 10).until(
        # #         EC.presence_of_element_located((By.XPATH, "//button[@data-original-title='Todas']"))
        # #     )
        # #     logger.info("Criteria Dropdown Located.")
        # # except Exception as e:
        # #     logger.error(f"Failed to Obtain Criteria Dropdown Instance: {e}")
        # #     return
        
        # # # Find all jurisdictions
        # # for i in range(1, 4):
        # #     try:
        # #         jurisdiction = WebDriverWait(self.driver, 10).until(
        # #             EC.presence_of_element_located((By.XPATH, f"//ul[@class='multiselect-container dropdown-menu']//li//label[contains(text(), '{search_record[i]}')]"))
        # #         )
        # #         logger.info(f"Jurisdiction {i} Located.")
        # #     except Exception as e:
        # #         logger.error(f"Failed to Locate Jurisdiction {i}: {e}")
        # #         return
        
        # # # Locating Submit Button
        # # try:
        # #     submit_button = WebDriverWait(self.driver, 10).until(
        # #         EC.presence_of_element_located((By.ID, "srcjur_search"))
        # #     )
        # #     logger.info("Submit button Located.")
        # # except Exception as e:
        # #     logger.error(f"Failed to locate Submit button: {e}")
        # #     return
        
        # # # Enter data in form
        # # try:
        # #     search_box.send_keys(search_string)
        # #     search_box.send_keys("\n")
        # #     time.sleep(100)
        # #     dropdown.click()
        # #     time.sleep(0.5)
        # #     jurisdiction1.click()
        # #     jurisdiction2.click()
        # #     jurisdiction3.click()
        # #     time.sleep(0.5)
        # #     submit_button.click()
        # #     logger.info("Form submitted successfully.")
        # # except Exception as e:
        # #     logger.error(f"Failed to submit form: {e}")
        # #     return
            
        
        
        