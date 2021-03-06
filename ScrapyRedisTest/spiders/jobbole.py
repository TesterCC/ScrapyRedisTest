#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'MFC'
__time__ = '18/2/11 17:21'

import re
import datetime

import scrapy
from urllib import parse
from scrapy.http import Request

from scrapy_redis.spiders import RedisSpider


class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ["blog.jobbole.com"]
    redis_key = 'jobbole:start_urls'

    # start_urls=["http://blog.jobbole.com/all-posts/"]

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数
        """
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        # http://blog.jobbole.com/all-posts/
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)
            # print(post_url)

        # 提取下一页link并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")      # .next.page-numbers 不加空格表示在同一节点
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):

        # # 实例化JobBoleArticleItem
        # article_item = JobBoleArticleItem()
        #
        # # 提取文章的具体字段
        # # use CSS Selector to locate Element
        #
        # # 获取文章封面图
        # # front_image_url = response.meta.get("front_image_url", "")
        # #
        # # # get title
        # # title = response.css(".entry-header h1::text").extract()[0]      # CSS伪类选择器::
        # #
        # # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·", "").strip()      # 处理/r/n空格，处理点号，处理空格
        # #
        # # praise_nums = response.css(".vote-post-up h10::text").extract()[0]     # ' 2 收藏'
        # #
        # # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # # match_re = re.match(r".*?(\d+).*", fav_nums)
        # # if match_re:
        # #     fav_nums = int(match_re.group(1))
        # # else:
        # #     fav_nums = 0
        # #
        # # comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]    # ' 2 评论'
        # # match_re = re.match(r".*?(\d+).*", comment_nums)
        # # if match_re:
        # #     comment_nums = int(match_re.group(1))
        # # else:
        # #     comment_nums = 0
        # #
        # # content = response.css("div.entry").extract()[0]
        # #
        # # # tag = response.css("p.entry-meta-hide-on-mobile a::text").extract()[0]    # '开发'
        # # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()   # ['开发', ' 2 评论 ', '数据科学', '机器学习']
        # #
        # # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # # tags = ",".join(tag_list)     # '开发,数据科学,机器学习'
        # #
        # # article_item["url_object_id"] = get_md5(response.url)
        # # article_item["title"] = title     # in items.py
        # # article_item["url"] = response.url
        # #
        # # # need to convert create_date str to date
        # # try:
        # #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # # except Exception as e:
        # #     create_date = datetime.datetime.now().date()
        # #
        # # article_item["create_date"] = create_date
        # #
        # # article_item["front_image_url"] = [front_image_url]   # [front_image_url]
        # # article_item["praise_nums"] = praise_nums
        # # article_item["comment_nums"] = comment_nums
        # # article_item["fav_nums"] = fav_nums
        # # article_item["tags"] = tags
        # # article_item["content"] = content
        #
        # # 通过item loader加载item
        # front_image_url = response.meta.get("front_image_url", "")   # 文章封面图
        #
        # # 加载自定义item不能继承自ItemLoader，而是继承ArticleItemLoader
        # item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # # item_loader.add_xpath()
        # item_loader.add_css("title", ".entry-header h1::text")
        # item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        # item_loader.add_value("front_image_url", [front_image_url])
        # item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        # item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        # item_loader.add_css("fav_nums", ".bookmark-btn::text")
        # item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        # item_loader.add_css("content", "div.entry")
        #
        # # call item
        # article_item = item_loader.load_item()
        #
        # # call yield , article_item will transfer to pipelines
        # yield article_item

        pass