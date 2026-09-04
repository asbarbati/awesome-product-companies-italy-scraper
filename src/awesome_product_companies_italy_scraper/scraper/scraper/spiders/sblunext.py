import re
import scrapy
import unicodedata

from typing import ClassVar
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
                yield JobItem(title=self.clean_text(raw_title), career_page=self.career_page)

    @staticmethod
    def clean_text(text):
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()