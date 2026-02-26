import re

import scrapy
from scrapy import Request
from ..items import BookItem


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["spa5.scrape.center"]
    base_url= "https://spa5.scrape.center"

    def start_requests(self):
        start_url = f'{self.base_url}/page/1'
        yield Request(start_url, callback=self.parse_index)

    def parse_index(self, response):
        # 提取列表项并生成详情页请求
        items = response.css('.item')
        for item in items:
            href = item.css('.top a::attr(href)').extract_first()
            detail_url = response.urljoin(href)  # 相对URL转绝对URL
            yield Request(detail_url, callback=self.parse_detail, priority=2)  # 详情页请求优先级提升

        # 解析页码并生成下一页请求
        match = re.search(r'page/(\d+)', response.url)
        if not match:  # 无页码（如首页），终止翻页
            return
        page = int(match.group(1)) + 1
        next_url = f'{self.base_url}/page/{page}'
        yield Request(next_url, callback=self.parse_index)  # 递归翻页


    def parse_detail(self, response):
        # 提取页面核心字段
        name = response.css('.name::text').extract_first()
        tags = response.css('.tags button span::text').extract()
        score = response.css('.score::text').extract_first()
        price = response.css('.price span::text').extract_first()
        cover = response.css('.cover::attr(src)').extract_first()

        # 数据清洗：去除空白字符/处理空值
        tags = [tag.strip() for tag in tags] if tags else []
        score = score.strip() if score else None

        # 封装Item并输出
        item = BookItem(name=name, tags=tags, score=score, price=price, cover=cover)
        yield item