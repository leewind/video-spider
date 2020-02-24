# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import SpiderXigua

class IxiguaSpider(scrapy.Spider):
    name = 'ixigua'
    allowed_domains = ['ixigua.com']
    start_urls = ['http://ixigua.com/']

    user_id_list = [98852196301]

    def start_requests(self):

        for user_id in self.user_id_list:
            url = 'https://m.ixigua.com/video/app/user/home/?to_user_id=%d&format=json&max_behot_time=%d' % (user_id, 0)

            yield scrapy.Request(
                method='get',
                url=url,
                callback=self.parse,
                meta={
                    'user_id': user_id
                }
            )

    def parse(self, response):
        o = json.loads(response.text)

        yield SpiderXigua(
            data=o['data']
        )

        behot_time = 0
        for item in o['data']:

            if behot_time == 0:
                behot_time = item['behot_time']
                continue

            if item['behot_time'] < behot_time:
                behot_time = item['behot_time']

        if behot_time > 0:
            url = 'https://m.ixigua.com/video/app/user/home/?to_user_id=%d&format=json&max_behot_time=%d' % (response.meta['user_id'], behot_time)

            yield scrapy.Request(
                method='get',
                url=url,
                callback=self.parse,
                meta={
                    'user_id': response.meta['user_id']
                }
            )



