# -*- coding: utf-8 -*-
import scrapy
import csv

class TrickData(object):
    def __init__(self):
        pass

class LojSpider(scrapy.Spider):
    name = 'loj'
    allowed_domains = ['libraryofjuggling.com']
    start_urls = ['https://libraryofjuggling.com/Home.html']
    trick_data = []
    csv_file = open('juggling_tricks.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows([['Name', 'Difficulty', 'Prerequisites']])

    def parse(self, response):
        # a panel that contains links to all available juggling tricks
        trick_links = response.xpath('//div[@id="tree"]/ul[2]/li/ul/li')
        for link in trick_links:
            href = link.xpath('a/@href')
            url = response.urljoin(href.extract_first())
            yield response.follow(url, callback=self.parse_trick_data)
        print(self.trick_data)

    # each juggling trick has an explanation site
    # we extract the difficulty and prerequisites (other tricks that should be learned before this one)
    def parse_trick_data(self, response):
        trick_data = TrickData()
        trick_data.name = self.canonicalize_name(response.url.split('/')[-1].replace('.html', ''))
        trick_data.difficulty = response.xpath('//ul[@id="otherinfo"]/li')[1].xpath('.//text()')[1].extract().replace(' ', '')
        trick_data.prerequisites = map(lambda plink: self.canonicalize_name(plink),
                                       response.xpath('//ul[@id="otherinfo"]/li')[2].xpath('a/@href').extract())
        data = [trick_data.name, trick_data.difficulty]
        print(trick_data.prerequisites)
        for p in trick_data.prerequisites:
            data.append(p)
        self.csv_writer.writerows([data])

    def canonicalize_name(self, str):
        # remove apostrophe: Mill'sMess -> MillsMess
        # only take last part of link without .html
        return str.split('/')[-1].replace('.html', ''). replace('\'', '')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('CLOSE')
        self.csv_file.close()