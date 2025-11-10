# Research: Automatic Image Fetching for Publications on Research Page

**Date**: 2025-11-10 14:30:37 CET
**Researcher**: Adrien Florio
**Git Commit**: N/A (not a git repository)
**Branch**: N/A
**Repository**: GroupWebsite

## Research Question

How does the website currently handle images for publications on the research page, and what mechanisms exist for automatically fetching publication images?

## Summary

The Greene Lab website template includes built-in support for displaying publication images, but **no automatic image fetching is currently implemented**. Images must be manually specified in publication data via the `image` field. The citation display system (`_includes/citation.html:13-27`) renders images when `style="rich"` is used and an `image` field is present, but neither the existing plugins (ORCID, PubMed, Google Scholar) nor the newly implemented INSPIRE-HEP plugin fetch publication images automatically.

**Key Finding**: Publication images are currently a **manual-only feature** requiring explicit image URLs in source data files.

## Current State: Image Support in Citation System

### Image Display Implementation

The citation template supports images with these characteristics:

**File**: `_includes/citation.html:13-27`

**Display Logic**:
- Images only render when `style="rich"` parameter is used
- Requires `citation.image` field to be populated
- Image wrapped in anchor tag linking to publication
- Lazy loading enabled (`loading="lazy"`)
- Fallback handler included (`{% include fallback.html %}`)

**Code Structure**:
```liquid
{% if include.style == "rich" %}
  <a href="{{ citation.link | relative_url | uri_escape }}" class="citation-image">
    <img
      src="{{ citation.image | relative_url | uri_escape }}"
      alt="{{ citation.title | default: "citation image" | regex_strip }}"
      loading="lazy"
      {% include fallback.html %}
    >
  </a>
{% endif %}
```

**Styling**: `_styles/citation.scss` provides CSS for image layout and responsive behavior

### Research Page Configuration

**File**: `research/index.md:14-34`

The research page uses two citation display modes:

1. **Highlighted Publications** (Lines 16-24):
   ```markdown
   {% include citation.html lookup="Thermalization from quantum entanglement" style="rich" %}
   ```
   - Uses `style="rich"` to enable image display
   - 5 manually curated publications shown

2. **All Publications List** (Line 34):
   ```markdown
   {% include list.html data="citations" component="citation" style="rich" %}
   ```
   - Displays all publications from `_data/citations.yaml`
   - `style="rich"` parameter enables images for entire list

**Current Status**: All citations configured to display images when available, but none have image data.

## Data Structure for Publication Images

### Input Format: sources.yaml

**File**: `_data/sources.yaml:1-10`

Manual publication entries can include image field:

```yaml
- id: doi:10.1234/example
  image: https://example.com/image.jpg  # Image URL
  # or
  image: images/publication-thumb.jpg   # Relative path to local image
```

**Documentation Reference**: `/thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md:116-139`

**Field Specifications**:
- `image`: Optional field (string)
- Supports absolute URLs (https://...) or relative paths (images/...)
- Recommended width: 180px (per documentation)
- No validation or automatic fetching

### Output Format: citations.yaml

**File**: `_data/citations.yaml:1-50`

**Current State**: 30+ publications, **zero have image fields**

Example entry structure:
```yaml
- id: arxiv:2511.01966
  title: 'Entanglement asymmetry in gauge theories...'
  authors:
  - Adrien Florio
  - Sara Murciano
  publisher: arXiv
  date: '2025-11-05'
  link: https://arxiv.org/abs/2511.01966
  buttons:
  - type: preprint
    text: arXiv
    link: https://arxiv.org/abs/2511.01966
  type: article
  tags:
  - Theory-HEP
  - Condensed Matter
  # NO IMAGE FIELD - this is the current state for all publications
```

## Plugin Analysis: Image Fetching Capabilities

### INSPIRE-HEP Plugin (Recently Implemented)

**File**: `_cite/plugins/inspire-hep.py:1-132`

**Functionality**:
- Fetches publications from INSPIRE-HEP API
- Extracts DOIs, arXiv IDs, titles, authors, publication info
- Adds automatic arXiv buttons
- Adds document types and tags

**Image Handling**: **NONE**
- API endpoint (`https://inspirehep.net/api/literature`) queried with fields: `control_number,dois,arxiv_eprints,titles,authors,publication_info,document_type,inspire_categories` (Line 37)
- No `image` field requested from API
- No image processing in plugin code
- INSPIRE-HEP literature API does not provide publication thumbnail images

**Implementation Date**: 2025-11-10 (per plan document `/thoughts/shared/plans/2025-11-10-inspire-hep-citation-fetcher.md`)

### ORCID Plugin

**File**: `_cite/plugins/orcid.py:1-140`

**Functionality**:
- Fetches publication list from ORCID API
- Extracts DOIs and basic metadata
- Creates sources for Manubot processing

**Image Handling**: **NONE**
- No image extraction from ORCID API
- ORCID provides profile pictures but not publication images

### PubMed Plugin

**File**: `_cite/plugins/pubmed.py`

**Functionality**:
- Searches NCBI PubMed database
- Returns PMIDs for Manubot processing

**Image Handling**: **NONE**
- PubMed API does not provide publication thumbnails
- Journal cover images not accessed

### Google Scholar Plugin

**File**: `_cite/plugins/google-scholar.py`

**Functionality**:
- Fetches publication metadata via SerpAPI
- Returns titles, authors, publishers, dates

**Image Handling**: **NONE**
- SerpAPI response does not include images
- Google Scholar displays thumbnails in UI but not via API

### Sources Plugin (Manual Entries)

**File**: `_cite/plugins/sources.py:1-6`

**Functionality**:
```python
def main(entry):
    return [entry]  # Pass-through only
```

**Image Handling**: **MANUAL ONLY**
- If user includes `image` field in `_data/sources.yaml`, it passes through
- No automatic fetching or validation
- This is the **only** way to currently add images to publications

## Manubot Integration

**File**: `_cite/util.py:186-252`

The `cite_with_manubot()` function fetches metadata from DOIs/arXiv/PubMed:

**Fields Extracted**:
- Title (line 214)
- Authors (lines 216-222)
- Publisher (lines 224-228)
- Date (lines 238-246)
- Link/URL (line 249)

**Image Handling**: **NONE**
- Manubot CSL-JSON output does not include image field
- No processing for publisher thumbnails or journal covers
- Function at `util.py:186-252` has no image-related code

## Historical Context from Thoughts Directory

### Phase 5 Publication Workflow Documentation

**File**: `/thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md:116-139`

Documents the manual image specification pattern:

```yaml
image: https://journals.plos.org/...  # Optional: thumbnail URL
```

**Key Points**:
- Images are documented as "optional"
- Only URL format shown (external hosting)
- No mention of automatic fetching mechanisms
- 180px width recommended

### INSPIRE-HEP Implementation Plan

**File**: `/thoughts/shared/plans/2025-11-10-inspire-hep-citation-fetcher.md:1-1030`

**Scope Explicitly Excludes Images**:

Line 106-120 "What We're NOT Doing" section:
- Does NOT mention image fetching as excluded
- Focus on literature records only (Line 114)
- No INSPIRE-specific display fields (Line 117)

**Plugin Capabilities** (Lines 40-50):
- Extracts DOIs, arXiv IDs, titles, authors
- Generates arXiv button links
- Optional metadata (citation counts, document types)
- **No mention of image fetching**

**Metadata Enrichment** (Lines 430-550, Phase 3):
- Adds arXiv buttons automatically
- Adds citation counts and tags
- **No image processing**

### Greene Lab Website Setup Plan

**File**: `/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`

Phase 5 publication tasks (lines 830-889 per Phase 5 workflow doc):
- Add publications with Manubot
- Add optional buttons (arXiv links, code repositories)
- No mention of image requirements or fetching

## Similar Features: Project Images

**File**: `_data/projects.yaml:1-30`

Projects use images successfully with local files:

```yaml
- title: Cool Dataset
  image: images/photo.jpg  # Local file path
  link: https://github.com/
  description: Lorem ipsum...
```

**Pattern**: Local images stored in `images/` directory, referenced by relative path

**Difference from Publications**: Projects have manually curated images, publications do not

## Where Publication Images Could Come From

### Potential External Sources (Not Implemented)

1. **arXiv API**:
   - Provides PDF and source files
   - Could generate first-page thumbnails from PDF
   - Not currently accessed for images

2. **Publisher APIs**:
   - Springer, Elsevier, Wiley provide cover art
   - Crossref API has limited image support
   - Requires API keys and terms compliance
   - Not implemented in any plugin

3. **DOI Metadata**:
   - Some DOI resolvers include thumbnail links
   - Not standardized across publishers
   - Manubot doesn't extract image metadata

4. **INSPIRE-HEP Thumbnails**:
   - INSPIRE-HEP web interface shows paper thumbnails
   - Not available via REST API literature endpoint
   - Would require web scraping (not API-based)

5. **Open Graph / Social Media Tags**:
   - Many journal articles include og:image meta tags
   - Would require HTML fetching and parsing
   - Not implemented

### Manual Image Sources (Currently Used)

1. **Local Files**:
   - Store images in `images/` directory
   - Reference as `image: images/publication-name.jpg`
   - Requires manual download and curation

2. **External URLs**:
   - Direct link to hosted images
   - Format: `image: https://example.com/image.jpg`
   - Risk of broken links if source removed

## Code References

### Display Components
- `_includes/citation.html:13-27` - Image rendering logic
- `_includes/fallback.html` - Image fallback handler
- `_styles/citation.scss` - Image styling

### Data Processing
- `_cite/cite.py:26-95` - Plugin orchestration (no image logic)
- `_cite/util.py:186-252` - Manubot metadata extraction (no images)
- `_data/citations.yaml:1-50` - Generated output (no image fields)

### Input Configuration
- `_data/sources.yaml:1-10` - Manual entries (supports image field)
- `_data/inspire-hep.yaml` - INSPIRE-HEP config (no image options)

### Plugins
- `_cite/plugins/inspire-hep.py:1-132` - INSPIRE-HEP fetcher (no images)
- `_cite/plugins/orcid.py:1-140` - ORCID fetcher (no images)
- `_cite/plugins/sources.py:1-6` - Manual passthrough (preserves images if provided)

## Architecture Documentation

### Current Image Flow

```
User Input (Manual)
       |
       v
_data/sources.yaml
  image: https://...
       |
       v
sources.py plugin
  (passthrough)
       |
       v
_data/citations.yaml
  image: https://...
       |
       v
citation.html template
  (renders if style="rich")
       |
       v
Research page display
```

**Characteristics**:
- Entirely manual process
- No validation or processing
- No automatic fetching from any source
- Single entry point (sources.yaml)

### What Doesn't Exist

The following components **do not exist** in the codebase:

1. **Image Fetching Service**: No code to download or generate publication thumbnails
2. **Image Processing Pipeline**: No thumbnail generation, resizing, or optimization
3. **Image Cache**: No local storage of fetched images
4. **Image Validation**: No checks for broken links or missing images
5. **API Integration for Images**: No calls to publisher APIs, arXiv rendering services, etc.
6. **Automatic Image Discovery**: No scanning of publication pages for og:image tags
7. **Image Configuration**: No settings in `_config.yaml` for image sources or preferences

## System Limitations

### Technical Constraints

1. **Static Site Architecture**: Jekyll generates static HTML at build time
   - No server-side image fetching during page load
   - All images must be known at build time
   - Dynamic image loading would require JavaScript

2. **Plugin Execution**: Runs locally before git commit (per GitLab deployment plan)
   - Image fetching would need to happen in Python plugins
   - Downloaded images would need to be committed to repository
   - Increases repository size if storing images locally

3. **API Limitations**:
   - INSPIRE-HEP API: Does not provide image URLs
   - ORCID API: Provides profile pictures only, not publication images
   - Manubot: CSL-JSON format doesn't include images
   - PubMed: No thumbnail support in API

4. **Copyright and Licensing**: Publication images (journal covers, first pages) have copyright restrictions
   - Fair use applies to academic contexts
   - Redistribution may require publisher permission
   - arXiv allows thumbnail generation from PDFs

### Current Implementation Gaps

1. **No Image Field Population**: All 30+ current publications lack image fields
2. **No Plugin Support**: Zero plugins fetch or process images
3. **No Documentation**: No workflow documented for adding images
4. **No Validation**: No checks for broken image URLs or missing files
5. **No Fallback Strategy**: If image URL breaks, displays broken image icon

## Related Research

- `/thoughts/shared/research/2025-11-10-phase-5-publication-workflow.md` - Publication system documentation
- `/thoughts/shared/plans/2025-11-10-inspire-hep-citation-fetcher.md` - INSPIRE-HEP plugin implementation
- `/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md` - Overall website setup plan

## Conclusion

The website template provides **complete support for displaying publication images** through the citation template and rich styling mode, but **zero support for automatically fetching images**. All publication images must be manually specified in `_data/sources.yaml` using the `image` field with either external URLs or local file paths.

The recently implemented INSPIRE-HEP plugin, while comprehensive in fetching publication metadata (DOIs, arXiv IDs, authors, citation counts, tags), does not include any image fetching capability. This was not identified as a requirement in the implementation plan and is consistent with the API's lack of image support.

**Current State Summary**:
- ✅ Image display infrastructure: Complete
- ✅ Image styling and responsive design: Complete
- ✅ Image configuration format: Documented
- ❌ Automatic image fetching: Not implemented
- ❌ Image processing pipeline: Does not exist
- ❌ Plugin support for images: None

**Manual Workflow Available**:
1. Add `image: URL` field to publication entry in `_data/sources.yaml`
2. Run `python _cite/cite.py` to regenerate citations
3. Images appear on research page when rendered with `style="rich"`
