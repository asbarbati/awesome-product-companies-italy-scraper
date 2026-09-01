# Contributing

Thank you for considering contributing to this project! Community contributions help keep our spider list active, accurate, and up-to-date.

## How to Contribute

1. **Verify Company Availability:**  
   Check the company listings on [https://github.com/asbarbati/awesome-product-companies-italy](https://github.com/asbarbati/awesome-product-companies-italy) and select an un-implemented product company with open tech roles.

2. **Fork the Repository:**  
   Fork this repository to your own GitHub account and create a local branch for your feature:
   ```bash
   git clone https://github.com/your-username/awesome-product-companies-italy-scraper.git
   cd awesome-product-companies-italy-scraper
   uv sync
   git checkout -b feature/add-spider-<company-name>

3. Implement Your Changes:

    Create a new Scrapy spider inside src/awesome_product_companies_italy_scraper/scraper/spiders/.

    > Naming Convention: The filename must start with s (e.g., s3bee.py or s<company_name>.py).

    Ensure your spider returns standard fields (company, title, location, url).

4. Test the Spider:

    Run your spider locally to ensure it correctly extracts job listings without errors:
    Bash

    `uv run --directory src/awesome_product_companies_italy_scraper/scraper scrapy crawl <spider_name>`

5. Submit a Pull Request (PR):

    Commit your changes, push the branch to your fork, and submit a PR to the main branch with a brief description of the spider added and a quick sample of the scraped data.

---