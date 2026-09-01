from scrapy.crawler import AsyncCrawlerProcess
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings


def run_all():
    settings = get_project_settings()
    process = AsyncCrawlerProcess(settings)

    spider_loader = SpiderLoader.from_settings(settings)
    
    for spider_name in spider_loader.list():
        process.crawl(spider_name)

    process.start()

if __name__ == "__main__":
    run_all()