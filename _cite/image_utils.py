"""
Utility functions for publication image fetching and processing
"""

import fitz  # PyMuPDF
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import defaultdict
from threading import Lock
from util import log


def download_arxiv_pdf(arxiv_id, cache_dir="_cite/.cache/pdfs"):
    """
    Download PDF from arXiv with file-based caching.

    Args:
        arxiv_id: arXiv identifier (e.g., "2511.01966" or "hep-th/9901001")
        cache_dir: Directory for cached PDFs

    Returns:
        Path to downloaded PDF file
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    # Normalize arXiv ID for filename (replace / with _)
    safe_id = arxiv_id.replace("/", "_")
    pdf_path = cache_path / f"{safe_id}.pdf"

    # Check cache first
    if pdf_path.exists():
        log(f"Using cached PDF: {arxiv_id}", indent=2, level="INFO")
        return pdf_path

    # Download from arXiv
    arxiv_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    log(f"Downloading arXiv PDF: {arxiv_id}", indent=2)

    try:
        urlretrieve(arxiv_url, pdf_path)
        return pdf_path
    except Exception as e:
        raise Exception(f"Failed to download arXiv PDF {arxiv_id}: {e}")


def generate_thumbnail(pdf_path, output_path, width=300):
    """
    Generate thumbnail from first page of PDF.

    Args:
        pdf_path: Path to source PDF file
        output_path: Path for output thumbnail image
        width: Target width in pixels (height auto-scaled)

    Returns:
        Path to generated thumbnail
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip if thumbnail already exists
    if output_path.exists():
        log(f"Thumbnail exists: {output_path.name}", indent=2, level="INFO")
        return output_path

    log(f"Generating thumbnail: {output_path.name}", indent=2)

    try:
        # Open PDF and get first page
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)

        # Calculate zoom to achieve target width
        page_rect = page.rect
        zoom = width / page_rect.width
        mat = fitz.Matrix(zoom, zoom)

        # Render page to image (no alpha channel for smaller files)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(output_path))

        doc.close()
        return output_path

    except Exception as e:
        raise Exception(f"Failed to generate thumbnail from {pdf_path}: {e}")


def generate_arxiv_thumbnail(arxiv_id, output_dir="images/publications", width=300):
    """
    Complete workflow: download arXiv PDF and generate thumbnail.

    Args:
        arxiv_id: arXiv identifier
        output_dir: Directory for output thumbnails
        width: Target thumbnail width in pixels

    Returns:
        Relative path to thumbnail (for Jekyll site)
    """
    # Normalize arXiv ID for filename
    safe_id = arxiv_id.replace("/", "_")
    output_path = Path(output_dir) / f"{safe_id}.png"

    # Skip if thumbnail already exists
    if output_path.exists():
        return str(output_path)

    # Download PDF
    pdf_path = download_arxiv_pdf(arxiv_id)

    # Generate thumbnail
    generate_thumbnail(pdf_path, output_path, width)

    return str(output_path)


# Module-level state for rate limiting
class RateLimiter:
    """Domain-specific rate limiter with robots.txt compliance."""

    def __init__(self, default_delay=2.0):
        self.default_delay = default_delay
        self.last_request = defaultdict(float)
        self.lock = Lock()
        self.robots_parsers = {}

    def _get_robots_parser(self, url):
        """Get or create robots.txt parser for domain."""
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"

        if domain not in self.robots_parsers:
            rp = RobotFileParser()
            robots_url = urljoin(domain, "/robots.txt")
            rp.set_url(robots_url)

            try:
                rp.read()
                self.robots_parsers[domain] = rp
            except Exception:
                # If can't read robots.txt, assume allowed
                self.robots_parsers[domain] = None

        return self.robots_parsers[domain]

    def can_fetch(self, url, user_agent="*"):
        """Check if URL can be fetched per robots.txt."""
        rp = self._get_robots_parser(url)
        if rp is None:
            return True
        return rp.can_fetch(user_agent, url)

    def get_crawl_delay(self, url, user_agent="*"):
        """Get crawl delay from robots.txt."""
        rp = self._get_robots_parser(url)
        if rp is None:
            return self.default_delay

        delay = rp.crawl_delay(user_agent)
        return delay if delay else self.default_delay

    def wait_if_needed(self, url):
        """Enforce rate limiting per domain."""
        parsed = urlparse(url)
        domain = parsed.netloc

        with self.lock:
            delay = self.get_crawl_delay(url)
            time_since_last = time.time() - self.last_request[domain]

            if time_since_last < delay:
                wait_time = delay - time_since_last
                time.sleep(wait_time)

            self.last_request[domain] = time.time()


# Global rate limiter instance
_rate_limiter = RateLimiter(default_delay=2.0)


def fetch_opengraph_image(url, timeout=(5, 15)):
    """
    Fetch og:image URL from article page.

    Args:
        url: URL of the article page
        timeout: (connect_timeout, read_timeout) in seconds

    Returns:
        Image URL string or None if not found
    """
    # User agent identifies this bot
    user_agent = (
        "PublicationImageBot/1.0 "
        "(Jekyll static site generator; +https://github.com/greenelab/lab-website-template)"
    )

    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    # Check robots.txt
    if not _rate_limiter.can_fetch(url, user_agent):
        log(f"Blocked by robots.txt: {url}", indent=2, level="WARNING")
        return None

    # Apply rate limiting
    _rate_limiter.wait_if_needed(url)

    # Fetch HTML
    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        log(f"Timeout fetching {url}", indent=2, level="WARNING")
        return None
    except requests.exceptions.RequestException as e:
        log(f"Error fetching {url}: {e}", indent=2, level="WARNING")
        return None

    # Parse HTML
    try:
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        log(f"Error parsing HTML from {url}: {e}", indent=2, level="WARNING")
        return None

    # Try multiple strategies for finding images

    # Strategy 1: OpenGraph og:image
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image_url = og_image["content"]
        return _normalize_image_url(image_url, url)

    # Strategy 2: Twitter Card image
    twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
    if twitter_image and twitter_image.get("content"):
        image_url = twitter_image["content"]
        return _normalize_image_url(image_url, url)

    # Strategy 3: citation_image meta tag (common in academic papers)
    citation_image = soup.find("meta", attrs={"name": "citation_image"})
    if citation_image and citation_image.get("content"):
        image_url = citation_image["content"]
        return _normalize_image_url(image_url, url)

    # Strategy 4: Schema.org image
    schema_image = soup.find("meta", attrs={"itemprop": "image"})
    if schema_image and schema_image.get("content"):
        image_url = schema_image["content"]
        return _normalize_image_url(image_url, url)

    # No image found
    return None


def _normalize_image_url(image_url, base_url):
    """
    Normalize and validate image URL.

    Args:
        image_url: Image URL from meta tag (may be relative)
        base_url: Base URL for resolving relative paths

    Returns:
        Absolute image URL or None if invalid
    """
    if not image_url:
        return None

    # Skip data URIs (usually placeholders)
    if image_url.startswith('data:'):
        return None

    # Convert relative URLs to absolute
    if not image_url.startswith(('http://', 'https://')):
        image_url = urljoin(base_url, image_url)

    # Validate URL
    parsed = urlparse(image_url)
    if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
        return None

    return image_url


def get_journal_logo(publisher_name):
    """
    Map publisher name to journal logo file.

    Args:
        publisher_name: Publisher name from citation metadata

    Returns:
        Relative path to logo file or None if no logo available
    """
    if not publisher_name:
        return None

    # Normalize publisher name for matching
    publisher_lower = publisher_name.lower()

    # Publisher to logo mapping
    logo_map = {
        'physical review d': 'images/journals/PRD.jpg',
        'physical review letters': 'images/journals/PRL.jpg',
        'physical review applied': 'images/journals/PRApplied.jpg',
        'scipost physics': 'images/journals/logo_scipost_RGB_HTML_groot.png',
        'the european physical journal c': 'images/journals/EPJC.png',
        'journal of cosmology and astroparticle physics': 'images/journals/JCAP.jpeg',
        'reports on progress in physics': 'images/journals/ReptProgPhys.jpg',
    }

    # Check for exact match
    if publisher_lower in logo_map:
        return logo_map[publisher_lower]

    # Check for partial matches
    for key, logo_path in logo_map.items():
        if key in publisher_lower or publisher_lower in key:
            return logo_path

    return None
