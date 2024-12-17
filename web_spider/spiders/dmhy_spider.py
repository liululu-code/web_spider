from pathlib import Path
from web_spider.items import DmhyItem
import scrapy


class SearchSpider(scrapy.Spider):
    name = "dmhy_search"

    def start_requests(self):
        main_url = "https://share.dmhy.org"

        keyword=getattr(self, "keyword", "")
        sort_id=getattr(self, "sort_id", "")
        team_id=getattr(self, "team_id", "")
        order=getattr(self, "order", "")
        urls = [
            f"{main_url}/topics/list?keyword={keyword}&sort_id={sort_id}&team_id={team_id}&order={order}",
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
            yield {
                "text": text,
                "href": href
            }
            # yield scrapy.Request(
            #     url=response.urljoin(href),
            #     callback=self.parse_deatil,
            #     meta={'text': text}
            # )

    # def parse_deatil(self, response):
    #     text = response.meta['text']
    #     a = response.xpath('//div[@id="tabs-1"]/p[1]/a')
    #     href = a.xpath('./@href').get()
    #     text = a.xpath('normalize-space(.)').get()
    #     item = DmhyItem()
    #     item['href'] = href
    #     item['text'] = text
    #     yield item

import json
class DownloadSpider(scrapy.Spider):
    name="download_spider"
    def start_requests(self):
        main_url = "https://share.dmhy.org"
        download_json_file = getattr(self, "download_json_file", "./dmhy.json")
        if (download_json_file):
            with open(download_json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    url = main_url + item['href']
                    yield scrapy.Request(
                        url=url, 
                        callback=self.parse, 
                        headers={
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                        }, 
                        # meta={'text': item['text']}
                    )


    def parse(self, response):
        # text = response.meta['text']
        a = response.xpath('//div[@id="tabs-1"]/p[1]/a')
        href = a.xpath('./@href').get()
        text = a.xpath('normalize-space(.)').get()
        item = DmhyItem()
        item['href'] = "https:" + href
        item['text'] = text
        yield item
