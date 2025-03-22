# Web Crawler for Documentation

This project is a Python-based web crawler that fetches content from web pages listed in a sitemap and saves it as markdown files. It leverages the crawl4ai library for asynchronous crawling, making it efficient for processing multiple URLs while reusing a single browser session. The script is designed to avoid redundant work by skipping URLs whose markdown files already exist.

## Features

- **Asynchronous Crawling**: Processes URLs concurrently for better performance.
- **Session Reuse**: Uses a single browser session across all URLs to optimize resource usage.
- **Duplicate Avoidance**: Skips URLs if their markdown files already exist in the output directory.
- **Flexible Sitemap**: Allows crawling any website by changing the sitemap URL.
- **Markdown Output**: Saves page content as markdown files for easy readability and storage.

## Requirements

- **Python**: Version 3.7 or higher
- **Libraries**:
    - crawl4ai: For web crawling functionality
    - requests: For fetching the sitemap
    - asyncio: For asynchronous operations (included with Python)

## Installation

1. **Clone or Download**: Obtain the script by cloning this repository or downloading the file directly.
2. **Install Dependencies**: Run the following command in your terminal or command prompt:

```bash
pip install crawl4ai requests
```

## Usage

1. **Set Up Dependencies**: Ensure all required libraries are installed as described in the Installation section.
2. **Configure the Sitemap URL**: Open the script and locate the `get_pydantic_ai_docs_urls()` function. Modify the `sitemap_url` variable to point to the sitemap of the website you want to crawl. For example:

```python
sitemap_url = "https://example.com/sitemap.xml"
```

The default is set to "https://aveosoftware.ca/sitemap.xml", but you can replace it with any valid sitemap URL (e.g., "https://docs.python.org/sitemap.xml" or "https://yourwebsite.com/sitemap.xml").

> **Important**: Ensure the website permits crawling by checking its robots.txt file and terms of service.

3. **Run the Script**: Execute the script from the command line:

```bash
python crawler.py
```

4. **Check Output**: The script will:
     - Fetch URLs from the specified sitemap.
     - Crawl each page asynchronously.
     - Save the content as markdown files in the output directory.

## Configuration

- **Sitemap URL**: Edit the `sitemap_url` in `get_pydantic_ai_docs_urls()` to target a different website's sitemap.
- **Output Directory**: Markdown files are saved in the output directory by default. To change this, modify the `output_dir` parameter in the `save_markdown()` function, e.g.:

```python
save_markdown(url, markdown, output_dir="custom_output")
```

- **Browser Settings**: The crawler runs in headless mode with options optimized for environments like Docker (`--disable-gpu`, `--no-sandbox`, etc.). Adjust these in the `BrowserConfig` instantiation if needed:

```python
browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"]
)
```

## Output

- **File Naming**: Each markdown file is named after its URL, with non-alphanumeric characters replaced by underscores (e.g., `https_example_com_page_md`).
- **Location**: Files are stored in the output directory (or your custom directory).
- **Skipping Existing Files**: If a markdown file already exists for a URL, the script skips that URL to avoid overwriting.

## Troubleshooting

- **Browser Fails to Launch**: If the browser doesn't start or crashes:
    - Verify that crawl4ai dependencies (e.g., Chrome/Chromium) are installed.
    - Check system compatibility and permissions.
- **Sitemap Errors**: If the sitemap fails to load:
    - Confirm the URL is correct and accessible.
    - Ensure it follows the standard XML sitemap format (`<loc>` tags within a `<urlset>`).
- **Empty Markdown**: If markdown files are empty or incomplete:
    - Review the `DefaultMarkdownGenerator` configuration in `CrawlerRunConfig`.
    - Test with a different URL to isolate the issue.

## Contributing

Feel free to contribute by submitting pull requests or reporting issues. Suggestions for improving performance, adding features, or enhancing error handling are welcome!