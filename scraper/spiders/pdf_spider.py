import scrapy
from scrapy.utils.project import get_project_settings

class PdfSpiderSpider(scrapy.Spider):
    name = "pdf_spider"
    allowed_domains = ["www.thenationalcouncil.org"]
    start_urls = ["https://www.thenationalcouncil.org/resources/"]


    def parse(self, response):
        # Extract resource links
        resource_links = response.css(".featured-content__content a::attr(href)").getall()
        self.logger.debug(f"Found resource links: {resource_links}")  # Log the scraped links

        for link in resource_links:
            self.logger.info(f"Scraped Link: {link}")  # Log the scraped link
            yield scrapy.Request(link, callback=self.parse_resource)

        # Follow pagination links (if any)
        next_page = response.css("link[rel='next']::attr(href)").get()
        self.logger.info(f"Scraped next page number: {next_page}")  # Log the scraped link
        if next_page:
            self.logger.debug(f"Following pagination link: {next_page}")  # Log the pagination link
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_resource(self, response):
        self.logger.debug(f"Parsing resource page: {response.url}")

        # Check for PDF links
        pdf_link = response.css("a[href*='.pdf']::attr(href)").get()

        if pdf_link:
            # Download PDF
            filename = pdf_link.split("/")[-1]
            self.logger.debug(f"PDF: {pdf_link} as {filename}")
            yield {
                "resource_url": response.url,
                "pdf_url": pdf_link,
                "pdf_filename": filename,
            }

            # You can customize the download location here
            # with open(f"downloads/{filename}", "wb") as f:
                # f.write(response.css("a[href*='.pdf']").xpath("@href").getall()[0].response.body)

# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess(get_project_settings())

# process.crawl(PdfSpiderSpider)
# process.start()