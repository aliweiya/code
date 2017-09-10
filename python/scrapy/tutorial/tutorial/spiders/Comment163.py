import scrapy

class Comment163(scrapy.Spider):
    name = 'Comment163'
    def start_requests(self):
        url = 'http://music.163.com'
        # yield scrapy.FormRequest(
        #     url = url,
        #     callback = self.parse_page, 
        #     )
        yield scrapy.Requests()

    def parse_page(self, response):
        with open('comment.html', 'w') as f:
            f.write(response.body)
            f.close()