from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SBlunextSpider(scrapy.Spider):
    name = "blunext"
    allowed_domains: ClassVar[list[str]] = ["https://www.bluenext.it/it/"]
    career_page = "https://www.bluenext.it/it/lavora-con-noi/"
    start_urls: ClassVar[list[str]] = ["https://www.bluenext.it/it/lavora-con-noi/"]

    def parse(self, response):
        job_items = response.css("a.vc_gitem-link.vc-zone-link")

        for job in job_items:
            raw_title = job.attrib.get("title")
            if raw_title:
                yield JobItem(title=raw_title.strip(), career_page=self.career_page)