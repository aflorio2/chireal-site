"""
Plugin to fetch publications from INSPIRE-HEP literature database
"""

import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from util import *


def main(entry):
    """
    Receives single list entry from inspire-hep data file
    Returns list of sources to cite
    """

    # INSPIRE-HEP API endpoint
    endpoint = "https://inspirehep.net/api/literature"
    headers = {"Accept": "application/json"}

    # Get author identifier from entry
    bai = get_safe(entry, "bai", "")

    if not bai:
        raise Exception('No "bai" key in inspire-hep.yaml entry')

    # Query API with caching (7 days)
    @log_cache
    @cache.memoize(name=__file__, expire=7 * (60 * 60 * 24))
    def query(bai):
        """Fetch publications from INSPIRE-HEP"""
        # Build query parameters
        params = {
            'q': f'a {bai}',
            'size': 1000,  # Maximum allowed by API
            'sort': 'mostrecent',
            'fields': 'control_number,dois,arxiv_eprints,titles,authors,publication_info,document_type,inspire_categories'
        }

        url = f"{endpoint}?{urlencode(params)}"
        request = Request(url=url, headers=headers)

        try:
            response = json.loads(urlopen(request).read())
            return get_safe(response, "hits.hits", [])
        except Exception as e:
            raise Exception(f"INSPIRE-HEP API request failed: {e}")

    # Fetch publications
    papers = query(bai)

    # List of sources to return
    sources = []

    # Process each paper
    for paper in papers:
        metadata = get_safe(paper, "metadata", {})

        # Filter: Skip conference papers/proceedings
        document_types = get_safe(metadata, "document_type", [])
        if "conference paper" in document_types or "proceedings" in document_types:
            continue

        # Filter: Skip papers with more than 20 authors
        authors = get_safe(metadata, "authors", [])
        if len(authors) > 20:
            continue

        # Create source dict
        source = {}

        # Extract identifiers (prefer DOI over arXiv)
        dois = get_safe(metadata, "dois", [])
        arxiv_eprints = get_safe(metadata, "arxiv_eprints", [])

        # Prefer DOI as primary identifier
        if dois and len(dois) > 0:
            doi_value = get_safe(dois, "0.value", "")
            if doi_value:
                source["id"] = f"doi:{doi_value}"
        # Fallback to arXiv if no DOI
        elif arxiv_eprints and len(arxiv_eprints) > 0:
            arxiv_value = get_safe(arxiv_eprints, "0.value", "")
            if arxiv_value:
                source["id"] = f"arxiv:{arxiv_value}"

        # Skip papers without usable identifiers
        if "id" not in source:
            continue

        # --- Metadata Enrichment ---
        # Get enable_metadata flag from entry (default: True)
        enable_metadata = get_safe(entry, "enable_metadata", True)

        if enable_metadata:
            # Add arXiv button if available
            if arxiv_eprints and len(arxiv_eprints) > 0:
                arxiv_value = get_safe(arxiv_eprints, "0.value", "")
                if arxiv_value:
                    # Add arXiv button (will be displayed on publications page)
                    if "buttons" not in source:
                        source["buttons"] = []
                    source["buttons"].append({
                        "type": "preprint",
                        "text": "arXiv",
                        "link": f"https://arxiv.org/abs/{arxiv_value}"
                    })

            # Add document type
            doc_type = get_safe(metadata, "document_type", [])
            if doc_type and len(doc_type) > 0:
                source["type"] = doc_type[0]

            # Add INSPIRE categories as tags
            inspire_categories = get_safe(metadata, "inspire_categories", [])
            if inspire_categories:
                if "tags" not in source:
                    source["tags"] = []
                # Extract category terms and add as tags
                for category in inspire_categories:
                    term = get_safe(category, "term", "")
                    if term:
                        source["tags"].append(term)

        # Copy fields from entry to source (preserves configuration)
        source.update(entry)

        # Add source to list
        sources.append(source)

    return sources
