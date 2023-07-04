import scrapy


class EmpiresSpider(scrapy.Spider):
    name = 'emp_scraper'
    allowed_domains = ['https://en.wikipedia.org/']
    start_urls = ['http://en.wikipedia.org/']

    def start_requests(self):
        urls = ['https://en.wikipedia.org/wiki/List_of_Hindu_empires_and_dynasties#List']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for num, row in enumerate(response.xpath('//*[@class="wikitable sortable"]//tr')):
            yield {
            'empire/dynasty' : row.xpath('td[1]//text()').extract().encode('utf-8').decode('utf-8'),
            'established' : row.xpath('td[2]//text()').extract().encode('utf-8').decode('utf-8'),
            'disestablished' : row.xpath('td[3]//text()').extract().encode('utf-8').decode('utf-8'),
            'capital(s)' : row.xpath('td[4]//text()').extract().encode('utf-8').decode('utf-8'),
            'language(s)' : row.xpath('td[5]//text()').extract().encode('utf-8').decode('utf-8'),
            'present part of' : row.xpath('td[6]//text()').extract().encode('utf-8').decode('utf-8')
            }
