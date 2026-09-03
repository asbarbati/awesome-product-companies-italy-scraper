from typing import ClassVar
from urllib.parse import urlencode

import scrapy

from scraper.items import JobItem

PAGE_SIZE = 5


class SBludigitSpider(scrapy.Spider):
    name = "bludigit"
    allowed_domains: ClassVar[list[str]] = ["carriere.italgas.it"]
    career_page = "https://carriere.italgas.it/search"
    start_urls: ClassVar[list[str]] = ["https://carriere.italgas.it/search"]

    def parse(self, response):
        yield from self.parse_tiles(response)
        yield scrapy.Request(
            self.results_url(PAGE_SIZE),
            callback=self.parse_more,
            meta={"startrow": PAGE_SIZE},
        )

    def parse_more(self, response):
        if not response.css("li.job-tile"):
            return
        yield from self.parse_tiles(response)
        next_startrow = response.meta["startrow"] + PAGE_SIZE
        yield scrapy.Request(
            self.results_url(next_startrow),
            callback=self.parse_more,
            meta={"startrow": next_startrow},
        )

    def parse_tiles(self, response):
        for tile in response.css("li.job-tile"):
            title = tile.css("a::text").get()
            if title:
                yield JobItem(title=title.strip(), career_page=self.career_page)

    @staticmethod
    def results_url(startrow):
        params = {
            "q": "",
            "sortColumn": "referencedate",
            "sortDirection": "desc",
            "startrow": startrow,
        }
        return f"https://carriere.italgas.it/tile-search-results/?{urlencode(params)}"