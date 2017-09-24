import scrapy

class Comment163(scrapy.Spider):
    name = 'Comment163'

    # enter from singers

    def start_requests(self):
        url = 'http://music.163.com/#/discover/artist/signed/'
        # yield scrapy.FormRequest(
        #     url = url,
        #     callback = self.parse_page, 
        #     )
        yield scrapy.Requests(url, callback=self.parse_singer)

    def parse_singer(self, response):
        print response.body