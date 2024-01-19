!pip install scrapy
import scrapy
import pandas as pd

!scrapy startproject myproject

cd /content/myproject/myproject/spiders

!scrapy genspider citations1 dblp.org

!scrapy crawl data_spider
