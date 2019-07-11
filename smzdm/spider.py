import datetime
import requests
import time
import json
import re
from lxml import etree


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def get_timestamp(stime):
    stime = ''.join(stime.split())
    stime = '%s %s'%(str(datetime.date.today()), stime)
    timeArray = time.strptime(stime, "%Y-%m-%d %H:%M")
    timestamp = time.mktime(timeArray)
    timestamp = int(timestamp)
    return(timestamp)

if __name__ == '__main__':
    url = 'https://www.smzdm.com/jingxuan/'
    r = requests.get(url, headers=headers)
    xe_r = etree.HTML(r.text)
    for xe_item in xe_r.xpath('//ul[@id="feed-main-list"]/li[@class="feed-row-wide"]'):
        try:
            item = {}
            item['title'] = re.findall(r"'pagetitle':'(.+?)'}", xe_item.xpath('.//h5[@class="feed-block-title"]/a/@onclick')[0])[0]
            item['id'] = int(xe_item.xpath('.//h5[@class="feed-block-title"]/a/@href')[0].split('/')[-2])
            try:
                item['sprice'] = ''.join(xe_item.xpath('.//a[@class="z-highlight"]/text()')[0].split())
            except:
                item['sprice'] = ''.join(xe_item.xpath('.//div[@class="z-highlight"]/a/text()')[0].split())
            try:
                item['descripe_title'] = xe_item.xpath('.//div[@class="feed-block-descripe"]/strong/text()')[0]
                item['descripe_content'] = ''.join(xe_item.xpath('.//div[@class="feed-block-descripe"]/text()')[1:-1])
            except:
                item['descripe_title'] = ''
                item['descripe_content'] = ''.join(xe_item.xpath('.//div[@class="feed-block-descripe"]/text()'))[34:-30]
            item['worthy'] = int(xe_item.xpath('.//i[@class="icon-zhi-o-thin"]/../span/text()')[0])
            item['unworthy'] = int(xe_item.xpath('.//i[@class="icon-buzhi-o-thin"]/../span/text()')[0])
            item['star'] = int(xe_item.xpath('.//i[@class="icon-star-o-thin"]/../span/text()')[0])
            item['comment'] = int(xe_item.xpath('.//i[@class="icon-comment-o-thin"]/../span/text()')[0])
            item['timestamp'] = get_timestamp(xe_item.xpath('.//span[@class="feed-block-extras"]/text()')[0])
            item['market'] = re.findall(r"'mall':'(.+?)','", xe_item.xpath('.//span[@class="feed-block-extras"]/a/@onclick')[0])[0]
            item['links'] = xe_item.xpath('.//div[@class="feed-link-btn-inner"]/a/@href')[0]
            print(json.dumps(item, ensure_ascii=False, indent=1))
        except Exception as e:
            print(e)


