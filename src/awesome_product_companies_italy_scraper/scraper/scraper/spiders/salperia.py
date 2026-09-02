from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SAlperiaSpider(scrapy.Spider):
    name = "alperia"
    allowed_domains = ("www.alperiagroup.eu", "alperiagroup.onboard.org")
    career_page = "https://www.alperiagroup.eu/it/carriera"
    start_urls: ClassVar[list[str]] = ["https://alperiagroup.onboard.org/it/exports/v2/jobs.json?show_on_career_site=true&ignore_type=internship"]


    def parse(self, response):
        body = response.json()
        for job in body:
            if int(job["departments"][0]["id"]) == 8259:
                yield JobItem(title=job["title"].strip(), career_page=self.career_page)