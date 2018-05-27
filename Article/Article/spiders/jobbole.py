# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse

from Article.items import JobboleArticleItem
from Article.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章 url 并交给 scrapy 下载后解析
        2. 获取下一页 url 并交给 scrapy 进行下载，下载完成后进行解析
        """

        # 解析列表页中的所有文章 url
        post_urls = response.css('#archive .floated-thumb .post-meta .archive-title ::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_articles)
            # print(post_url)

        # 提取下一页并交给 scrapy 进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_articles(self, response):
        """
        提取文章的具体字段
        """
        article_item = JobboleArticleItem()

        # 标题（默认值为空字符串''）
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # 发表时间
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first('')\
            .strip().replace('·', "").strip()
        # 点赞数
        praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first('')
        # 收藏数
        favor_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first('')
        match_re1 = re.match('.*?(\d+).*', favor_nums)
        if match_re1:
            favor_nums = int(match_re1.group(1))
        else:
            favor_nums = 0
        # 评论数
        comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first('')
        match_re2 = re.match('.*?(\d+).*', comment_nums)
        if match_re2:
            comment_nums = int(match_re2.group(1))
        else:
            comment_nums = 0
        # 正文内容（带标签）
        # content = response.xpath('//div[@class="entry"]').extract_first('')
        content = response.xpath(
            '//div[@class="entry"]/p/text()|'
            '//div[@class="entry"]/p/code/text()|'
            '//div[@class="entry"]/p/a/text()|'
            '//div[@class="entry"]/p/strong/text()|'
            '//div[@class="entry"]//div[@class="crayon-line"]/span/text()|'
            '//div[@class="entry"]/h3/text()|'
            '//div[@class="entry"]/ul/li/text()').extract()
        all_content = ""
        for c in content:
            all_content += c

        # 作者
        author = response.xpath('//div[@class="copyright-area"]/a/text()').extract_first('')
        # 标签
        tags = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()

        # print(title, create_date, praise_nums, favor_nums, comment_nums, author, tags)

        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, '%Y%m%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['praise_nums'] = praise_nums
        article_item['favor_nums'] = favor_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = all_content
        article_item['author'] = author
        article_item['tags'] = tags

        yield article_item
