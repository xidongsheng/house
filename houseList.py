# -*- coding:utf-8 -*-
import lxml.html
import re
from urlparse import urljoin

html = open('dongcheng').read()

response = lxml.html.document_fromstring(html)

_detail_url_re = re.compile('^http://bj\.lianjia\.com/chengjiao/[a-zA-Z0-9]{10,}\.html$')

_start_url_re = re.compile('^http://bj\.lianjia\.com/chengjiao/([a-zA-Z0-9]{2,}/){1,2}$')
# listPage = response.xpath('//ul[@class="listContent"]/@href')

detail_URL = []
start_URL = []

for url in response.xpath('//a/@href'):
    url = urljoin("http://bj.lianjia.com/chengjiao",url)

    if _detail_url_re.search(url):
        if url not in detail_URL:
            detail_URL.append(url)

    if _start_url_re.search(url):
        if url not in start_URL:
            start_URL.append(url)


print len(detail_URL)
print len(start_URL)

#
# title = response.xpath('//div[@class="title"]/a/text()')
# print title[0]
#
# url_detail = response.xpath('//div[@class="title"]/a/@href')
# print url_detail[0]
#

houses = response.xpath('//ul[@class="listContent"]//div[@class="info"]')

for h in houses:

    # print h.tag, type(h), len(h)
    # print h.getroottree().tag
    # print h.getparent()
    title11 = h.xpath('div[@class="title"]/a/text()')
    print title11[0] if len(title11)>=1 else ''

    dealDate = h.xpath('div[@class="address"]/div[@class="dealDate"]/text()')
    dealDate = dealDate[0] if len(dealDate) >= 1 else ''
    print dealDate

    url_detail11 = h.xpath('div[@class="title"]/a/@href')
    print url_detail11