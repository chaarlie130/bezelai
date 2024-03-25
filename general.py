from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse
from googletrans import Translator
import json  # For working with JSON data

#BEST SELLERS = https://www.aliexpress.com/gcp/300001064/aptaxwR82N
#ELECTRONICS = https://www.aliexpress.com/p/calp-plus/index.html?categoryTab=US_electronics
#PET SUPPLIES = https://www.aliexpress.com/p/calp-plus/index.html?categoryTab=us_pet_supplies



def trim_title(title, num_words=5):
    return ' '.join(title.split()[:num_words])


def updateProducts(x=None):
    if x is None:
        x = input("""Select a niche:
            1. general
            2. beauty & health
            3. electronics
            4. us women's clothing
            5. toys & games
            6. pet supplies
            """)

    # Convert the input to an integer for comparison
    try:
        x = int(x)  # Convert string input to integer
    except ValueError:
        print("Please enter a valid number.")
        exit()

    # Assign the niche based on the input
    if x == 1:
        niche = 'general'
    elif x == 2:
        niche = 'bad'
    elif x == 3:
        niche = 'bad'
    elif x == 4:
        niche = 'bad'
    elif x == 5:
        niche = 'bad'
    elif x == 6:
        niche = 'bad'
    else:
        print("Invalid selection. Please select a number between 1 and 6.")
        exit()
    if niche == 1:
        # Create a translator object
        translator = Translator()

        # Set up the Selenium WebDriver options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in the background
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")  # Set log level to suppress informational messages
        chrome_options.add_argument('--disable-gpu')  # Recommended for headless
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress WebDriver logging

        # Initialize the WebDriver with the configured options
        service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = 'https://www.aliexpress.com/gcp/300001064/aptaxwR82N'
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Get page source and set up BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Load existing data from db.json
        with open('db.json', 'r', encoding='utf-8') as file:
            db = json.load(file)
            
        db["winningProducts"]["general"]["products"] = []
        # Counter for product IDs
        product_counter = len(db["winningProducts"]["general"]["products"]) + 1

        # Find all product elements and extract info
        products = soup.find_all('a', {'class': 'productContainer'})
        for product in products:
            title_element = product.find('span', {'class': 'AIC-T-text'})
            title = title_element.get_text(strip=True) if title_element else 'No Title Available'
            translated_title = trim_title(translator.translate(title, dest='en').text)
            
            full_link = product.get('href')
            parsed_link = urlparse(full_link)
            clean_link = f'https://{parsed_link.netloc}{parsed_link.path}'

            img_element = product.find('img', {'class': 'item-card-img'})
            img_src = 'https:' + img_element['src'] if img_element else 'No Image Available'

            # Construct the product data structure
            product_data = {
                "id": f"gen{product_counter:03d}",
                "name": translated_title,
                "description": "No description available",  # Placeholder, as description isn't provided by your scraping
                "price": 0,  # Placeholder, as price isn't provided by your scraping
                "currency": "USD",  # Assuming USD, adjust as necessary
                "imageUrl": img_src,
                "productUrl": clean_link
            }

            # Append product to the database
            db["winningProducts"]["general"]["products"].append(product_data)
            product_counter += 1

        # Write the updated data back to db.json
        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(db, file, ensure_ascii=False, indent=4)

        # Close the WebDriver
        driver.quit()

    else:
        # Create a translator object
        translator = Translator()

        # Set up the Selenium WebDriver options
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Run browser in the background
        chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.add_argument("--log-level=3")  # Set log level to suppress informational messages
        #chrome_options.add_argument('--disable-gpu')  # Recommended for headless
        #chrome_options.add_argument('--disable-extensions')
        #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress WebDriver logging

        # Initialize the WebDriver with the configured options
        service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        if niche != 'bad':
            url = f"https://www.aliexpress.com/p/calp-plus/index.html?categoryTab=US_{niche}"
        else:
            if x == 4: #WOMEN'S CLOTHING
                url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.categorymp.allcategoriespc.16.60c5q2Qgq2QgQW&categoryTab=us_women%27s_clothing'
                niche = 'women%27s_clothing'
            if x == 2: #BEAUTY & HEALTH
                url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.categorymp.allcategoriespc.1.2585xIQ0xIQ07h&categoryTab=us_beauty_%2526_health'
                niche = 'beauty_%2526_health'
            if x == 5: #TOYS & GAMES
                url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.categorymp.allcategoriespc.7.3e88uU9quU9qcC&categoryTab=us_toys_%2526_games'
                niche = 'toys_%2526_games'
            if x == 6:
                url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.categorymp.allcategoriespc.11.79a8iGiwiGiwTo&categoryTab=us_pet_supplies'
                niche = 'pet_supplies'
            if x == 3:
                url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.categorymp.allcategoriespc.10.24d4c2qVc2qVgW&categoryTab=us_electronics'
                niche = 'electronics'
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Get page source and set up BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Load existing data from db.json
        with open('db.json', 'r', encoding='utf-8') as file:
            db = json.load(file)
            
        db["winningProducts"][niche]["products"] = []
        # Counter for product IDs
        product_counter = len(db["winningProducts"][niche]["products"]) + 1

        # Find all product elements and extract info
        products = soup.find_all('a', {'class': '_1UZxx'})
        for product in products:
            title_element = product.find('h3', {'class': 'nXeOv'})
            title = title_element.get_text(strip=True) if title_element else 'No Title Available'
            translated_title = trim_title(translator.translate(title, dest='en').text)
            
            full_link = product.get('href')
            parsed_link = urlparse(full_link)
            clean_link = f'https://{parsed_link.netloc}{parsed_link.path}'

            img_element = product.find('img', {'class': 'product-img'})
            img_src = 'https:' + img_element['src'] if img_element else 'No Image Available'

            # Construct the product data structure
            product_data = {
                "id": f"gen{product_counter:03d}",
                "name": translated_title,
                "description": "No description available",  # Placeholder, as description isn't provided by your scraping
                "price": 0,  # Placeholder, as price isn't provided by your scraping
                "currency": "USD",  # Assuming USD, adjust as necessary
                "imageUrl": img_src,
                "productUrl": clean_link
            }

            # Append product to the database
            db["winningProducts"][niche]["products"].append(product_data)
            product_counter += 1

        # Write the updated data back to db.json
        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(db, file, ensure_ascii=False, indent=4)

        # Close the WebDriver
        driver.quit()

def updateAll(): 
    updateProducts(1)
    updateProducts(2)
    print('30% COMPLETED...')
    updateProducts(3)
    updateProducts(4)
    print('60% COMPLETED...')
    updateProducts(5)
    updateProducts(6)
    print('100% COMPLETED...')

updateAll()
