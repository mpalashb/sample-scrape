import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    done = 0
    itemsDone = 0

    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')

        for q in quotes:

            items = {}
            items['url_page'] = response.url
            items['author_link'] = response.urljoin(q.xpath('.//*[@class="author"]//following-sibling::a//@href').extract_first())
            items['author'] = q.xpath('.//*[@class="author"]//text()').extract_first()
            items['tags_count'] = len(q.xpath('.//*[@class="tags"]//*[@class="tag"]'))

            yield items
            self.itemsDone +=1
        
        print("========================================================")
        if not self.done == 0:
            print(f"Pages Done: {self.done+1}")
        else:
            print(f"Startd to crawl the first page")

        print(f"Items done: {self.itemsDone}")
        print("========================================================")

        next_page = response.xpath('.//*[@class="next"]//@href').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            self.done +=1
