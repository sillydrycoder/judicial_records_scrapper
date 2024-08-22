import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import requests
from bs4 import BeautifulSoup
import re

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
    def __init__(self, gui_logger, update_progress):
        self.page_url = "https://www.poderjudicial.es/search/indexAN.jsp"
        self.gui_logger = gui_logger
        self.update_progress = update_progress
        
    def obtain_cookie(self):
        
        # Initialize the Chrome driver
        if os.path.exists("chromedriver"):
            service = Service('chromedriver')
        else:  
            service = Service()
            
        self.update_progress(10)
            
        # Set up Chrome options for downloading
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        
        self.gui_logger.set("Initializing Bot...")
        self.update_progress(20)

        try:
            self.driver= webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Initialized chromedriver successfully.")
            self.update_progress(50)
        except Exception as e:
            logger.error(f"Error initializing chromedriver: {e}")
            self.gui_logger.set("Error with chromedriver. You should check 'script.log'.")
            return False

        try:
            # Navigating to URL
            self.driver.get(self.page_url)
            logger.info(f"Navigated to Search page.")
            self.update_progress(80)

        except Exception as e:
            logger.error("Failed navigating to Search Page")
            self.gui_logger.set("Error while loading page. You should check 'script.log'.")
            self.driver.quit()
            return False
        
        # get the cookie named JSESSIONID
        cookie = self.driver.get_cookie("JSESSIONID")
        if cookie:
            logger.info(f"Cookie JSESSIONID: {cookie}")
            self.update_progress(100)
            cookie = cookie["value"]
        else:
            logger.error("Failed to get cookie JSESSIONID.")
            self.gui_logger.set("Failed to get cookie. You should check 'script.log'.")
            self.driver.quit()
            return False
        
        self.driver.quit()
        return cookie

    
    def get_total_results(self, search_string, selected_jurisdictions, cookie):
        # Define the URL and parameters
        url = 'https://www.poderjudicial.es/search/search.action'
        judiction_string = ""
        for jurisdiction in selected_jurisdictions:
            judiction_string += f"|{jurisdiction}|"
        params = {
            'action': 'query',
            'sort': 'IN_FECHARESOLUCION:decreasing',
            'recordsPerPage': 10,
            'databasematch': 'AN',
            'start': 1,
            'TEXT': search_string,
        }

        if selected_jurisdictions:
            params['JURISDICCION'] = judiction_string
            
        # Define the headers
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'JSESSIONID={cookie}',
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
            numhits_div = soup.find('div', class_=re.compile(r'col-md-(5|7)\snumhits\s'))
            if numhits_div:
                # Extract the number of results
                results_text = numhits_div.get_text(strip=True)
                # Extract only the number using regular expressions
                match = re.search(r'\d+', results_text)
                if match:
                    num_results = match.group()
                else:
                    logger.error("Failed to extract number of results.")
                    return False
            else:
                return "0"
        elif(response.status_code == 403):
            logger.error("Failed to get results. Forbidden.")
            return False
           
        else:
            return False
        
        return num_results       
    