# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join


class ScrapyredistestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 运用自带Item loader
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(lambda x:x+"-jobbole")
        # input_processor=MapCompose(add_jobbole)
        # input_processor=MapCompose(lambda x: x+"-jobbole", add_jobbole)
    )    # 统一Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor=TakeFirst()    # 只取第一个   , jobbole5customloader no need.
    )

    url = scrapy.Field()    # url长度是变化的，用md5处理可以使URL变成唯一且长度固定的值
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value),   # return front_image_url原值，覆盖default_output_processor = TakeFirst()
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(","),
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_nums) 
                    VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title), fav_nums=VALUES(fav_nums)
                """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"])
        return insert_sql, params
