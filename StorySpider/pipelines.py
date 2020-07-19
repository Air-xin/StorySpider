# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os


class StoryspiderPipeline:
    def process_item(self, item, spider):
        print(dict(item))
        return item


class ConserveTxt:
    def process_item(self, item, spider):
        type = item['type']
        name = item['name']
        chapter = item['chapter']
        content = ''.join(item['content'])
        dir = './files/{}/{}/'
        if not os.path.exists(dir.format(type, name)):
            os.makedirs(dir.format(type, name))
        with open(dir.format(type, name) + '{}.txt'.format(chapter), 'w') as f:
            f.write(content)
        return item
