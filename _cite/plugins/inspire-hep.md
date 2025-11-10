# INSPIRE-HEP Plugin Documentation

## Overview

The INSPIRE-HEP plugin automatically fetches publication lists from [INSPIRE-HEP](https://inspirehep.net/), the primary literature database for high-energy physics. Publications are automatically enriched with DOIs, arXiv links, physics category tags, and other metadata.

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
  enable_metadata: true  # Default: true, adds arXiv buttons and INSPIRE category tags
```

Set `enable_metadata: false` to disable automatic metadata enrichment.

## Features

### Automatic DOI/arXiv Extraction

The plugin automatically:
- Prefers DOI as primary identifier (better for Manubot citation generation)
- Falls back to arXiv ID if no DOI available
- Adds arXiv buttons automatically for papers with arXiv versions

### Automatic Filtering

Papers are automatically filtered to exclude:
- **Conference papers** - Only articles and theses are included
- **Large collaborations** - Papers with more than 20 authors are excluded

These filters are hardcoded in the plugin and ensure a focused publication list.

### Metadata Enrichment

When `enable_metadata: true` (default):
- **arXiv buttons** added to all papers with arXiv IDs
- **Document types** mapped (article, thesis, etc.)
- **INSPIRE category tags** added for physics subfield classification:
  - Theory-HEP
  - Phenomenology-HEP
  - Lattice
  - Quantum Physics
  - Theory-Nucl
  - Condensed Matter
  - Experiment-HEP
  - Experiment-Nucl
  - Gravitation and Cosmology
  - Astrophysics
  - General Physics

### Caching

API responses are cached for 7 days to:
- Speed up repeated builds
- Respect INSPIRE-HEP rate limits (15 requests per 5 seconds)
- Reduce network traffic

Cache location: `_cite/.cache/`

To clear cache: `rm -rf _cite/.cache/`

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
2. Filter out conference papers and large collaborations
3. Extract DOIs and arXiv IDs
4. Enrich metadata with arXiv buttons and category tags
5. Merge with other sources (ORCID, manual entries)
6. Call Manubot for full citation metadata
7. Generate `_data/citations.yaml`

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

### Problem: No publications fetched

- Verify your BAI is correct: Visit https://inspirehep.net/authors/{your-bai}
- Check INSPIRE-HEP has publications for your author
- Look for warnings in `python _cite/cite.py` output

### Problem: Fewer papers than expected

Check the automatic filters:
- Conference papers are excluded
- Papers with >20 authors are excluded
- Modify `_cite/plugins/inspire-hep.py` lines 59-67 to adjust filters

### Problem: Duplicate publications with ORCID plugin

- This is expected! The cite.py script merges duplicates automatically
- Keep both plugins enabled for maximum coverage
- INSPIRE-HEP typically has better metadata for physics papers

### Problem: Cache not refreshing

- Delete cache: `rm -rf _cite/.cache/`
- Or wait 7 days for automatic cache expiration

### Problem: Rate limit errors (HTTP 429)

- Wait 5 seconds between manual runs
- Cache should prevent this in normal usage

### Problem: Missing arXiv buttons

- Verify `enable_metadata: true` in your config (or omit for default)
- Check that papers have arXiv IDs in INSPIRE-HEP
- Inspect `_data/citations.yaml` for button data

## Integration with Other Plugins

The INSPIRE-HEP plugin runs in this order:

1. google-scholar (if configured)
2. pubmed (if configured)
3. orcid (if configured)
4. **inspire-hep** ← You are here
5. sources (manual entries)

Duplicates are automatically merged by DOI/arXiv ID, with later sources overriding earlier ones.

## Customizing Filters

To modify the automatic filters, edit `site/_cite/plugins/inspire-hep.py`:

**Conference paper filter** (lines 59-62):
```python
# Filter: Skip conference papers/proceedings
document_types = get_safe(metadata, "document_type", [])
if "conference paper" in document_types or "proceedings" in document_types:
    continue
```

**Author count filter** (lines 64-67):
```python
# Filter: Skip papers with more than 20 authors
authors = get_safe(metadata, "authors", [])
if len(authors) > 20:
    continue
```

Adjust the number `20` or comment out entire filter blocks to customize behavior.

## Technical Details

**Plugin Architecture**:
- Follows Greene Lab template plugin pattern
- Uses `@cache.memoize()` decorator for 7-day caching
- Returns list of sources with Manubot-compatible IDs
- Metadata fields override Manubot fields

**Data Flow**:
1. Read `_data/inspire-hep.yaml` configuration
2. Query INSPIRE-HEP API for each BAI
3. Filter papers by document type and author count
4. Extract DOIs (preferred) or arXiv IDs (fallback)
5. Add metadata (buttons, tags, document types)
6. Return sources for Manubot processing

**Cache Key**: Based on BAI only (filters are applied post-fetch)

## Requirements

No additional Python packages required beyond the standard citation system dependencies:
- manubot
- PyYAML
- diskcache
- rich
- python-dotenv

All required libraries are already in `_cite/requirements.txt`.

## Credits

Developed for the Greene Lab website template integration with INSPIRE-HEP database.

- Template: https://github.com/greenelab/lab-website-template
- INSPIRE-HEP: https://inspirehep.net/
- Plugin implementation: 2025
