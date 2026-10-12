import re
import unicodedata
from typing import ClassVar

import scrapy
from scraper.items import JobItem


class BoltonGroupSpider(scrapy.Spider):
    name = "boltongroup"
    allowed_domains: ClassVar[list[str]] = ["jobs.boltongroup.net"]
    career_page = "https://jobs.boltongroup.net/search/"
    start_url = (
        "https://jobs.boltongroup.net/search/?createNewAlert=false&q=&locationsearch="
        "&optionsFacetsDD_customfield1=Information+%26+Communication+Technology"
        "&optionsFacetsDD_country=&optionsFacetsDD_city=&optionsFacetsDD_customfield2="
        "&optionsFacetsDD_customfield5=Permanent"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [self.start_url]
        self.seen: set[str] = set()

    def parse(self, response, offset=0):
        links = response.css("a.jobTitle-link") or response.css('a[href*="/job/"]')

        new_jobs = 0
        for link in links:
            href = response.urljoin(link.attrib.get("href", ""))
            if not href or href in self.seen:
                continue
            title = self.clean_text(link.xpath("string(.)").get() or "")
            if not title:
                continue
            self.seen.add(href)
            new_jobs += 1
            yield JobItem(title=title, career_page=self.career_page)

        self.logger.info(
            "startrow=%s status=%s links=%s new_jobs=%s",
            offset, response.status, len(links), new_jobs,
        )

        if new_jobs:
            next_offset = offset + new_jobs
            yield scrapy.Request(
                f"{self.start_url}&startrow={next_offset}",
                cb_kwargs={"offset": next_offset},
            )

    @staticmethod
    def clean_text(text):
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
