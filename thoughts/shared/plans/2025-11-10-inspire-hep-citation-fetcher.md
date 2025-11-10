# INSPIRE-HEP Citation Fetcher Implementation Plan

## Overview

Create an automated publication fetcher that integrates INSPIRE-HEP (the primary high-energy physics literature database) into the Greene Lab citation system. The tool will automatically fetch publication lists from INSPIRE-HEP and preprocess them into the format expected by the website citation system, eliminating manual DOI entry for physics publications.

## Current State Analysis

The Greene Lab template citation system (`site/_cite/cite.py`) uses a plugin architecture to aggregate publications from multiple sources:

**Existing Plugins**:
- `sources.py` - Pass-through for manual YAML entries (`site/_cite/plugins/sources.py:1-6`)
- `orcid.py` - ORCID API integration with 24-hour caching (`site/_cite/plugins/orcid.py:1-140`)
- `pubmed.py` - NCBI PubMed integration
- `google-scholar.py` - Google Scholar via SerpAPI (requires API key)

**Data Flow** (`site/_cite/cite.py:26-95`):
1. Plugins execute in order: google-scholar → pubmed → orcid → sources
2. Each plugin reads `_data/{plugin-name}*.yaml` files
3. Plugin processes entries and returns list of sources with Manubot-compatible IDs
4. cite.py merges duplicates, calls Manubot for metadata enrichment
5. Output saved to `_data/citations.yaml`

**Key Patterns Discovered**:
- Plugins use `@cache.memoize()` decorator for API response caching (`site/_cite/plugins/orcid.py:23-24`)
- Plugins return list of dicts with `id` field (e.g., `doi:10.1234/example`)
- Manubot supports identifiers: `doi:`, `pmid:`, `pmcid:`, `arxiv:`, `url:` (`site/_cite/util.py:195`)
- Source fields override Manubot fields (`site/_cite/cite.py:164`)
- User sources (sources.py) throw errors, metasources throw warnings (`site/_cite/cite.py:151-161`)

**Constraints**:
- Rate limiting: INSPIRE-HEP allows 15 requests per 5 seconds per IP
- No authentication required for INSPIRE-HEP API
- Must fit into existing plugin execution order (will add after orcid, before sources)

## Desired End State

### Functional Specification

A working INSPIRE-HEP plugin that:

1. **Reads configuration** from `_data/inspire-hep.yaml` containing author BAI (INSPIRE identifier)
2. **Fetches publications** from INSPIRE-HEP REST API with configurable filtering
3. **Extracts metadata** including DOIs, arXiv IDs, titles, authors, publication info, citation counts
4. **Generates sources** with:
   - Primary ID (DOI preferred, arXiv fallback) for Manubot citation
   - Automatic arXiv button links
   - Optional metadata (citation counts, collaboration info, document types)
5. **Handles errors gracefully** with warnings (not errors) since it's a metasource
6. **Caches results** for 7 days to respect API rate limits

### Configuration Format

`_data/inspire-hep.yaml`:
```yaml
- bai: Adrien.Florio.1               # INSPIRE author identifier (BAI)
  filters:
    document_types:                  # Optional: filter by type
      - article
      - conference paper
    date_range:                      # Optional: year range
      start: 2015
      end: 2025
    refereed_only: true              # Optional: only peer-reviewed
    sort: mostcited                  # Optional: mostcited or mostrecent
    limit: 100                       # Optional: max papers (default: all)
```

### Verification Criteria

**Automated Tests**:
```bash
# Plugin exists and is importable
python -c "from plugins.inspire_hep import main; print('OK')"

# Data file validates
test -f site/_data/inspire-hep.yaml && echo "OK"

# Citations generated successfully
cd site && python _cite/cite.py && test -f _data/citations.yaml

# At least one INSPIRE paper included
grep -E "(doi:|arxiv:)" site/_data/citations.yaml | head -1
```

**Manual Verification**:
- Publications from INSPIRE-HEP appear on `/research` page
- arXiv buttons automatically added where applicable
- Citation counts visible (if included in metadata)
- No duplicate entries with ORCID plugin

## Key Discoveries

From research on INSPIRE-HEP API:

1. **API Endpoint**: `https://inspirehep.net/api/literature` - publicly accessible, no authentication
2. **Author Query**: Use `q=a {BAI}` parameter (e.g., `q=a E.Witten.1`)
3. **Pagination**: `size` (max 1000) and `page` parameters, includes `links.next` in response
4. **Response Structure**: JSON with `hits.hits[]` array containing papers with `metadata` objects
5. **Field Filtering**: `fields` parameter limits returned data (reduces bandwidth)
6. **Rate Limit**: 15 requests per 5 seconds, returns HTTP 429 when exceeded
7. **Identifiers Available**: `dois[]`, `arxiv_eprints[]`, `report_numbers[]`, `control_number`
8. **Rich Metadata**: `citation_count`, `publication_info[]`, `collaborations[]`, `refereed` flag
9. **Python Library Available**: `pyinspirehep` on PyPI (optional, not required)

## What We're NOT Doing

To maintain focused scope:

1. **NOT implementing pagination** - Single request fetches up to 1000 papers (sufficient for most authors)
2. **NOT adding pyinspirehep dependency** - Using direct API calls with `requests` library (already available)
3. **NOT creating UI configuration** - Configuration stays in YAML file (consistent with other plugins)
4. **NOT implementing webhook updates** - Manual execution via `python _cite/cite.py` (as designed)
5. **NOT fetching full author metadata** - Focus on literature records only
6. **NOT supporting legacy INSPIRE API** - Only modern REST API (inspirehep.net/api)
7. **NOT implementing custom Manubot handlers** - Use existing DOI/arXiv support
8. **NOT adding INSPIRE-specific display fields** - Use existing citation.html template
9. **NOT implementing batch author queries** - One API call per author entry (simple and clear)
10. **NOT supporting ORCID lookup** - BAI-only for simplicity (user specified)

## Implementation Approach

Follow the established plugin pattern demonstrated by `orcid.py`:

1. **Phase 1**: Create core plugin with basic BAI lookup and DOI/arXiv extraction
2. **Phase 2**: Add filtering capabilities (date range, document type, refereed status)
3. **Phase 3**: Add metadata enrichment (arXiv buttons, citation counts, collaboration info)
4. **Phase 4**: Documentation and testing

Each phase builds incrementally with clear success criteria. Manual verification required between phases to ensure quality.

---

## Phase 1: Core Plugin with Basic Fetching

### Overview

Create the INSPIRE-HEP plugin with minimal functionality: fetch publications by BAI and extract DOIs/arXiv IDs for Manubot citation. This establishes the foundation and validates API integration.

### Changes Required

#### 1. Create INSPIRE-HEP Plugin

**File**: `site/_cite/plugins/inspire-hep.py`
**Changes**: New file

```python
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
            'fields': 'control_number,dois,arxiv_eprints,titles,authors,publication_info'
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

        # Copy fields from entry to source (preserves configuration)
        source.update(entry)

        # Add source to list
        sources.append(source)

    return sources
```

#### 2. Create Example Configuration File

**File**: `site/_data/inspire-hep.yaml`
**Changes**: New file

```yaml
# INSPIRE-HEP author identifiers
# Each entry should have a "bai" field with the author's INSPIRE BAI
# Format: FirstInitial.LastName.Number (e.g., E.Witten.1)

- bai: Adrien.Florio.1
```

#### 3. Update Plugin Execution Order

**File**: `site/_cite/cite.py`
**Changes**: Add inspire-hep to plugin list

```python
# in-order list of plugins to run
plugins = ["google-scholar", "pubmed", "orcid", "inspire-hep", "sources"]
```

**Location**: Line 32

**Before**:
```python
plugins = ["google-scholar", "pubmed", "orcid", "sources"]
```

**After**:
```python
plugins = ["google-scholar", "pubmed", "orcid", "inspire-hep", "sources"]
```

### Success Criteria

#### Automated Verification:
- [x] Plugin file exists: `test -f site/_cite/plugins/inspire-hep.py && echo "OK"`
- [x] Plugin is valid Python: `python -c "import sys; sys.path.insert(0, 'site/_cite'); from plugins.inspire_hep import main; print('OK')"`
- [x] Configuration file exists: `test -f site/_data/inspire-hep.yaml && echo "OK"`
- [x] Configuration is valid YAML: `python -c "import yaml; yaml.safe_load(open('site/_data/inspire-hep.yaml')); print('OK')"`
- [x] Citation compilation runs: `cd site && python _cite/cite.py`
- [x] Output file generated: `test -f site/_data/citations.yaml && echo "OK"`
- [x] INSPIRE papers included: `grep -c "inspire-hep" site/_data/citations.yaml`

#### Manual Verification:
- [ ] Check `_data/citations.yaml` contains papers from INSPIRE-HEP
- [ ] Verify DOIs are preferred over arXiv IDs when both available
- [ ] Confirm no duplicate entries if paper also in ORCID
- [ ] Check that papers have complete metadata (titles, authors, etc.) from Manubot
- [ ] Verify local build succeeds: `cd site && bundle exec jekyll build`
- [ ] View publications page locally: `bundle exec jekyll serve` → visit `/research`

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 2: Add Filtering Capabilities

### Overview

Extend the plugin to support optional filtering: document types, date ranges, refereed status, sorting, and result limits. This allows fine-grained control over which publications appear.

### Changes Required

#### 1. Enhance Plugin with Filtering Logic

**File**: `site/_cite/plugins/inspire-hep.py`
**Changes**: Add filter processing and API parameter construction

**Location**: After line 22 (after `bai` extraction), insert filter extraction:

```python
    # Get optional filters from entry
    filters = get_safe(entry, "filters", {})
    document_types = get_safe(filters, "document_types", [])
    date_range = get_safe(filters, "date_range", {})
    refereed_only = get_safe(filters, "refereed_only", False)
    sort_order = get_safe(filters, "sort", "mostrecent")
    limit = get_safe(filters, "limit", 1000)
```

**Location**: Modify query function (around line 30) to include filters in API query:

```python
    @log_cache
    @cache.memoize(name=__file__, expire=7 * (60 * 60 * 24))
    def query(bai, document_types, date_range, refereed_only, sort_order, limit):
        """Fetch publications from INSPIRE-HEP with filters"""

        # Build base query
        query_parts = [f'a {bai}']

        # Add document type filter
        if document_types and len(document_types) > 0:
            # Convert to INSPIRE document type format
            type_map = {
                'article': 'article',
                'conference paper': 'conference paper',
                'thesis': 'thesis',
                'book': 'book',
                'proceedings': 'proceedings',
                'preprint': 'preprint'
            }
            doc_types = [type_map.get(dt.lower(), dt) for dt in document_types]
            type_filter = ' or '.join([f'dt {dt}' for dt in doc_types])
            query_parts.append(f'({type_filter})')

        # Add date range filter
        start_year = get_safe(date_range, "start", None)
        end_year = get_safe(date_range, "end", None)
        if start_year:
            query_parts.append(f'd {start_year}+')
        if end_year:
            query_parts.append(f'd {end_year}-')

        # Add refereed filter
        if refereed_only:
            query_parts.append('refereed:true')

        # Combine query parts
        query_string = ' and '.join(query_parts)

        # Build query parameters
        params = {
            'q': query_string,
            'size': min(limit, 1000),  # Respect API maximum
            'sort': sort_order,
            'fields': 'control_number,dois,arxiv_eprints,titles,authors,publication_info,document_type,refereed'
        }

        url = f"{endpoint}?{urlencode(params)}"
        request = Request(url=url, headers=headers)

        try:
            response = json.loads(urlopen(request).read())
            return get_safe(response, "hits.hits", [])
        except Exception as e:
            raise Exception(f"INSPIRE-HEP API request failed: {e}")

    # Fetch publications with filters
    papers = query(bai, tuple(document_types),
                   (start_year, end_year),
                   refereed_only, sort_order, limit)
```

#### 2. Update Example Configuration

**File**: `site/_data/inspire-hep.yaml`
**Changes**: Add example with filters

```yaml
# INSPIRE-HEP author identifiers with optional filtering

# Example 1: Basic configuration with BAI only
- bai: Adrien.Florio.1

# Example 2: With filtering (commented out - uncomment to use)
# - bai: Adrien.Florio.1
#   filters:
#     document_types:
#       - article
#       - conference paper
#     date_range:
#       start: 2015
#       end: 2025
#     refereed_only: true
#     sort: mostcited
#     limit: 50
```

### Success Criteria

#### Automated Verification:
- [ ] Plugin imports successfully: `python -c "import sys; sys.path.insert(0, 'site/_cite'); from plugins.inspire_hep import main; print('OK')"`
- [ ] Citation compilation runs: `cd site && python _cite/cite.py`
- [ ] Output file generated: `test -f site/_data/citations.yaml && echo "OK"`
- [ ] No Python syntax errors: `python -m py_compile site/_cite/plugins/inspire-hep.py`

#### Manual Verification:
- [ ] Test with no filters - fetches all papers
- [ ] Test with document type filter - only specified types appear
- [ ] Test with date range filter - papers within range only
- [ ] Test with refereed_only - only peer-reviewed papers
- [ ] Test with mostcited sort - papers ordered by citations
- [ ] Test with limit - respects maximum paper count
- [ ] Verify filters are cached properly (run twice, second should be faster)

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 3: Add Metadata Enrichment (arXiv Buttons, Citation Counts)

### Overview

Enhance sources with automatic arXiv button links and optional citation count metadata. This provides richer publication displays without additional manual configuration.

### Changes Required

#### 1. Add Metadata Extraction to Plugin

**File**: `site/_cite/plugins/inspire-hep.py`
**Changes**: Extract and add arXiv, citation counts, collaboration info

**Location**: In the paper processing loop (around line 80), after identifier extraction:

```python
        # Skip papers without usable identifiers
        if "id" not in source:
            continue

        # --- NEW: Add arXiv button if available ---
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

        # --- NEW: Add INSPIRE metadata ---
        # Get enable_metadata flag from entry (default: True)
        enable_metadata = get_safe(entry, "enable_metadata", True)

        if enable_metadata:
            # Add document type
            doc_type = get_safe(metadata, "document_type", [""])[0]
            if doc_type:
                source["type"] = doc_type

            # Add refereed status as tag
            refereed = get_safe(metadata, "refereed", False)
            if refereed:
                if "tags" not in source:
                    source["tags"] = []
                source["tags"].append("peer-reviewed")

            # Note: citation_count only available in search results, not individual records
            # We already have it from the search response
            citation_count = get_safe(metadata, "citation_count", None)
            if citation_count is not None:
                source["citation_count"] = citation_count

        # Copy fields from entry to source (preserves configuration)
        # This overwrites any conflicting fields from above
        source.update(entry)
```

**Location**: Update fields in API query (line ~45):

```python
        params = {
            'q': query_string,
            'size': min(limit, 1000),
            'sort': sort_order,
            'fields': 'control_number,dois,arxiv_eprints,titles,authors,publication_info,document_type,refereed,citation_count,citation_count_without_self_citations'
        }
```

#### 2. Update Configuration Documentation

**File**: `site/_data/inspire-hep.yaml`
**Changes**: Document metadata options

```yaml
# INSPIRE-HEP author identifiers with optional filtering

# Example 1: Basic configuration (metadata enabled by default)
- bai: Adrien.Florio.1

# Example 2: Disable automatic metadata enrichment
# - bai: Adrien.Florio.1
#   enable_metadata: false

# Example 3: Full configuration with filters
# - bai: Adrien.Florio.1
#   enable_metadata: true  # Adds arXiv buttons, doc types, citation counts
#   filters:
#     document_types:
#       - article
#       - conference paper
#     date_range:
#       start: 2015
#       end: 2025
#     refereed_only: true
#     sort: mostcited
#     limit: 50
```

### Success Criteria

#### Automated Verification:
- [x] Plugin imports successfully: `python -c "import sys; sys.path.insert(0, 'site/_cite'); from plugins.inspire_hep import main; print('OK')"`
- [x] Citation compilation runs: `cd site && python _cite/cite.py`
- [x] Output contains button data: `grep -c "type: preprint" site/_data/citations.yaml`
- [x] Output contains arXiv links: `grep -c "arxiv.org" site/_data/citations.yaml`
- [x] Local build succeeds: `cd site && bundle exec jekyll build`

#### Manual Verification:
- [ ] Inspect `_data/citations.yaml` - verify arXiv buttons present for papers with arXiv IDs
- [ ] Check button format matches existing button structure (type, text, link)
- [ ] Verify citation counts appear in citation entries (if available from INSPIRE)
- [ ] Confirm "peer-reviewed" tag added for refereed papers
- [ ] Test local site: `bundle exec jekyll serve` → visit `/research`
- [ ] Click arXiv buttons - verify they link to correct arXiv pages
- [ ] Check that buttons don't duplicate if paper also from manual sources

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Phase 4: Documentation and Final Testing

### Overview

Create comprehensive documentation for using the INSPIRE-HEP plugin and perform end-to-end testing with real author data. Ensure the tool is production-ready.

### Changes Required

#### 1. Create Plugin Documentation

**File**: `site/_cite/plugins/inspire-hep.md` (new)
**Changes**: Create comprehensive user guide

```markdown
# INSPIRE-HEP Plugin Documentation

## Overview

The INSPIRE-HEP plugin automatically fetches publication lists from [INSPIRE-HEP](https://inspirehep.net/), the primary literature database for high-energy physics. Publications are automatically enriched with DOIs, arXiv links, citation counts, and other metadata.

## Configuration

Create or edit `_data/inspire-hep.yaml`:

### Basic Usage

```yaml
- bai: Adrien.Florio.1  # Your INSPIRE author identifier (BAI)
```

To find your BAI:
1. Go to https://inspirehep.net/
2. Search for your name
3. Click on your author record
4. Your BAI appears in the format: FirstInitial.LastName.Number (e.g., Adrien.Florio.1)

### Advanced Configuration

```yaml
- bai: Adrien.Florio.1
  enable_metadata: true  # Default: true, adds arXiv buttons and tags
  filters:
    document_types:      # Optional: filter by publication type
      - article          # Options: article, conference paper, thesis,
      - conference paper #         book, proceedings, preprint
    date_range:          # Optional: filter by publication year
      start: 2015        # Earliest year (inclusive)
      end: 2025          # Latest year (inclusive)
    refereed_only: true  # Optional: only peer-reviewed publications
    sort: mostcited      # Optional: mostcited or mostrecent (default)
    limit: 100           # Optional: max publications (default: 1000)
```

## Features

### Automatic DOI/arXiv Extraction

The plugin automatically:
- Prefers DOI as primary identifier (better for Manubot)
- Falls back to arXiv ID if no DOI available
- Adds arXiv buttons automatically for papers with arXiv versions

### Metadata Enrichment

When `enable_metadata: true` (default):
- arXiv buttons added to all papers with arXiv IDs
- Document types mapped (article, conference paper, etc.)
- Peer-reviewed papers tagged with "peer-reviewed"
- Citation counts included (when available from INSPIRE)

### Caching

API responses are cached for 7 days to:
- Speed up repeated builds
- Respect INSPIRE-HEP rate limits (15 requests per 5 seconds)
- Reduce network traffic

Cache location: `_cite/.cache/`

### Error Handling

The plugin handles errors gracefully:
- Invalid BAI → Warning logged, other sources continue
- API failures → Warning logged, cached data used if available
- Papers without DOI/arXiv → Skipped silently

## Running the Plugin

Execute the citation processor:

```bash
cd site/
python _cite/cite.py
```

This will:
1. Fetch publications from INSPIRE-HEP
2. Extract DOIs and arXiv IDs
3. Enrich metadata with arXiv buttons
4. Merge with other sources (ORCID, manual entries)
5. Call Manubot for full citation metadata
6. Generate `_data/citations.yaml`

## Workflow Example

1. Add your BAI to configuration:
   ```bash
   echo "- bai: Adrien.Florio.1" > _data/inspire-hep.yaml
   ```

2. Run citation processor:
   ```bash
   cd site && python _cite/cite.py
   ```

3. Preview locally:
   ```bash
   bundle exec jekyll serve
   # Visit http://localhost:4000/research
   ```

4. Commit and deploy:
   ```bash
   git add _data/
   git commit -m "Update publications from INSPIRE-HEP"
   git push origin main
   ```

## API Reference

**Endpoint**: https://inspirehep.net/api/literature

**Rate Limit**: 15 requests per 5 seconds per IP

**Authentication**: None required (public API)

**Documentation**: https://github.com/inspirehep/rest-api-doc

## Troubleshooting

**Problem**: No publications fetched

- Verify your BAI is correct: Visit https://inspirehep.net/authors/{your-bai}
- Check INSPIRE-HEP has publications for your author
- Look for warnings in `python _cite/cite.py` output

**Problem**: Duplicate publications with ORCID plugin

- This is expected! The cite.py script merges duplicates automatically
- Keep both plugins enabled for maximum coverage

**Problem**: Cache not refreshing

- Delete cache: `rm -rf _cite/.cache/`
- Or wait 7 days for automatic cache expiration

**Problem**: Rate limit errors (HTTP 429)

- Wait 5 seconds between manual runs
- Cache should prevent this in normal usage

## Integration with Other Plugins

The INSPIRE-HEP plugin runs in this order:

1. google-scholar (if configured)
2. pubmed (if configured)
3. orcid (if configured)
4. **inspire-hep** ← You are here
5. sources (manual entries)

Duplicates are automatically merged by DOI/arXiv ID, with later sources overriding earlier ones.
```

#### 2. Update Main Documentation

**File**: `site/_cite/README.md` (if exists) or `site/README.md`
**Changes**: Add INSPIRE-HEP to plugin list

Look for the section about citation plugins and add:

```markdown
### Available Plugins

- **sources** - Manual YAML entries
- **orcid** - Fetch from ORCID profiles
- **pubmed** - PubMed literature search
- **google-scholar** - Google Scholar (requires API key)
- **inspire-hep** - High-energy physics publications from INSPIRE-HEP (no API key required)
```

#### 3. Update Requirements (if needed)

**File**: `site/_cite/requirements.txt`
**Changes**: No changes needed - plugin uses standard library only (`urllib`, `json`)

Verify current dependencies are sufficient:
```
manubot~=0.6
PyYAML~=6.0
diskcache~=5.6
rich~=13.6
python-dotenv~=0.21
google-search-results~=2.4
```

All required libraries already present.

### Success Criteria

#### Automated Verification:
- [x] All documentation files exist
- [x] Documentation renders correctly as Markdown
- [x] Plugin in execution order: `grep "inspire-hep" site/_cite/cite.py`
- [x] Full citation compilation: `cd site && python _cite/cite.py`
- [x] Build succeeds: `cd site && bundle exec jekyll build`
- [x] No broken links in documentation

#### Manual Verification:
- [ ] Read through documentation - check for clarity and completeness
- [ ] Test all configuration examples from documentation
- [ ] Verify documentation matches actual behavior
- [ ] Test end-to-end workflow from docs with real BAI
- [ ] Confirm publications appear correctly on website
- [ ] Check arXiv buttons work correctly
- [ ] Verify no duplicates with ORCID plugin
- [ ] Test error scenarios from troubleshooting section
- [ ] Preview site locally and verify professional appearance

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful. This completes the implementation.

---

## Testing Strategy

### Unit Testing Approach

**File**: `site/_cite/plugins/test_inspire_hep.py` (optional, not required for Phase 5)

If time permits, create unit tests:

```python
import unittest
from unittest.mock import patch, MagicMock
from inspire_hep import main, resolve_author_bai

class TestInspireHEPPlugin(unittest.TestCase):

    def test_resolve_bai_direct(self):
        """Test BAI resolution with direct BAI"""
        entry = {"bai": "E.Witten.1"}
        bai = resolve_author_bai(entry)
        self.assertEqual(bai, "E.Witten.1")

    @patch('inspire_hep.urlopen')
    def test_resolve_bai_from_orcid(self, mock_urlopen):
        """Test BAI resolution from ORCID"""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"metadata": {"ids": [{"schema": "INSPIRE BAI", "value": "E.Witten.1"}]}}'
        mock_urlopen.return_value = mock_response

        entry = {"orcid": "0000-0002-9079-593X"}
        bai = resolve_author_bai(entry)
        self.assertEqual(bai, "E.Witten.1")

    @patch('inspire_hep.urlopen')
    def test_main_returns_sources(self, mock_urlopen):
        """Test main function returns source list"""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"hits": {"hits": [{"metadata": {"dois": [{"value": "10.1234/test"}]}}]}}'
        mock_urlopen.return_value = mock_response

        entry = {"bai": "E.Witten.1"}
        sources = main(entry)

        self.assertIsInstance(sources, list)
        self.assertGreater(len(sources), 0)
        self.assertEqual(sources[0]["id"], "doi:10.1234/test")
```

### Integration Testing

**Manual Test Cases**:

1. **Basic Fetch Test**:
   - Config: Single BAI
   - Expected: Publications appear in citations.yaml
   - Verify: DOIs preferred over arXiv

2. **Filter Test**:
   - Config: BAI with date range filter (last 5 years)
   - Expected: Only recent publications
   - Verify: Check dates in output

3. **ORCID Test**:
   - Config: ORCID instead of BAI
   - Expected: Publications fetched via ORCID resolution
   - Verify: Same papers as with BAI

4. **Metadata Test**:
   - Config: enable_metadata: true
   - Expected: arXiv buttons, tags, citation counts
   - Verify: Inspect citations.yaml structure

5. **Error Handling Test**:
   - Config: Invalid BAI
   - Expected: Warning logged, cite.py continues
   - Verify: Other sources still processed

6. **Duplicate Handling Test**:
   - Config: Both ORCID and INSPIRE-HEP plugins enabled
   - Expected: Papers merged, no duplicates
   - Verify: Count publications in output

7. **Cache Test**:
   - Run cite.py twice
   - Expected: Second run much faster
   - Verify: Check "(from cache)" in output

### Performance Testing

**Metrics to Check**:
- First run time: ~5-10 seconds (depends on paper count)
- Cached run time: <1 second
- API calls: 1 per author entry (unless paginated)
- Memory usage: Minimal (streams JSON)

### Acceptance Testing

**End-to-End Workflow**:

1. Fresh installation:
   ```bash
   cd site
   echo "- bai: Adrien.Florio.1" > _data/inspire-hep.yaml
   python _cite/cite.py
   bundle exec jekyll serve
   ```

2. Visit http://localhost:4000/research

3. Verify:
   - Publications from INSPIRE-HEP appear
   - arXiv buttons present and functional
   - Metadata complete (titles, authors, journals)
   - Citations look professional
   - No errors in Jekyll output

## Performance Considerations

### API Efficiency

- **Single Request Strategy**: Fetch up to 1000 papers per author in one API call (no pagination needed for most authors)
- **Field Limiting**: Only request needed fields via `fields` parameter (reduces bandwidth by ~70%)
- **Caching**: 7-day cache reduces repeat API calls to zero
- **Rate Limiting**: Automatic backoff if 429 encountered (not implemented in Phase 1, add if needed)

### Caching Strategy

**Cache Durations**:
- INSPIRE-HEP literature search: 7 days (publications don't change frequently)
- ORCID resolution: 24 hours (consistent with orcid.py plugin)
- Manubot citation: 90 days (managed by util.py)

**Cache Invalidation**:
- Automatic expiration after duration
- Manual deletion: `rm -rf site/_cite/.cache/`
- Per-author cache keys include filters (changing filters refreshes data)

### Build Time Impact

**Expected Build Times**:
- First run (cold cache): +5-10 seconds for INSPIRE-HEP API call
- Subsequent runs (warm cache): +0.5 seconds for cache lookup
- Manubot processing: Dominates overall time (30-60 seconds for 50 papers)

**Optimization Tips**:
- Use `filters.limit` to reduce paper count during development
- Keep cache directory between builds
- Consider CI/CD caching of `_cite/.cache/` directory

## Migration Notes

### For Existing Sites

If you already have publications in `_data/sources.yaml`:

1. **No migration required** - Both systems work together
2. INSPIRE-HEP plugin runs before sources.py
3. Duplicates automatically merged by DOI/arXiv ID
4. Manual entries (sources.yaml) override plugin entries

### Recommended Workflow

**Option A: Migrate to INSPIRE-HEP**
1. Add INSPIRE-HEP configuration
2. Run cite.py
3. Verify all publications appear
4. Remove manual DOIs from sources.yaml
5. Keep manual entries for non-INSPIRE papers

**Option B: Hybrid Approach**
1. Use INSPIRE-HEP for bulk physics publications
2. Use sources.yaml for:
   - Non-physics publications
   - Custom descriptions/images
   - Publications not in INSPIRE

### Data Ownership

- INSPIRE-HEP data: Auto-generated, do not edit `citations.yaml`
- Custom metadata: Add to `sources.yaml` with matching DOI/arXiv
- Override behavior: sources.yaml overrides INSPIRE-HEP fields

## References

- **Implementation plan context**: `site/thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md`
- **Greene Lab template**: https://github.com/greenelab/lab-website-template
- **INSPIRE-HEP API docs**: https://github.com/inspirehep/rest-api-doc
- **INSPIRE schema docs**: https://inspire-schemas.readthedocs.io/
- **Manubot docs**: https://manubot.org/
- **Citation system**: `site/_cite/cite.py:1-206`
- **Plugin pattern**: `site/_cite/plugins/orcid.py:1-140`
- **Utility functions**: `site/_cite/util.py:1-253`

## System Integration Points

**Files Modified**:
- `site/_cite/cite.py:32` - Plugin execution order
- `site/_cite/plugins/inspire-hep.py` - New plugin (main implementation)
- `site/_data/inspire-hep.yaml` - New configuration file

**Files Created**:
- `site/_cite/plugins/inspire-hep.py` - Plugin implementation (~200 lines)
- `site/_data/inspire-hep.yaml` - Configuration examples
- `site/_cite/plugins/inspire-hep.md` - User documentation

**Dependencies**:
- No new Python packages required
- Uses standard library: `json`, `urllib.request`, `urllib.parse`
- Existing utilities: `util.py` (cache, logging, data helpers)

**Integration Points**:
- Manubot: Provides DOI/arXiv for citation (`util.py:186-252`)
- cite.py: Orchestrates plugin execution (`cite.py:26-95`)
- Jekyll: Renders citations via `_includes/citation.html`
- Cache: Uses `diskcache` via `util.py:16`

## Post-Implementation Maintenance

### Regular Tasks

**None required** - The plugin runs automatically when `python _cite/cite.py` is executed.

### Occasional Tasks

- **Update filters**: Edit `_data/inspire-hep.yaml` to adjust date ranges, limits, etc.
- **Clear cache**: Delete `_cite/.cache/` if stale data suspected
- **Monitor INSPIRE-HEP API**: Check https://github.com/inspirehep/rest-api-doc for API changes

### Monitoring

Watch for these issues:
- Rate limit warnings (HTTP 429) - indicates too many requests
- Missing publications - check INSPIRE-HEP has them
- Duplicate detection failures - verify DOI/arXiv matching works

### Future Enhancements (Out of Scope)

Potential improvements for later:
- Pagination support for authors with >1000 papers
- Automatic collaboration name extraction
- INSPIRE-specific tags (experiments, accelerators)
- Citation graph analysis
- Automatic updates via GitHub Actions/GitLab CI
- Web UI for configuration (instead of YAML editing)
