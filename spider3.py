#The below spider is specially made for AAAI Conference which will go to particular xpath and extract information. 

import scrapy
import csv


class AAAILinkSpider(scrapy.Spider):
    name = 'aaai_link_spider'

    def start_requests(self):
        with open('url_metadata.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) 

            for row in reader:
                link = row[0]
                yield scrapy.Request(url=link.strip(), callback=self.parse, dont_filter=True)

    def parse(self, response):
        doi = response.xpath('/html/body/div/div[1]/div[1]/div/article/div/div[1]/section[2]/span/a/text()').get()
        yield {'doi': doi}

        if doi:
            with open('doi_metadata.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([doi])
