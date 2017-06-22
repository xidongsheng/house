# -*- coding:utf-8 -*-
import lxml.html
import re


html = open('101091511585.html').read()

response = lxml.html.document_fromstring(html)

region_div = response.xpath('//div[@class="deal-bread"]')

district = region_div[0].xpath('a[last()-1]/text()')
district_detail = region_div[0].xpath('a[last()]/text()')


base_property_value = response.xpath('//div[@class="base"]/div[@class="content"]/ul/li/text()')
base_property_key = response.xpath('//div[@class="base"]/div[@class="content"]/ul/li/span/text()')
base_property = dict(zip(base_property_key,base_property_value))


deal_property_value = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li/text()')
deal_property_key = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li/span/text()')
deal_property = dict(zip(deal_property_key,deal_property_value))


msg_key = response.xpath('//div[@class="msg"]/span/text()')
msg_value = response.xpath('//div[@class="msg"]/span/label/text()')
msg = dict(zip(msg_key,msg_value))

price = response.xpath('//span[@class="dealTotalPrice"]/i/text()')
# price = ','.join(price)

unitPrice = response.xpath('//div[@class="price"]/b/text()')
# unitPrice = ','.join(unitPrice)


print price,unitPrice,msg