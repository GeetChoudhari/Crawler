import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import os
import re


def save_markdown(url: str, markdown: str, output_dir: str = "output"):
    """
    Saves the markdown content to a file based on the URL.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Create a safe filename from the URL
    safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url)
    file_path = os.path.join(output_dir, f"{safe_filename}.md")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown)
    print(f"Saved markdown to {file_path}")


async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        session_id = "session1"  # Reuse the same session across all URLs
        for url in urls:
            # Generate the safe filename and check if the file already exists
            safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url)
            output_file = os.path.join("output", f"{safe_filename}.md")
            if os.path.exists(output_file):
                print(f"Skipping {url}, markdown file already exists.")
                continue

            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                # Check markdown length
                print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")
                # Save markdown content to a file
                save_markdown(url, result.markdown_v2.raw_markdown)
            else:
                print(f"Failed: {url} - Error: {result.error_message}")
    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()


def get_pydantic_ai_docs_urls():
    """
    Fetches all URLs from the Pydantic AI documentation.
    Uses the sitemap (https://docs.crawl4ai.com/sitemap.xml) to get these URLs.
    
    Returns:
        List[str]: List of URLs with duplicates removed.
    """            
    sitemap_url = "https://example.com/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        # Remove duplicate URLs if any
        unique_urls = list(dict.fromkeys(urls))
        return unique_urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No URLs found to crawl")


if __name__ == "__main__":
    asyncio.run(main())
