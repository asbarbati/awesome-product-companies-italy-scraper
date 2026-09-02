from typing import ClassVar

import scrapy

from scraper.items import JobItem


class SAristonSpider(scrapy.Spider):
    name = "ariston"
    allowed_domains: ClassVar[list[str]] = ["careers.aristongroup.com"]
    career_page = "https://careers.aristongroup.com/search/"
    start_urls: ClassVar[list[str]] = [
        "https://careers.aristongroup.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=&optionsFacetsDD_department=ICT&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield2=",
        "https://careers.aristongroup.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=&optionsFacetsDD_department=R%26D&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield2="
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_titles = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        job_links = response.css("table#searchresults a.jobTitle-link")

        for link in job_links:
            title = link.css("::text").get("").strip()

            if title and title not in self.seen_titles:
                self.seen_titles.add(title)
                yield JobItem(
                    title=title, 
                    career_page=self.career_page
                )