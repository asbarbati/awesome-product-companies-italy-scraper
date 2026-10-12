import re
import unicodedata
from typing import ClassVar
from urllib.parse import urlencode

import scrapy

from scraper.items import JobItem


class SBludigitSpider(scrapy.Spider):
    name = "bludigit"
    allowed_domains: ClassVar[list[str]] = ["carriere.italgas.it"]
    career_page = "https://carriere.italgas.it/search"
    start_url = (
        "https://carriere.italgas.it/search/?createNewAlert=false&q=&locationsearch="
        "&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield1=IT"
    )
    results_path = "/tile-search-results/"
    filters: ClassVar[dict[str, str]] = {
        "q": "",
        "sortColumn": "referencedate",
        "sortDirection": "desc",
        "optionsFacetsDD_customfield1": "IT",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [self.start_url]
        self.seen: set[str] = set()

    def parse(self, response, startrow=0):
        tiles = response.css("li.job-tile")
        if not tiles:
            return

        new_jobs = 0
        for tile in tiles:
            link = (tile.css("a.jobTitle-link") or tile.css("a"))[:1]
            if not link:
                continue
            href = response.urljoin(link[0].attrib.get("href", ""))
            title = self.clean_text(link[0].xpath("string(.)").get() or "")
            if not title or href in self.seen:
                continue
            self.seen.add(href)
            new_jobs += 1
            yield JobItem(title=title, career_page=self.career_page)

        self.logger.info("startrow=%s tiles=%s new=%s", startrow, len(tiles), new_jobs)

        # Stop if the page added nothing new (end of results or ignored startrow).
        if not new_jobs:
            return

        next_startrow = startrow + len(tiles)
        yield scrapy.Request(
            self.results_url(response, next_startrow),
            cb_kwargs={"startrow": next_startrow},
        )

    def results_url(self, response, startrow):
        query = urlencode({**self.filters, "startrow": startrow})
        return response.urljoin(f"{self.results_path}?{query}")

    @staticmethod
    def clean_text(text):
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
