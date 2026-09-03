from typing import ClassVar
from urllib.parse import urlencode

import scrapy

from scraper.items import JobItem

class SBludigitSpider(scrapy.Spider):
    name = "bludigit"
    allowed_domains: ClassVar[list[str]] = ["carriere.italgas.it"]
    career_page = "https://carriere.italgas.it/search"
    start_urls: ClassVar[list[str]] = ["https://carriere.italgas.it/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield1=IT"]

    def parse(self, response):
        page_size = 5

        yield from self.parse_tiles(response)

        yield scrapy.Request(
            self.results_url(page_size),
            callback=self.parse_more,
            meta={"startrow": page_size, "page_size" : page_size},
        )

    def parse_more(self, response):
        if not response.css("li.job-tile"):
            return

        yield from self.parse_tiles(response)

        page_size = response.meta["page_size"]
        next_startrow = response.meta["startrow"] + page_size

        yield scrapy.Request(
            self.results_url(next_startrow),
            callback=self.parse_more,
            meta={"startrow": next_startrow, "page_size" : page_size},
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
            "optionsFacetsDD_customfield1": "IT",
            "startrow": startrow,
        }

        return f"https://carriere.italgas.it/tile-search-results/?{urlencode(params)}"