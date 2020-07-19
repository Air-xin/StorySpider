import scrapy
from ..items import StoryspiderItem
import requests
from fake_useragent import UserAgent
from lxml import etree


class StorySpiderSpider(scrapy.Spider):
    name = 'story_spider'
    allowed_domains = ['www.quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']

    def parse(self, response):
        li_list = response.xpath('//*[@id="channel-header"]/div/nav/ul/li')
        for li in li_list:
            if li != li_list[-1]:
                item = StoryspiderItem()
                item['type'] = li.xpath('.//a/text()').get()
                link = li.xpath('.//a/@href').get()
                yield scrapy.Request(url=link, callback=self.parse_two, meta={'item': item}, dont_filter=True)

    def parse_two(self, response):
        item_1 = response.meta['item']
        count = response.xpath('//*[@id="pagelink"]/a[@class="last"]/text()')
        li_list = response.xpath('//*[@id="navList"]/section/ul/li')
        for li in li_list:
            item = StoryspiderItem()
            item['type'] = item_1['type']
            item['name'] = li.xpath('.//span/a[1]/@title').get()
            link_1 = li.xpath('.//span/a[3]/@href').get()
            code = li.xpath('//*[@id="container"]/div[2]/section/div/div[4]/div[1]/dl[1]/dd/text()').get()
            link = self.get_chapter_link(link_1)
            if code == '连载':
                yield scrapy.Request(url=link, callback=self.parse_three, meta={'item': item}, dont_filter=True)
            else:
                yield scrapy.Request(url=link, callback=self.parse_three, meta={'item': item})

    def get_chapter_link(self, url):
        html = requests.get(url=url, headers={'User-Agent': UserAgent().random}).text
        parse = etree.HTML(html)
        link = parse.xpath('//*[@id="container"]/div[2]/section/div/div[1]/div[2]/a[1]/@href')[0]
        return link

    def parse_three(self, response):
        item_1 = response.meta['item']
        li_list = response.xpath('//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/li')
        for li in li_list:
            item = StoryspiderItem()
            item['type'] = item_1['type']
            item['name'] = item_1['name']
            item['chapter'] = li.xpath('.//a/text()').get()
            link = li.xpath('.//a/@href').get()
            yield scrapy.Request(url=link, callback=self.parse_four, meta={'item': item})

    def parse_four(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//*[@id="content"]/text()').extract()
        yield item
