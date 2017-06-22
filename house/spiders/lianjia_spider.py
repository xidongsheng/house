# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from house.items import House
import logging
from urlparse import urljoin
import re
import os

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = [
        # "http://bj.lianjia.com/chengjiao/"
        "http://bj.lianjia.com/chengjiao/dongcheng/"
    ]

    rules = [
        Rule(LxmlLinkExtractor(allow='^http://bj\.lianjia\.com/chengjiao/([a-zA-Z0-9]{2,}/){1,2}$'),callback = 'parse',follow = True)
    ]


    def parse_house_basic(self, h):
        house = House()

        title = h.xpath('div[@class="title"]/a/text()').extract()
        house['title'] = title[0] if len(title)>=1 else ''

        dealDate = h.xpath('div[@class="address"]/div[@class="dealDate"]/text()').extract()
        house['dealDate'] = dealDate[0] if len(dealDate) >= 1 else ''

        url_detail = h.xpath('div[@class="title"]/a/@href').extract()
        house['url'] = url_detail
        # print url_detail
        return house

    def parse_house_details(self, response):
        ## store detail page
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)

        house = response.meta['house']

        house['price'] = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()
        house['unitPrice'] = response.xpath('//div[@class="price"]/b/text()').extract()

        region_div = response.xpath('//div[@class="deal-bread"]')
        house['district'] = region_div[0].xpath('a[last()-1]/text()').extract()
        house['district_detail'] = region_div[0].xpath('a[last()]/text()').extract()

        base_property_value = response.xpath('//div[@class="base"]/div[@class="content"]/ul/li/text()').extract()
        base_property_key = response.xpath('//div[@class="base"]/div[@class="content"]/ul/li/span/text()').extract()
        house['base_property'] = dict(zip(base_property_key, base_property_value))

        deal_property_value = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li/text()').extract()
        deal_property_key = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li/span/text()').extract()
        house['deal_property'] = dict(zip(deal_property_key, deal_property_value))

        msg_key = response.xpath('//div[@class="msg"]/span/text()').extract()
        msg_value = response.xpath('//div[@class="msg"]/span/label/text()').extract()
        house['msg'] = dict(zip(msg_key, msg_value))

        return house

    def parse(self, response):

        self.log('received house list page %s:' % response.url,level=logging.INFO)

        if 'captcha' in response.url:
            filename = 'captcha.html'
            with open(filename, 'wb') as f:
                f.write(response.body)

        houses = response.xpath('//ul[@class="listContent"]//div[@class="info"]')
        for h in houses:
            house = self.parse_house_basic(h)
            # print item
            if len(house['url']) == 1:
                yield Request(house['url'][0], meta={'house': house}, callback=self.parse_house_details)

        #
        # _start_url_re = re.compile('^http://bj\.lianjia\.com/chengjiao/([a-zA-Z0-9]{2,}/){1,2}$')
        #
        # for url in response.xpath('//a/@href').extract():
        #     url = urljoin("http://bj.lianjia.com/chengjiao", url)
        #     start_URL = []
        #     if _start_url_re.search(url):
        #         if url not in start_URL:
        #             start_URL.append(url)
        #             yield Request(url, callback=self.parse)

        # house = HouseItem()
        #
        # price = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()
        # price = ','.join(price)
        # house['price'] = price
        #
        # yield house
        #
        #
        # for url in response.xpath('//a/@href').extract():
        #     if url
        #     yield scrapy.Request(url, callback=self.parse)