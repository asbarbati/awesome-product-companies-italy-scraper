from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SAbletechSpider(scrapy.Spider):
    name = "abletech"
    allowed_domains: ClassVar[list[str]] = ["www.abletech.it"]
    career_page = "https://www.abletech.it/lavora-con-noi/"
    start_urls: ClassVar[list[str]] = ["https://www.abletech.it/lavora-con-noi/"]

    def parse(self, response):
        job_blocks = response.css('div.candidature')
        for block in job_blocks:
            for card in block.css('div.card'):
                job_title = card.css('h4::text').get()
                if job_title:
                    yield JobItem(title=job_title.strip(), career_page=self.career_page)
