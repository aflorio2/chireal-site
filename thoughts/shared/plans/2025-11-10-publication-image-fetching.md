# Automatic Publication Image Fetching Implementation Plan

## Overview

Implement automatic image fetching for publications on the research page. The system will generate thumbnails from arXiv PDFs and fetch OpenGraph images from publisher pages, with images displayed in the existing "rich" citation style that's already configured on the research page.

## Current State Analysis

The Greene Lab template has complete infrastructure for displaying publication images but zero automatic fetching capability:

**Existing Infrastructure:**
- `_includes/citation.html:13-27` renders images when `style="rich"` and `image` field present
- `research/index.md` already uses `style="rich"` for all citations
- `_styles/citation.scss` provides complete styling and responsive design
- Manual workflow exists: add `image` field to `_data/sources.yaml`

**Current Gaps:**
- 30+ publications in `_data/citations.yaml` have zero image fields
- No plugins fetch or process images
- No image generation or downloading code exists
- Manubot (`_cite/util.py:186-252`) extracts title/authors/dates but no images

**Key Infrastructure Details:**
- Plugin architecture in `_cite/cite.py:26-95` orchestrates plugins sequentially
- Plugins process entries from `_data/*.yaml` files and return sources list
- Each source passes through Manubot (`cite_with_manubot()`) if it has an `id`
- Final citations saved to `_data/citations.yaml:1-50`
- Jekyll builds run locally before git commit (per deployment plan)

## Desired End State

After implementation, the citation system will automatically fetch and display publication images:

**Priority Order:**
1. **Published papers with DOI** → OpenGraph images from publisher (preferred)
2. **arXiv-only papers** (no DOI) → Generated PDF thumbnails
3. Papers with both DOI and arXiv use OpenGraph (published version is canonical)

**For Published Articles (DOI):**
- OpenGraph images extracted from publisher pages (DOI URLs)
- External URLs stored in citation metadata (no local download)
- Fallback chain: og:image → twitter:image → citation_image meta tag
- Rate-limited, robots.txt-compliant scraping
- Used even if paper also has arXiv ID

**For arXiv-Only Papers (no DOI):**
- First-page PDF thumbnails generated locally during `python _cite/cite.py`
- Images stored in `images/publications/` directory (300px wide, PNG format)
- Committed to repository for reliable offline access
- Only used when no DOI available

**User Control:**
- Automatic by default for all publications
- Per-publication opt-out: `skip_image: true` in sources.yaml
- Manual override: explicit `image` field in sources.yaml takes precedence
- Configuration flag: `enable_image_fetching` in inspire-hep.yaml and sources.yaml

**Verification:**
- Run `python _cite/cite.py` successfully generates/fetches images
- Generated citations in `_data/citations.yaml` contain `image` fields
- Jekyll build displays images on research page with rich style
- Images load properly and have appropriate dimensions
- No broken image links or missing thumbnails

## What We're NOT Doing

To prevent scope creep, these are explicitly out of scope:

1. **Image Optimization Pipeline**: No automatic resizing, format conversion (PNG→WebP), or compression of fetched images
2. **Image Caching Service**: No separate image CDN or external hosting service
3. **Multiple Image Sizes**: No responsive image sets (srcset) or multiple resolution variants
4. **Journal Cover Images**: Not fetching journal/publisher logos or cover art
5. **INSPIRE-HEP Thumbnails**: Not scraping INSPIRE-HEP web interface (API doesn't provide images)
6. **Crossref Image API**: Not attempting to fetch images from Crossref metadata (not available)
7. **Author Profile Pictures**: Not fetching author photos or institutional logos
8. **Retroactive Updates**: Not updating existing cached citations (90-day Manubot cache respected)
9. **Interactive Image Management**: No web UI for reviewing/selecting images

## Implementation Approach

**Strategy Overview:**
- Add new plugin `_cite/plugins/image-fetcher.py` to run after all metadata plugins
- Process citations to add `image` field based on available identifiers
- Use PyMuPDF for fast arXiv thumbnail generation (no external dependencies)
- Use requests + BeautifulSoup for OpenGraph scraping with rate limiting
- Respect robots.txt, implement per-domain rate limiting (2+ seconds)
- Store arXiv thumbnails locally, OpenGraph images as external URLs

**Integration Points:**
- Modify `_cite/cite.py:32` to add `image-fetcher` to plugins list (runs last)
- Image fetcher processes existing sources (no Manubot re-querying needed)
- Preserves existing `image` fields from manual entries (no override)
- Respects `skip_image: true` flag to disable per publication

**Technical Decisions:**
- **PyMuPDF over pdf2image**: No external dependencies (Poppler), 2-3x faster
- **Hybrid storage**: Local files for generated content (arXiv), URLs for scraped content (OpenGraph)
- **DOI priority**: Published papers (DOI) use OpenGraph; arXiv thumbnails only for preprints without DOI
- **Automatic with opt-out**: Simplest workflow, maximum coverage, easy to disable
- **Plugin-based**: Fits existing architecture, runs during normal cite.py execution
- **Rate limiting**: 2-second default delay, domain-specific tracking, robots.txt compliance

## Phase 1: arXiv Thumbnail Generation

### Overview
Implement automatic first-page thumbnail generation for arXiv preprints. This provides the highest quality and most reliable images for physics papers.

### Changes Required

#### 1. Install PyMuPDF Dependency
**File**: `_cite/requirements.txt`
**Changes**: Add PyMuPDF library for PDF processing

```txt
manubot~=0.6
PyYAML~=6.0
diskcache~=5.6
rich~=13.6
python-dotenv~=0.21
google-search-results~=2.4
PyMuPDF~=1.24.0
```

**Installation Command**: User must run `pip install -r _cite/requirements.txt`

#### 2. Create arXiv Thumbnail Generator Module
**File**: `_cite/image_utils.py` (NEW)
**Purpose**: Reusable utilities for PDF thumbnail generation

```python
"""
Utility functions for publication image fetching and processing
"""

import fitz  # PyMuPDF
from pathlib import Path
from urllib.request import urlretrieve
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
```

#### 3. Create Image Fetcher Plugin (Phase 1 Only)
**File**: `_cite/plugins/image-fetcher.py` (NEW)
**Purpose**: Plugin to add images to citations

**Note**: In Phase 1, this only handles arXiv-only papers. Phase 2 will add DOI handling with priority logic.

```python
"""
Plugin to fetch publication images from arXiv and publisher pages
"""

import re
from pathlib import Path
from util import get_safe, log
from image_utils import generate_arxiv_thumbnail


def main(entry):
    """
    Receives single citation entry, adds image field if possible.
    Runs as final plugin in chain (after all metadata plugins).

    Returns list with single entry (modified or unmodified).
    """

    # Check if image fetching is disabled for this entry
    if get_safe(entry, "skip_image", False):
        log("Skipping image (skip_image: true)", indent=2, level="INFO")
        return [entry]

    # Check if manual image already provided
    if get_safe(entry, "image", ""):
        log("Using manual image from sources.yaml", indent=2, level="INFO")
        return [entry]

    # Get citation ID
    citation_id = get_safe(entry, "id", "")
    if not citation_id:
        return [entry]

    # PHASE 1: Handle arXiv-only papers (no DOI)
    # Note: Papers with both DOI and arXiv will be handled in Phase 2
    if citation_id.startswith("arxiv:"):
        try:
            # Extract arXiv ID (remove "arxiv:" prefix)
            arxiv_id = citation_id[6:]  # Skip "arxiv:" prefix

            log(f"Fetching arXiv thumbnail for {arxiv_id}", indent=2)

            # Generate thumbnail
            thumbnail_path = generate_arxiv_thumbnail(arxiv_id)

            # Add image field to entry
            entry["image"] = thumbnail_path
            log(f"Added arXiv thumbnail: {thumbnail_path}", indent=2, level="SUCCESS")

        except Exception as e:
            log(f"Could not generate arXiv thumbnail: {e}", indent=2, level="WARNING")

    # Return entry (with or without image)
    return [entry]
```

#### 4. Integrate Image Fetcher into Citation Pipeline
**File**: `_cite/cite.py:32`
**Changes**: Add image-fetcher to plugins list (runs last, after all metadata collected)

```python
# in-order list of plugins to run
plugins = ["google-scholar", "pubmed", "orcid", "inspire-hep", "sources", "image-fetcher"]
```

#### 5. Create Publications Image Directory
**File**: `images/publications/.gitkeep` (NEW)
**Purpose**: Ensure directory exists in git for generated thumbnails

```
# This directory stores automatically generated publication thumbnails
```

**Command**: `mkdir -p images/publications && touch images/publications/.gitkeep`

### Success Criteria

#### Automated Verification:
- [x] Install dependencies successfully: `pip install -r _cite/requirements.txt`
- [x] Create publications directory: `mkdir -p images/publications`
- [x] Run citation generator: `python _cite/cite.py`
- [x] No Python errors during execution
- [x] Generated `_data/citations.yaml` contains `image` fields for arXiv papers
- [x] Thumbnail files exist in `images/publications/` directory
- [x] Thumbnail files are valid PNG images: `file images/publications/*.png`
- [x] Jekyll build succeeds: `bundle exec jekyll build`

#### Manual Verification:
- [ ] Open research page in browser (http://localhost:4000/research/)
- [ ] Verify arXiv paper thumbnails display correctly
- [ ] Check thumbnail quality is acceptable (text readable, not pixelated)
- [ ] Verify thumbnails have appropriate dimensions (~300px wide)
- [ ] Test with publication that has `skip_image: true` - should not generate thumbnail
- [ ] Test with publication that has manual `image` field - should use manual image, not generate

**Implementation Note**: After completing Phase 1 and all automated verification passes, test the feature manually in the browser to confirm thumbnails display properly before proceeding to Phase 2.

---

## Phase 2: OpenGraph Image Fetching

### Overview
Implement OpenGraph (og:image) scraping for published articles with DOI identifiers. This provides images for papers published in journals and conference proceedings.

### Changes Required

#### 1. Install Web Scraping Dependencies
**File**: `_cite/requirements.txt`
**Changes**: Add libraries for HTML parsing and HTTP requests

```txt
manubot~=0.6
PyYAML~=6.0
diskcache~=5.6
rich~=13.6
python-dotenv~=0.21
google-search-results~=2.4
PyMuPDF~=1.24.0
beautifulsoup4~=4.12.0
lxml~=5.0.0
requests~=2.31.0
```

**Note**: requests likely already installed (Manubot dependency), but making explicit

#### 2. Add OpenGraph Fetcher to Image Utils
**File**: `_cite/image_utils.py`
**Changes**: Add functions for OpenGraph scraping with rate limiting and robots.txt compliance

```python
# Add at top of file:
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import defaultdict
from threading import Lock


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
```

#### 3. Extend Image Fetcher Plugin with DOI Priority
**File**: `_cite/plugins/image-fetcher.py`
**Changes**: Add OpenGraph fetching with DOI priority (DOI preferred over arXiv)

```python
"""
Plugin to fetch publication images from arXiv and publisher pages

Priority: Published papers (DOI) use OpenGraph, arXiv-only papers use thumbnails
"""

import re
from pathlib import Path
from util import get_safe, log
from image_utils import generate_arxiv_thumbnail, fetch_opengraph_image


def main(entry):
    """
    Receives single citation entry, adds image field if possible.
    Runs as final plugin in chain (after all metadata plugins).

    Returns list with single entry (modified or unmodified).
    """

    # Check if image fetching is disabled for this entry
    if get_safe(entry, "skip_image", False):
        log("Skipping image (skip_image: true)", indent=2, level="INFO")
        return [entry]

    # Check if manual image already provided
    if get_safe(entry, "image", ""):
        log("Using manual image from sources.yaml", indent=2, level="INFO")
        return [entry]

    # Get citation ID
    citation_id = get_safe(entry, "id", "")
    if not citation_id:
        return [entry]

    # PRIORITY 1: Handle DOI papers (published articles) - ALWAYS PREFERRED
    if citation_id.startswith("doi:"):
        try:
            # Get article URL from citation (added by Manubot)
            article_url = get_safe(entry, "link", "")

            if not article_url:
                log("No link field available for OpenGraph fetching", indent=2, level="INFO")
                return [entry]

            log(f"Fetching OpenGraph image from {article_url}", indent=2)

            # Fetch og:image from publisher page
            image_url = fetch_opengraph_image(article_url)

            if image_url:
                entry["image"] = image_url
                log(f"Added OpenGraph image: {image_url}", indent=2, level="SUCCESS")
            else:
                log("No OpenGraph image found", indent=2, level="INFO")

        except Exception as e:
            log(f"Could not fetch OpenGraph image: {e}", indent=2, level="WARNING")

    # PRIORITY 2: Handle arXiv-only papers (no DOI) - FALLBACK ONLY
    elif citation_id.startswith("arxiv:"):
        try:
            # Extract arXiv ID (remove "arxiv:" prefix)
            arxiv_id = citation_id[6:]

            log(f"Fetching arXiv thumbnail for {arxiv_id}", indent=2)

            # Generate thumbnail
            thumbnail_path = generate_arxiv_thumbnail(arxiv_id)

            # Add image field to entry
            entry["image"] = thumbnail_path
            log(f"Added arXiv thumbnail: {thumbnail_path}", indent=2, level="SUCCESS")

        except Exception as e:
            log(f"Could not generate arXiv thumbnail: {e}", indent=2, level="WARNING")

    # Return entry (with or without image)
    return [entry]
```

### Success Criteria

#### Automated Verification:
- [x] Install dependencies successfully: `pip install -r _cite/requirements.txt`
- [x] Run citation generator: `python _cite/cite.py`
- [x] No Python errors during execution
- [x] Rate limiting works: observe 2+ second delays between requests to same domain
- [x] Generated `_data/citations.yaml` contains `image` fields for DOI papers
- [x] Image URLs are valid absolute URLs (start with https://)
- [x] Jekyll build succeeds: `bundle exec jekyll build`

#### Manual Verification:
- [ ] Open research page in browser
- [ ] Verify DOI paper images display correctly (external URLs)
- [ ] Check image quality is appropriate for publication previews
- [ ] Test with multiple publishers (Springer, APS, Elsevier, etc.)
- [ ] Verify robots.txt compliance: check that blocked sites are skipped
- [ ] Test rate limiting: run cite.py with multiple DOI papers, observe delays
- [ ] Verify fallback behavior: papers without og:image should have no broken images
- [ ] **Test priority logic**: Paper with both DOI and arXiv should use OpenGraph (not arXiv thumbnail)
- [ ] Verify arXiv-only papers still use local thumbnails (no regression from Phase 1)

**Implementation Note**: After completing Phase 2 and all automated verification passes, manually test across multiple publishers to confirm OpenGraph fetching works reliably before proceeding to Phase 3.

---

## Phase 3: Configuration and Documentation

### Overview
Add configuration options for controlling image fetching behavior and document the feature for users.

### Changes Required

#### 1. Add Configuration to INSPIRE-HEP Data File
**File**: `_data/inspire-hep.yaml`
**Changes**: Add enable_image_fetching flag

```yaml
# INSPIRE-HEP author identifier (BAI)
- bai: A.Florio.2

  # Enable automatic metadata enrichment (citation counts, tags, arXiv buttons)
  enable_metadata: true

  # Enable automatic image fetching (arXiv thumbnails, OpenGraph images)
  # Set to false to disable image fetching for all INSPIRE-HEP publications
  enable_image_fetching: true
```

#### 2. Update INSPIRE-HEP Plugin to Pass Configuration
**File**: `_cite/plugins/inspire-hep.py:125-126`
**Changes**: Pass enable_image_fetching flag to sources

```python
        # Copy fields from entry to source (preserves configuration)
        source.update(entry)

        # Preserve enable_image_fetching configuration
        if "enable_image_fetching" in entry:
            source["enable_image_fetching"] = entry["enable_image_fetching"]
```

#### 3. Update Image Fetcher to Respect Configuration
**File**: `_cite/plugins/image-fetcher.py`
**Changes**: Check enable_image_fetching flag at start of main()

```python
def main(entry):
    """
    Receives single citation entry, adds image field if possible.
    Runs as final plugin in chain (after all metadata plugins).

    Returns list with single entry (modified or unmodified).
    """

    # Check if image fetching is disabled globally for this source
    if get_safe(entry, "enable_image_fetching", True) == False:
        log("Image fetching disabled (enable_image_fetching: false)", indent=2, level="INFO")
        return [entry]

    # Check if image fetching is disabled for this entry
    if get_safe(entry, "skip_image", False):
        log("Skipping image (skip_image: true)", indent=2, level="INFO")
        return [entry]

    # ... rest of function unchanged
```

#### 4. Document Manual Image Override in Sources
**File**: `_data/sources.yaml` (update comments)
**Changes**: Add documentation examples

```yaml
# Publications from manual sources
# Use this file to add publications not available via INSPIRE-HEP or other plugins

# Example entry with all fields:
# - id: doi:10.1234/example.56789
#   image: https://example.com/custom-image.jpg  # Manual image (overrides automatic)
#   skip_image: true  # Disable automatic image fetching for this entry
#   title: Custom Title  # Override Manubot-generated title
#   # ... other fields

# Example: Manual image for specific publication
# - id: arxiv:1234.5678
#   image: images/publications/custom-thumbnail.png  # Use custom local image

# Example: Disable image for specific publication
# - id: doi:10.1234/example
#   skip_image: true  # Don't fetch image automatically
```

#### 5. Create User Documentation
**File**: `thoughts/shared/research/2025-11-10-publication-image-usage.md` (NEW)
**Purpose**: Document image fetching feature for users

```markdown
# Publication Image Fetching - User Guide

**Date**: 2025-11-10
**Feature**: Automatic publication image fetching for research page
**Status**: Implemented

## Overview

The citation system automatically fetches images for publications to display on the research page. Images are generated from arXiv PDFs or fetched from publisher pages using OpenGraph tags.

## How It Works

### Automatic Behavior

When you run `python _cite/cite.py`, the system automatically:

1. **For published papers** (id starts with `doi:`) - **PRIORITY 1**:
   - Fetches the article page from the publisher
   - Extracts OpenGraph image URL (og:image meta tag)
   - Adds external image URL to citation metadata
   - **Used even if paper also has arXiv ID** (published version preferred)

2. **For arXiv-only papers** (id starts with `arxiv:` and no DOI) - **FALLBACK**:
   - Downloads the PDF from arXiv
   - Generates a thumbnail from the first page
   - Saves thumbnail to `images/publications/` directory
   - Adds image path to citation metadata

3. **Rate limiting and politeness**:
   - Respects robots.txt for all domains
   - Waits 2+ seconds between requests to same domain
   - Uses descriptive User-Agent identifying the bot

### Priority Logic

The system prioritizes published papers over preprints:
- Paper with **DOI only** → OpenGraph image from publisher
- Paper with **arXiv only** → Generated PDF thumbnail
- Paper with **both DOI and arXiv** → OpenGraph image (DOI wins)

### Image Display

Images appear on the research page when:
- The research page uses `style="rich"` (already configured)
- The citation has an `image` field in `_data/citations.yaml`
- Images are lazy-loaded for performance

## Configuration Options

### Global Configuration

Disable image fetching for all INSPIRE-HEP publications:

**File**: `_data/inspire-hep.yaml`

```yaml
- bai: A.Florio.2
  enable_image_fetching: false  # Disable for all papers
```

### Per-Publication Control

#### Skip Image for Specific Publication

**File**: `_data/sources.yaml`

```yaml
- id: doi:10.1234/example
  skip_image: true  # Don't fetch image for this paper
```

#### Manual Image Override

**File**: `_data/sources.yaml`

```yaml
# Use external URL
- id: arxiv:1234.5678
  image: https://example.com/custom-thumbnail.jpg

# Use local file
- id: doi:10.1234/example
  image: images/publications/custom-image.png
```

Manual `image` fields always take precedence over automatic fetching.

## Troubleshooting

### Image Not Appearing

1. **Check citation metadata**: Look in `_data/citations.yaml` for the `image` field
   - If missing, image fetching may have failed
   - Check console output from `python _cite/cite.py` for warnings

2. **For arXiv papers**:
   - Verify thumbnail exists: `ls images/publications/`
   - Check file is valid: `file images/publications/*.png`
   - Ensure images directory is committed to git

3. **For DOI papers**:
   - Check that publisher page has og:image meta tag
   - Test URL directly: visit the article page and inspect HTML
   - Some publishers don't provide og:image (expected)

4. **Check Jekyll build**: Run `bundle exec jekyll build` and check for errors

### Disabling Problematic Images

If a specific image doesn't work or looks bad:

```yaml
- id: arxiv:1234.5678
  skip_image: true  # Disable automatic image
```

Or provide a better manual image:

```yaml
- id: arxiv:1234.5678
  image: images/publications/better-thumbnail.png
```

### Re-generating Thumbnails

To regenerate a specific arXiv thumbnail:

```bash
# Delete existing thumbnail
rm images/publications/1234_5678.png

# Re-run citation generator
python _cite/cite.py
```

### Rate Limiting Errors

If you see warnings about robots.txt or rate limiting:
- This is expected behavior (being polite to publishers)
- The system automatically skips blocked URLs
- Images will be missing for blocked publishers (expected)

## Technical Details

### Image Specifications

- **arXiv thumbnails**: 300px wide, PNG format, ~50-100 KB
- **OpenGraph images**: External URLs, dimensions vary by publisher
- **Storage**: arXiv in git, OpenGraph as external URLs

### File Locations

- Generated thumbnails: `images/publications/*.png`
- PDF cache: `_cite/.cache/pdfs/*.pdf`
- Plugin code: `_cite/plugins/image-fetcher.py`
- Utilities: `_cite/image_utils.py`

### Dependencies

Required Python packages (in `_cite/requirements.txt`):
- PyMuPDF: PDF thumbnail generation
- beautifulsoup4: HTML parsing
- lxml: Fast HTML parser
- requests: HTTP requests

Install with: `pip install -r _cite/requirements.txt`

## Examples

### Example: arXiv-Only Paper (Preprint)

**Input** (`_data/inspire-hep.yaml`):
```yaml
- bai: A.Florio.2
  enable_image_fetching: true
```

**Output** (`_data/citations.yaml`) for paper with no DOI:
```yaml
- id: arxiv:2511.01966
  title: 'Entanglement asymmetry in gauge theories...'
  authors:
  - Adrien Florio
  - Sara Murciano
  publisher: arXiv
  date: '2025-11-05'
  link: https://arxiv.org/abs/2511.01966
  image: images/publications/2511_01966.png  # ← Local thumbnail (no DOI)
  buttons:
  - type: preprint
    text: arXiv
    link: https://arxiv.org/abs/2511.01966
```

### Example: Published Paper (DOI)

**Output** (`_data/citations.yaml`) for paper with DOI:
```yaml
- id: doi:10.1103/PhysRevLett.130.131801
  title: 'Search for Exotic Higgs Boson Decays...'
  authors:
  - ATLAS Collaboration
  publisher: Physical Review Letters
  date: '2023-03-31'
  link: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.131801
  image: https://journals.aps.org/prl/article/10.1103/PhysRevLett.130.131801/figures/1/medium  # ← OpenGraph (has DOI)
  buttons:
  - type: preprint
    text: arXiv
    link: https://arxiv.org/abs/2207.00178
```

**Note**: Even though this paper also has arXiv:2207.00178, it uses OpenGraph because DOI is preferred.

### Mixed Configuration

```yaml
# INSPIRE-HEP publications (automatic)
# _data/inspire-hep.yaml
- bai: A.Florio.2
  enable_image_fetching: true

# Manual entries with custom images
# _data/sources.yaml
- id: doi:10.1234/special-paper
  image: https://example.com/custom-image.jpg  # Manual image

- id: arxiv:9999.9999
  skip_image: true  # No image for this one

- id: doi:10.5678/another-paper
  # No image field = automatic fetching (if enable_image_fetching: true)
```

## Best Practices

1. **Let it run automatically**: Most publications will get good images automatically
2. **Override when needed**: Use manual `image` field for special cases
3. **Skip problematic images**: Use `skip_image: true` for papers with poor thumbnails
4. **Commit generated images**: Always commit `images/publications/` to git
5. **Check image quality**: Review research page after adding new publications

## Related Documentation

- Phase 5 Publication Workflow: `thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md`
- INSPIRE-HEP Plugin: `thoughts/shared/plans/2025-11-10-inspire-hep-citation-fetcher.md`
- Image Fetching Research: `thoughts/shared/research/2025-11-10-publication-image-fetching.md`
```

### Success Criteria

#### Automated Verification:
- [ ] Configuration flags parse correctly: `python -c "from util import load_data; print(load_data('_data/inspire-hep.yaml'))"`
- [ ] Run citation generator with enable_image_fetching: false: `python _cite/cite.py`
- [ ] Verify no images added when disabled: `grep -c "^  image:" _data/citations.yaml`
- [ ] Run citation generator with enable_image_fetching: true: `python _cite/cite.py`
- [ ] Verify images added when enabled: `grep "^  image:" _data/citations.yaml | head -5`
- [ ] Jekyll build succeeds: `bundle exec jekyll build`

#### Manual Verification:
- [ ] Test global disable: set enable_image_fetching: false, run cite.py, verify no images added
- [ ] Test global enable: set enable_image_fetching: true, run cite.py, verify images added
- [ ] Test per-publication disable: add skip_image: true to one entry, verify it has no image
- [ ] Test manual override: add explicit image field, verify it's used instead of automatic
- [ ] Review user documentation for clarity and completeness
- [ ] Test that configuration is preserved through plugin chain (INSPIRE-HEP → image-fetcher)

**Implementation Note**: After completing Phase 3, review the user documentation with a fresh perspective to ensure it's clear and complete for end users.

---

## Testing Strategy

### Unit Testing

No formal unit tests created (plugin architecture doesn't have test framework), but manual testing covers:

**Image Generation**:
- arXiv PDF download and caching
- Thumbnail generation from first page
- Output file path and format
- Error handling for invalid PDFs

**OpenGraph Fetching**:
- HTML parsing for og:image tags
- Fallback chain (og:image → twitter:image → citation_image)
- URL normalization (relative → absolute)
- Rate limiting enforcement
- robots.txt compliance

**Plugin Integration**:
- Entry processing (input/output format)
- Configuration flag handling
- Manual override preservation
- skip_image flag handling

### Integration Testing

**Complete Citation Pipeline**:
1. Create test entries in `_data/sources.yaml`:
   - arXiv paper (for thumbnail generation)
   - DOI paper (for OpenGraph fetching)
   - Manual image override
   - skip_image: true entry
   - enable_image_fetching: false configuration

2. Run `python _cite/cite.py` and verify:
   - No errors during execution
   - Generated `_data/citations.yaml` has correct image fields
   - Thumbnail files created in `images/publications/`
   - External URLs valid for DOI papers
   - Manual overrides preserved
   - Skipped entries have no images

3. Run Jekyll build and verify:
   - Build succeeds without errors
   - Research page displays all images
   - No broken image links
   - Images load with lazy loading

### Manual Testing Checklist

**Phase 1 Testing** (after Phase 1 completion):
- [ ] Create test arXiv entry in sources.yaml
- [ ] Run cite.py, observe console output
- [ ] Check thumbnail generated in images/publications/
- [ ] View research page, verify image displays
- [ ] Test with multiple arXiv papers (old and new ID formats)
- [ ] Test with invalid arXiv ID (should fail gracefully)

**Phase 2 Testing** (after Phase 2 completion):
- [ ] Create test DOI entry in sources.yaml
- [ ] Run cite.py, observe rate limiting delays
- [ ] Check external image URL in citations.yaml
- [ ] View research page, verify external image loads
- [ ] Test with multiple publishers (Springer, APS, etc.)
- [ ] Test with URL that has no og:image (should skip gracefully)
- [ ] Test with URL that redirects (should follow)

**Phase 3 Testing** (after Phase 3 completion):
- [ ] Test enable_image_fetching: false (global disable)
- [ ] Test skip_image: true (per-publication disable)
- [ ] Test manual image field (should override automatic)
- [ ] Test mixed configuration (some enabled, some disabled)
- [ ] Review documentation for accuracy

**Edge Cases**:
- [ ] Paper with both arXiv and DOI (should use OpenGraph, not arXiv thumbnail)
- [ ] Paper with no identifiers (should skip)
- [ ] Rate limiting across multiple domains
- [ ] robots.txt blocking specific domains
- [ ] Network timeout handling
- [ ] Malformed HTML from publisher
- [ ] Data URI in og:image (should skip)
- [ ] Relative URL in og:image (should convert to absolute)
- [ ] DOI paper without og:image (should gracefully skip, no fallback to arXiv)

## Performance Considerations

### Build Time Impact

**Current State**: `python _cite/cite.py` processes 30+ publications in ~5-10 seconds (mostly Manubot caching)

**Expected Impact with Image Fetching**:
- **First run** (no cache): +30-60 seconds
  - arXiv PDF downloads: ~1-2 seconds per paper
  - OpenGraph fetching: ~2-4 seconds per paper (rate limiting)
  - Total: ~10-20 papers/minute with rate limiting

- **Subsequent runs** (with cache): +5-10 seconds
  - arXiv thumbnails cached (no regeneration)
  - OpenGraph URLs cached (no refetching)
  - Only new papers processed

**Optimization Strategies**:
- PDF cache (`_cite/.cache/pdfs/`) persists across runs
- Thumbnail existence check before generation
- OpenGraph results cached (image_utils uses util.py cache)
- Rate limiting per-domain (not global)

### Repository Size Impact

**arXiv Thumbnails**:
- ~50-100 KB per thumbnail (PNG format, 300px wide)
- 30 papers = ~1.5-3 MB total
- 100 papers = ~5-10 MB total
- Committed to git (increases repository size)

**OpenGraph Images**:
- External URLs only (no local storage)
- Zero repository size impact
- Depends on external availability

**PDF Cache**:
- ~500 KB - 5 MB per arXiv PDF
- Stored in `_cite/.cache/` (not committed to git)
- Can be deleted to free disk space (`rm -rf _cite/.cache/pdfs/`)

### Network Usage

**Rate Limiting**:
- 2+ seconds between requests to same domain
- Respects robots.txt crawl-delay if specified
- Concurrent requests to different domains allowed

**Total Network Load** (first run, 30 papers):
- arXiv PDF downloads: ~15-50 MB (10 arXiv papers)
- OpenGraph fetching: ~1-5 MB HTML (20 DOI papers)
- Total: ~20-60 MB download
- Time: ~2-5 minutes with rate limiting

**Subsequent Runs**:
- Only new papers processed
- Cached results reused
- Minimal network usage

## Migration Notes

### Existing Publications

**Current State**: 30+ publications in `_data/citations.yaml` with zero image fields

**After Implementation**:
- Existing publications **will not** automatically get images
- Manubot caches citations for 90 days (no re-querying)
- Images only added to new publications or re-processed entries

**To Regenerate Images for Existing Publications**:

Option 1: Clear Manubot cache (regenerates all citations)
```bash
rm -rf _cite/.cache/manubot/
python _cite/cite.py
```

Option 2: Force re-processing of specific entries
```yaml
# _data/sources.yaml
# Add entries for papers you want images for:
- id: arxiv:2511.01966  # Already in citations.yaml via INSPIRE-HEP
  # Will be merged with existing entry and get image field
```

Option 3: Wait for cache expiration (90 days)
- Manubot cache expires after 90 days
- Papers will automatically re-process and get images

### Git Workflow

**New Files to Commit**:
```bash
git add _cite/plugins/image-fetcher.py
git add _cite/image_utils.py
git add _cite/requirements.txt
git add images/publications/*.png
git add _data/citations.yaml
git add thoughts/shared/plans/2025-11-10-publication-image-fetching.md
git add thoughts/shared/research/2025-11-10-publication-image-usage.md
```

**Files NOT to Commit** (.gitignore already configured):
```
_cite/.cache/       # PDF cache and other cached data
.bundle/            # Jekyll dependencies
_site/              # Generated Jekyll site
```

### Deployment Checklist

Before first production run:
1. [ ] Install dependencies: `pip install -r _cite/requirements.txt`
2. [ ] Create images directory: `mkdir -p images/publications`
3. [ ] Test with small dataset (2-3 papers) first
4. [ ] Review console output for warnings/errors
5. [ ] Check generated images quality
6. [ ] Commit images to git
7. [ ] Test Jekyll build locally
8. [ ] Push to GitLab CI/CD pipeline

### Rollback Plan

If issues arise, rollback is straightforward:

1. Remove image-fetcher from plugins list:
   ```python
   # _cite/cite.py:32
   plugins = ["google-scholar", "pubmed", "orcid", "inspire-hep", "sources"]
   ```

2. Regenerate citations without images:
   ```bash
   python _cite/cite.py
   ```

3. Images will disappear from research page (no broken links, fallback handled by template)

4. To fully remove:
   ```bash
   git rm _cite/plugins/image-fetcher.py
   git rm _cite/image_utils.py
   git rm images/publications/*.png
   git restore _cite/requirements.txt
   git commit -m "Rollback: Remove automatic image fetching"
   ```

## References

### Research Documents
- **Original Research**: `thoughts/shared/research/2025-11-10-publication-image-fetching.md`
- **Phase 5 Workflow**: `thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md`
- **INSPIRE-HEP Plugin**: `thoughts/shared/plans/2025-11-10-inspire-hep-citation-fetcher.md`
- **Greene Lab Setup**: `thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`

### External Documentation
- **arXiv API**: https://info.arxiv.org/help/api/user-manual.html
- **arXiv Terms of Use**: https://info.arxiv.org/help/api/tou.html
- **OpenGraph Protocol**: https://ogp.me/
- **PyMuPDF Documentation**: https://pymupdf.readthedocs.io/
- **BeautifulSoup4 Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **robots.txt Specification**: https://www.robotstxt.org/

### Code References
- **Citation Display**: `_includes/citation.html:13-27`
- **Research Page**: `research/index.md:14-34`
- **Plugin Orchestration**: `_cite/cite.py:26-95`
- **Manubot Integration**: `_cite/util.py:186-252`
- **INSPIRE-HEP Plugin**: `_cite/plugins/inspire-hep.py:1-132`
- **Sources Plugin**: `_cite/plugins/sources.py:1-6`

### Similar Implementations
- **Project Images**: `_data/projects.yaml` (manual local images pattern to follow)
- **Citation Styling**: `_styles/citation.scss` (existing image styling)
- **Fallback Handler**: `_includes/fallback.html` (handles missing images gracefully)
