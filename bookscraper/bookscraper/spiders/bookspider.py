import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if relative_url is not None:
                if 'catalogue/' in relative_url:
                    book_url = f"https://books.toscrape.com/{relative_url}"
                else:
                    book_url = f"https://books.toscrape.com/catalogue/{relative_url}"
                yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = f"https://books.toscrape.com/{next_page}"
            else:
                next_page_url = f"https://books.toscrape.com/catalogue/{next_page}"
            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_book_page(self,response):
        table_rows = response.css('table tr')
        
        book_item = BookItem()
        book_item['url'] = response.url,
        book_item['name']=  response.css('#content_inner > article > div.row > div.col-sm-6.product_main > h1::text').get()
        book_item['product type']=  response.css('#content_inner > article > table > tbody > tr:nth-child(2) > td::text').get()
        book_item['price_excl_tax']= response.css('#content_inner > article > table > tbody > tr:nth-child(3) > td::text').get()
        book_item['price_incl_tax']=  table_rows.css('#content_inner > article > table > tbody > tr:nth-child(4) > td').get()
        book_item['tax']= table_rows.css('#content_inner > article > table > tbody > tr:nth-child(5) > td::text').get()
        book_item['availability']=  table_rows.css('#content_inner > article > table > tbody > tr:nth-child(6) > td::text').get()
        book_item['num_reviews']=  table_rows.css('#content_inner > article > table > tbody > tr:nth-child(7) > td::text').get()
        book_item['stars']=  response.css('p.star-rating').attrib['class']
        book_item['category']= response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book_item['description']=  response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book_item['price']= response.css('#content_inner > article > div.row > div.col-sm-6.product_main > p.price_color::text').get()

        yield BookItem