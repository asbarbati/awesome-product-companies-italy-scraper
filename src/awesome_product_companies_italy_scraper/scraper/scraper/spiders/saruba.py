from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SArubaSpider(scrapy.Spider):
    name = "aruba"
    allowed_domains: ClassVar[list[str]] = ["www.aruba.it"]
    career_page = "https://www.aruba.it/lavora-con-noi.aspx"
    start_urls: ClassVar[list[str]] = ["https://www.aruba.it/lavora-con-noi.aspx"]

    def parse(self, response):
        main_container = response.css("div.aruba-lavora-con-noi-positions-container")
        job_items = main_container.css("h2.position-title")

        for job in job_items:
            raw_title = job.css("h2::text").get()
            if raw_title:
                yield JobItem(title=raw_title.strip(), career_page=self.career_page)
