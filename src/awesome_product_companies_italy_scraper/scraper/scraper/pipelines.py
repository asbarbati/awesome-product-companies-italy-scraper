# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from datetime import UTC, datetime
from typing import ClassVar

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exceptions import DropItem


class RemoveUselessJobsTitle:
    def __init__(self):
        self.skipped_words = ["spontaneous", "spontanea"]

    def is_valid(self, jobtitle):
        if not isinstance(jobtitle, str):
            return False

        jobtitlelow = jobtitle.lower()
        for skipword in self.skipped_words:
            if skipword in jobtitlelow:
                return False

        return True


class ScraperPipeline:
    all_items: ClassVar[list[dict]] = []

    def __init__(self):
        self.job_validator = RemoveUselessJobsTitle()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.engine_stopped, signal=signals.engine_stopped)
        return pipeline

    def engine_stopped(self):
        if ScraperPipeline.all_items:
            with open("output/output.json", "w", encoding="utf-8") as fjsonout:
                json.dump(ScraperPipeline.all_items, fjsonout, ensure_ascii=False, indent=4)

            with open("templates/index.tpl.html", "r", encoding="utf-8") as fhtmltpl:
                template_content = fhtmltpl.read()

            json_str = json.dumps(ScraperPipeline.all_items, ensure_ascii=False)
            formatted_date = datetime.now(UTC).strftime("%d %b %Y")
            html_output = template_content.replace("{{JSONDATA}}", json_str).replace(
                "{{DATA}}", formatted_date
            )

            with open("output/output.html", "w", encoding="utf-8") as fhtmlout:
                fhtmlout.write(html_output)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get("title")

        if not self.job_validator.is_valid(jobtitle=title):
            raise DropItem("Skipped useless Job Title")

        ScraperPipeline.all_items.append(adapter.asdict())
        return item