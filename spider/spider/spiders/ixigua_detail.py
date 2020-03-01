# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import json
from base64 import b64decode
import requests

class IxiguaDetailSpider(scrapy.Spider):
    name = 'ixigua_detail'
    allowed_domains = ['ixigua.com']
    start_urls = ['http://ixigua.com/']

    cookies = {
        'wafid':'af2ade58-1768-4fea-983d-c2ad0cf69fc2',
        'wafid.sig': 'xXI_Dn80Pyi_4TsddkTjVMYvnAQ',
        'xiguavideopcwebid': '6798376759479977479',
        'xiguavideopcwebid.sig': 'reKWpJ4q1-zRPqWZ3roOINB3wGc'
    }

    def __init__(self, path=None, *args, **kwargs):
        super(IxiguaDetailSpider, self).__init__(*args, **kwargs)
        self.path = path

    def start_requests(self):
        headers = {
            ':authority': 'www.ixigua.com',
            ':method': 'GET',
            ':path': self.path,
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5',
            'cache-control': 'max-age=0',
            'referer': 'https://www.ixigua.com/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        }

        print('https://www.ixigua.com%s' % (self.path))


        yield scrapy.Request(
            method='get',
            url='https://www.ixigua.com%s' % (self.path),
            callback=self.parse,
            headers=headers,
            cookies=self.cookies
        )

    def parse(self, response):

        html = etree.HTML(response.text)
        str_list = html.xpath('.//script/text()')
        for one in str_list:
            if 'video_1' in one:
                content = one.replace('window._SSR_HYDRATED_DATA=', '')

                o = json.loads(content)
                video_id = o['Projection']['video']['videoResource']['normal']['video_id']
                video_url = b64decode(o['Projection']['video']['videoResource']['normal']['video_list']['video_3']['main_url']).decode()

                self.downloadfile('/Users/leewind/Projects/open/video-spider/video/%s.mp4' % (video_id), video_url)


    def downloadfile(self, filepath, url):
        r=requests.get(url)
        print("****Connected****")
        f=open(filepath,'wb');
        print("Donloading.....")
        for chunk in r.iter_content(chunk_size=255):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        print("Done")
        f.close()
