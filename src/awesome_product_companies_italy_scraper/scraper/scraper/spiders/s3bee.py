from typing import ClassVar

import scrapy

from scraper.items import JobItem


class S3beeSpider(scrapy.Spider):
    name = "3bee"
    allowed_domains = ("3bee.factorial.it")
    career_page = "https://3bee.factorial.it"
    start_urls: ClassVar[list[str]] = ["https://3bee.factorial.it"]

    def parse(self, response):
        main_container = response.css('div[data-controller*="job-filters"]')
        job_items = main_container.css("li.job-offer-item")

        for item in job_items:
            raw_title = item.css("span div::text").get()
            if raw_title:
                yield JobItem(title=raw_title.strip(), career_page=self.career_page)
