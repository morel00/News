import requests
from bs4 import BeautifulSoup
import pandas as pd

class ProductScraper:
    def __init__(self, search_query):
        self.search_query = search_query
        self.ebay_base_url = "https://www.ebay.com/deals/sch?_nkw={}"
        self.amazon_base_url = "https://www.amazon.com/s?k={}"

    def scrape_ebay(self):
        ebay_url = self.ebay_base_url.format(self.search_query.replace(" ", "+"))
        response = requests.get(ebay_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.find_all("li", {"class": "s-item"}):
            title = item.find("h3", {"class": "s-item__title"})
            price = item.find("span", {"class": "s-item__price"})
            link = item.find("a", {"class": "s-item__link"})['href']
            if title and price:
                products.append({
                    'title': title.text,
                    'price': price.text,
                    'link': link,
                    'source': 'eBay'
                })
        return products

    def scrape_amazon(self):
        amazon_url = self.amazon_base_url.format(self.search_query.replace(" ", "+"))
        response = requests.get(amazon_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
            title = item.h2.text.strip()
            price = item.find("span", {"class": "a-price-whole"})
            link = "https://www.amazon.com" + item.h2.a['href']
            if title and price:
                products.append({
                    'title': title,
                    'price': price.text.strip(),
                    'link': link,
                    'source': 'Amazon'
                })
        return products

    def run(self):
        ebay_products = self.scrape_ebay()
        amazon_products = self.scrape_amazon()
        all_products = ebay_products + amazon_products
        df = pd.DataFrame(all_products)
        df.to_csv('products.csv', index=False)
        print('Scraping completado. Los resultados están en products.csv')

if __name__ == "__main__":
    search_query = input("Introduce el producto que deseas buscar: ")
    scraper = ProductScraper(search_query)
    scraper.run()