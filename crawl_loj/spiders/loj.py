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
    csv_writer.writerows([['Name', 'NumBalls', 'Difficulty', 'Prerequisites']])

    def parse(self, response):
        # a panel that contains links to all available juggling tricks

        base_path = response.xpath(f"/html/body/form/div/div[2]/div[2]/ul[2]")
        print(base_path)
        tricks_per_ball = base_path[0].xpath(f"(//ul)[2]/li")
        print(tricks_per_ball)
        for i, trick_list in enumerate(tricks_per_ball):
            num_balls = i + 3
            trick_links = trick_list.xpath('ul/li')
            #print(trick_links)
            for link in trick_links:
                href = link.xpath('a/@href')
                url = response.urljoin(href.extract_first())
                yield response.follow(url, callback=self.parse_trick_data, meta={'num_balls': num_balls})

                variations = link.xpath('ul/li/a/@href')
                for trick_var in variations:
                    var_url = response.urljoin(trick_var.get())
                    parent_name = self.canonicalize_name(url.split('/')[-1].replace('.html', ''))
                    yield response.follow(var_url, callback=self.parse_trick_data, meta={'num_balls': num_balls, 'parent_name': parent_name})


    # each juggling trick has an explanation site
    # we extract the difficulty and prerequisites (other tricks that should be learned before this one)
    def parse_trick_data(self, response):
        num_balls = response.meta.get('num_balls')
        parent_name = response.meta.get('parent_name')
        trick_data = TrickData()
        trick_data.num_balls = num_balls
        trick_data.name = self.canonicalize_name(response.url.split('/')[-1].replace('.html', ''))
        if parent_name:
            trick_data.name = f"[{parent_name}]{trick_data.name}"
        trick_data.difficulty = response.xpath('//ul[@id="otherinfo"]/li')[1].xpath('.//text()')[1].extract().replace(' ', '')
        trick_data.prerequisites = map(lambda plink: self.canonicalize_name(plink),
                                       response.xpath('//ul[@id="otherinfo"]/li')[2].xpath('a/@href').extract())
        data = [trick_data.name, trick_data.num_balls, trick_data.difficulty]
        for p in trick_data.prerequisites:
            data.append(p)
        self.csv_writer.writerows([data])

    def canonicalize_name(self, str):
        # remove apostrophe: Mill'sMess -> MillsMess
        # only take last part of link without .html
        return str.split('/')[-1].replace('.html', ''). replace('\'', '')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.csv_file.close()


if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute()