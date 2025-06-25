import requests
from bs4 import BeautifulSoup
import os
import time
import logging
from urllib.parse import urljoin

class IndianLawScraper:
    """Scraper for Indian laws and legal system content from Wikipedia."""
    
    def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
        """Initialize with base path and setup logging."""
        self.base_path = base_path
        self.output_path = os.path.join(base_path, r"raw\legal_texts")  # Changed to legal_texts
        self.logger = self._setup_logging()
        self.base_url = "https://en.wikipedia.org"
        self.start_urls = [
            "/wiki/Law_of_India",
            "/wiki/Indian_legal_system",
            "/wiki/Constitution_of_India",
            "/wiki/Indian_Penal_Code",
            "/wiki/Code_of_Criminal_Procedure_(India)",
            "/wiki/Indian_Evidence_Act",
            "/wiki/Indian_Contract_Act,_1872",
            "/wiki/Civil_Procedure_Code_(India)",
            "/wiki/Transfer_of_Property_Act_1882",
            "/wiki/Indian_Succession_Act,_1925",
            "/wiki/Hindu_Marriage_Act,_1955",
            "/wiki/Specific_Relief_Act,_1963",
            "/wiki/Consumer_Protection_Act,_2019",
            "/wiki/Right_to_Information_Act,_2005",
            "/wiki/Arbitration_and_Conciliation_Act,_1996",
            "/wiki/Supreme_Court_of_India",
            "/wiki/High_courts_of_India",
            "/wiki/Legal_education_in_India"
        ]
        os.makedirs(self.output_path, exist_ok=True)

    def _setup_logging(self):
        """Configure logging for scraper execution."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(self.base_path, "web_scraper.log")),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def fetch_page(self, url):
        """Fetch page content with error handling and rate limiting."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(1)  # Respect rate limit
            self.logger.info(f"Fetched: {url}")
            return response.text
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {str(e)}")
            return None

    def parse_page(self, html, url):
        """Parse HTML content and extract text."""
        try:
            soup = BeautifulSoup(html, "html.parser")
            content = soup.find("div", class_="mw-parser-output")
            if not content:
                self.logger.warning(f"No content found in {url}")
                return None
            
            # Extract text from paragraphs
            text = "\n".join(p.get_text().strip() for p in content.find_all("p") if p.get_text().strip())
            
            # Follow relevant links within the page
            links = []
            for a in content.find_all("a", href=True):
                href = a["href"]
                if href.startswith("/wiki/") and not href.startswith("/wiki/File:"):
                    full_url = urljoin(self.base_url, href)
                    if any(keyword in href.lower() for keyword in ["india", "law", "legal", "court", "act", "constitution"]):
                        links.append(full_url)
            return text, links
        except Exception as e:
            self.logger.error(f"Failed to parse {url}: {str(e)}")
            return None, []

    def save_content(self, text, filename):
        """Save scraped content to file."""
        try:
            file_path = os.path.join(self.output_path, f"{filename}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            self.logger.info(f"Saved content to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save {filename}: {str(e)}")

    def scrape(self, max_pages=30):
        """Scrape content from start URLs and follow relevant links."""
        visited = set()
        to_visit = [urljoin(self.base_url, url) for url in self.start_urls]
        page_count = 0

        while to_visit and page_count < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            self.logger.info(f"Scraping: {url}")
            html = self.fetch_page(url)
            if not html:
                continue

            text, links = self.parse_page(html, url)
            if text:
                filename = url.split("/")[-1].replace(":", "_")
                self.save_content(text, filename)
                page_count += 1

            # Add new links to visit
            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

            visited.add(url)

        self.logger.info(f"Scraping completed. Processed {page_count} pages.")

if __name__ == "__main__":
    scraper = IndianLawScraper()
    scraper.scrape()