"""
Plugin to fetch publication images from arXiv and publisher pages

Multi-tier fallback strategy:
1. OpenGraph from DOI URL (best - actual article images)
2. Journal logo (good - branded, clean appearance)
3. arXiv thumbnail (acceptable - actual first page but can be messy)
4. No image (template handles gracefully)
"""

import re
from pathlib import Path
from util import get_safe, log
from image_utils import generate_arxiv_thumbnail, fetch_opengraph_image, get_journal_logo


def _extract_arxiv_id_from_buttons(entry):
    """Extract arXiv ID from buttons field if present."""
    buttons = get_safe(entry, "buttons", [])
    for button in buttons:
        if button.get('type') == 'preprint':
            link = button.get('link', '')
            if 'arxiv.org' in link:
                # Extract ID from URL like https://arxiv.org/abs/2506.14983
                parts = link.split('/')
                if len(parts) > 0:
                    return parts[-1]
    return None


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

    # PRIORITY 1: Handle DOI papers (published articles)
    if citation_id.startswith("doi:"):
        publisher = get_safe(entry, "publisher", "")

        # Special case: For publishers with logos, prefer logo over OpenGraph
        # (some OpenGraph images are low quality or missing)
        publishers_prefer_logo = [
            'the european physical journal c',
        ]

        if publisher and publisher.lower() in publishers_prefer_logo:
            logo_path = get_journal_logo(publisher)
            if logo_path:
                entry["image"] = logo_path
                log(f"Added journal logo (preferred): {logo_path}", indent=2, level="SUCCESS")
                return [entry]

        # Try OpenGraph first for other publishers
        try:
            article_url = get_safe(entry, "link", "")
            if article_url:
                log(f"Fetching OpenGraph image from {article_url}", indent=2)
                image_url = fetch_opengraph_image(article_url)
                if image_url:
                    entry["image"] = image_url
                    log(f"Added OpenGraph image: {image_url}", indent=2, level="SUCCESS")
                    return [entry]
                else:
                    log("No OpenGraph image found", indent=2, level="INFO")
        except Exception as e:
            log(f"Could not fetch OpenGraph image: {e}", indent=2, level="WARNING")

        # FALLBACK 1: Try journal logo
        if publisher:
            logo_path = get_journal_logo(publisher)
            if logo_path:
                entry["image"] = logo_path
                log(f"Added journal logo: {logo_path}", indent=2, level="SUCCESS")
                return [entry]

        # FALLBACK 2: Try arXiv thumbnail if paper has arXiv
        arxiv_id = _extract_arxiv_id_from_buttons(entry)
        if arxiv_id:
            try:
                log(f"Trying arXiv fallback for {arxiv_id}", indent=2)
                thumbnail_path = generate_arxiv_thumbnail(arxiv_id)
                entry["image"] = thumbnail_path
                log(f"Added arXiv thumbnail (fallback): {thumbnail_path}", indent=2, level="SUCCESS")
                return [entry]
            except Exception as e:
                log(f"Could not generate arXiv thumbnail: {e}", indent=2, level="WARNING")

    # PRIORITY 2: Handle arXiv-only papers (no DOI)
    elif citation_id.startswith("arxiv:"):
        try:
            # Extract arXiv ID (remove "arxiv:" prefix)
            arxiv_id = citation_id[6:]
            log(f"Fetching arXiv thumbnail for {arxiv_id}", indent=2)
            thumbnail_path = generate_arxiv_thumbnail(arxiv_id)
            entry["image"] = thumbnail_path
            log(f"Added arXiv thumbnail: {thumbnail_path}", indent=2, level="SUCCESS")
        except Exception as e:
            log(f"Could not generate arXiv thumbnail: {e}", indent=2, level="WARNING")

    # Return entry (with or without image)
    return [entry]
