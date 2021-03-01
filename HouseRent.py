from selenium import webdriver
from bs4 import BeautifulSoup as Bs
import time
import lxml

google_form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSdCNPfeCyaYyl572TG7G6zJWi8oC2oEifVPuMUhpEQSr5oJjA/viewform?usp=sf_link'

driver_path = r"C:\Users\LENOVO\Devlopment\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path)

driver.get('https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-124.36407590953692%2C%22east%22%3A-110.82891965953692%2C%22south%22%3A33.29744354892151%2C%22north%22%3A41.97906468520313%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A6%7D')
time.sleep(2)

html = driver.page_source
soup = Bs(html, 'lxml')
data = soup.select(selector="ul li article")
prices = []
links = []
all_address = []
# Scraping data from Zillow

for house in data:

    house_data = house
    link = house_data.select_one(selector='div .list-card-link').get("href")
    address = house_data.select_one(selector='div .list-card-addr').getText()
    price = house_data.select_one(selector='div div .list-card-price').getText()

    if '/' in price:
        temp = price.split('/')
        price = temp[0]
    else:
        temp = price.split('+')
        price = temp[0]

    if 'https' not in link:
        link = 'https://www.zillow.com/'+link

    prices.append(price)
    links.append(link)
    all_address.append(address)

# Google form fill up
for i in range(len(links)):
    driver.get(google_form_link)
    time.sleep(2)
    from_address = driver.find_element_by_xpath('/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    from_address.send_keys(all_address[i])
    from_link = driver.find_element_by_xpath('/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    from_link.send_keys(links[i])
    from_price = driver.find_element_by_xpath('/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    from_price.send_keys(prices[i])

    from_submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    from_submit.click()
    time.sleep(3)