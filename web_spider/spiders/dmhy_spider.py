from pathlib import Path
from web_spider.items import DmhyItem
import scrapy


# class DmhySpider(scrapy.Spider):

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        keyword=getattr(self, "keyword", "%E5%90%9E%E5%99%AC")
        sort_id=getattr(self, "sort_id", "2")
        team_id=getattr(self, "team_id", "755")
        order=getattr(self, "order", "date-desc")
        urls = [
            f"https://share.dmhy.org/topics/list?keyword={keyword}&sort_id={sort_id}&team_id={team_id}&order={order}",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            })

    def parse(self, response):
        # filename = f"吞噬.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"------------------Saved file {filename}-----------------------")
        a_list = response.xpath('//tbody/tr/td[@class="title"]/a')
        for a in a_list:
            # item = DmhyItem()
            href = a.xpath('./@href').get()
            text = a.xpath('normalize-space(.)').get()
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_deatil,
                meta={'text': text}
            )

    def parse_deatil(self, response):
        text = response.meta['text']
        a = response.xpath('//div[@id="tabs-1"]/p[1]/a')
        href = a.xpath('./@href').get()
        text = a.xpath('normalize-space(.)').get()
        item = DmhyItem()
        item['href'] = href
        item['text'] = text
        yield item

        
