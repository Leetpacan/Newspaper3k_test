import scrapy
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
import json
datatosave = []
class NewsSpider(scrapy.Spider):
    name = "news_spider"
    def start_requests(self):
        urls = [
            'https://www.fontanka.ru',
            'https://news.mail.ru',
            'https://www.vesti.ru'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        url = response.url
        article = Article(url)
        article.download()
        article.parse()
        if article.is_parsed:
            with open('source_state.json', 'a+') as f:
                json.dump({"need_render": False}, f)
            data = {
                'url': article.url,
                'title': article.title,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'text': article.text,
            }
            datatosave.append(data)
            with open('news.json', 'a+') as newsfile:
                json.dump(datatosave, newsfile)
            yield data
        else:
            with open('source_state.json', 'a+') as f:
                json.dump({"need_render": True}, f)
            options = SafariOptions()
            options.add_argument("--headless")
            driver = webdriver.Safari(options=options)
            driver.get(url)
            yield {
                'url': url,
                'title': driver.title,
            }
            driver.close()