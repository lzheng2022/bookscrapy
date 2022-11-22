# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    def parse(self, response):
        # XPATH selector to get each book url
        all_books = response.xpath('//article[@class="product_pod"]')
        for book in all_books:
            book_url = book.xpath('.//h3/a/@href').extract_first()
            if 'catalogue/' not in book_url:
                book_url = 'catalogue/' + book_url
            book_url = self.base_url + book_url
            yield scrapy.Request(book_url, callback=self.parse_book)
        # Get next page url from nav bar
        next_page_partial_url = response.xpath(
            '//li[@class="next"]/a/@href').extract_first()
        if next_page_partial_url:
            if 'catalogue/' not in next_page_partial_url:
                next_page_partial_url = "catalogue/" + next_page_partial_url
            next_page_url = self.base_url + next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_book(self, response):
        # Function to scrap each field of data
        title = response.xpath('//div/h1/text()').extract_first()
        price = response.xpath(
            '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
        stock = response.xpath(
            '//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()').extract()[1].strip()
        stars = response.xpath(
            '//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
        description = response.xpath(
            '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        upc = response.xpath(
            '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        tax = response.xpath(
            '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()
        yield {
            'Title': title,
            'Price': price,
            'Stock': stock,
            'Stars': stars,
            'Description': description,
            'Upc': upc,
            'Tax': tax,
        }
