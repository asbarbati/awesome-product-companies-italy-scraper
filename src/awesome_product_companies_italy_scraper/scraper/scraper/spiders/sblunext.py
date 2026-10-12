import re
import unicodedata
from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SBluenextSpider(scrapy.Spider):
    name = "blunext"
    allowed_domains: ClassVar[list[str]] = ["www.bluenext.it"]
    career_page = "https://www.bluenext.it/it/lavora-con-noi/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [self.career_page]

    def parse(self, response):
        seen = set()

        for link in response.css("a.vc_gitem-link.vc-zone-link"):
            raw_title = link.attrib.get("title") or link.xpath("string(.)").get() or ""
            title = self.clean_text(raw_title)
            if not title or title in seen:
                continue
            seen.add(title)
            yield JobItem(title=title, career_page=self.career_page)

    @staticmethod
    def clean_text(text):
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
