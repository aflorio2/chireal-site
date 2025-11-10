# Research: Phase 5 Publication Workflow and System Documentation

**Date**: 2025-11-10
**Researcher**: Adrien Florio (inferred from plan document)
**Topic**: Publication system implementation for Phase 5 of Greene Lab website setup
**Status**: complete

## Research Question

Document the publication/citation system in the Greene Lab template to prepare for Phase 5 implementation (Content Population - Publications). Focus on understanding the current system architecture, data flow, automation capabilities, and workflow to inform streamlined publication management.

## Summary

The Greene Lab template uses a Python-based citation compilation system (`_cite/cite.py`) that aggregates publications from multiple sources (ORCID, Google Scholar, PubMed, manual entries) and generates a unified citation database. The system features:

1. **Multi-source aggregation**: Plugins fetch from ORCID API, Google Scholar (via SerpAPI), PubMed, and manual YAML entries
2. **Automated metadata**: Manubot CLI fetches complete bibliographic metadata from DOIs and other identifiers
3. **Two-stage processing**: Input sources → Plugin processing → Manubot enrichment → Output YAML
4. **Display system**: Liquid templates render citations with rich metadata, images, buttons, tags, and search
5. **Automation options**: GitHub Actions workflows exist in template (weekly updates, PR creation)
6. **Manual workflow**: The implementation plan specifies manual local Manubot execution (not CI/CD-based)

**Key Finding**: The template provides two automation approaches:
- **GitHub Actions**: Fully automated weekly citation updates with PR creation (in template)
- **Manual Local**: User runs Python script locally before Git push (planned implementation)

The planned GitLab deployment uses the manual approach where `python _cite/cite.py` runs locally, not in CI/CD pipeline.

## Phase 5 Scope (From Implementation Plan)

### What Phase 5 Covers

From `/Users/aflorio/Documents/GroupWebsite/site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`:

**Lines 734-1062**: Phase 5: Content Population (Team, Publications, Projects)

#### Publications-Specific Tasks (Lines 830-889):

1. **Add Publications with Manubot** (Lines 830-889):
   - Clear sample data from `_data/sources.yaml`
   - Add publication DOIs in YAML format
   - Add optional buttons (arXiv links, code repositories, data links)
   - Run Manubot locally: `manubot process --content-directory=.`
   - Verify `_data/citations-output.yaml` generated with full metadata
   - Commit both input and output files

2. **Success Criteria - Automated** (Lines 1037-1046):
   - [ ] Citations YAML has DOIs: `grep "doi:" site/_data/citations.yaml | wc -l` ≥ 3
   - [ ] Manubot processed: `test -f site/_data/citations-output.yaml` exists
   - [ ] Local build succeeds: `cd site && bundle exec jekyll build`

3. **Success Criteria - Manual** (Lines 1050-1053):
   - [ ] Publications page displays 3+ papers with complete metadata
   - [ ] Publication metadata looks correct (titles, authors, journals, dates)
   - [ ] arXiv/PDF buttons work on publications

**Note**: The plan references `citations-output.yaml` but the actual Greene Lab template uses `citations.yaml` as output (line 21 in cite.py). This is a discrepancy in the plan document.

### Other Phase 5 Content

- Add team member photos and YAML entries (Lines 742-829)
- Configure research projects (Lines 892-948)
- Create initial blog post (Lines 950-990)
- Test and deploy all content (Lines 992-1032)

## Publication System Architecture

### Data Flow Overview

```
Input Sources                Plugin Processing           Manubot Enrichment         Output
──────────────              ─────────────────           ──────────────────         ──────

_data/orcid.yaml     ───>   orcid.py          ───>                          ───>
_data/sources.yaml   ───>   sources.py        ───>     cite_with_manubot()  ───>  _data/citations.yaml
_data/pubmed.yaml    ───>   pubmed.py         ───>     (DOI → metadata)     ───>
_data/google-scholar ───>   google-scholar.py ───>                          ───>

                             cite.py orchestrates entire pipeline
                             Merges duplicates, handles errors, formats dates
```

### File Locations

**Core System Files**:
- `/Users/aflorio/Documents/GroupWebsite/site/_cite/cite.py` - Main orchestration script
- `/Users/aflorio/Documents/GroupWebsite/site/_cite/util.py` - Utilities (Manubot wrapper, caching, I/O)
- `/Users/aflorio/Documents/GroupWebsite/site/_cite/requirements.txt` - Python dependencies

**Plugin Files** (in `_cite/plugins/`):
- `sources.py` - Pass-through for manual entries
- `orcid.py` - ORCID Public API integration
- `pubmed.py` - NCBI PubMed eSearch API
- `google-scholar.py` - Google Scholar via SerpAPI

**Data Files**:
- Input: `_data/orcid.yaml`, `_data/sources.yaml`, `_data/pubmed.yaml`, `_data/google-scholar.yaml`
- Output: `_data/citations.yaml` (auto-generated, do not edit)
- Configuration: `_data/types.yaml` (icon/button type definitions)

**Display Components**:
- `_includes/citation.html` - Citation rendering template
- `_includes/list.html` - List component with grouping/sorting
- `_includes/button.html` - Action button renderer
- `_styles/citation.scss` - Citation styling with container queries

**Pages**:
- `research/index.md` - Publications page with search

## Current Citation Data Structure

### Input Format: sources.yaml

Manual citation entries in `/Users/aflorio/Documents/GroupWebsite/site/_data/sources.yaml`:

```yaml
- id: doi:10.1371/journal.pcbi.1007128          # Required for Manubot
  type: paper                                     # Optional: publication type
  description: Lorem ipsum _dolor_ **sit amet**  # Optional: markdown description
  date: 2020-12-4                                 # Optional: will be normalized
  image: https://journals.plos.org/...            # Optional: thumbnail URL
  buttons:                                        # Optional: custom action buttons
    - type: manubot
      link: https://greenelab.github.io/meta-review/
    - type: source
      text: Manuscript Source
      link: https://github.com/greenelab/meta-review
  tags:                                           # Optional: filter tags
    - open science
    - collaboration
  repo: greenelab/meta-review                     # Optional: GitHub repo
```

**Field Descriptions**:
- `id`: Manubot identifier (doi:, pmid:, arxiv:, url:)
- `type`: Publication type (paper, book, article, preprint) - maps to icon
- `description`: Markdown text displayed below citation
- `date`: Any format (normalized to YYYY-MM-DD)
- `image`: Thumbnail URL (180px width recommended)
- `buttons`: Array of action buttons (type/link/text)
- `tags`: Search/filter tags
- `repo`: GitHub repository reference

### Input Format: orcid.yaml

ORCID profile identifiers in `/Users/aflorio/Documents/GroupWebsite/site/_data/orcid.yaml`:

```yaml
- orcid: 0000-0002-4655-3773  # ORCID identifier only
```

**Processing**:
- Plugin queries `https://pub.orcid.org/v3.0/{orcid}/works`
- Extracts work IDs (prefers DOI over other types)
- Creates source entries with `id: doi:...` for Manubot

### Output Format: citations.yaml

Generated file at `/Users/aflorio/Documents/GroupWebsite/site/_data/citations.yaml` (264 lines total):

```yaml
# DO NOT EDIT, GENERATED AUTOMATICALLY

- id: doi:10.1371/journal.pcbi.1007128
  title: Open collaborative writing with Manubot        # From Manubot
  authors:                                              # From Manubot
  - Daniel S. Himmelstein
  - Vincent Rubinetti
  - David R. Slochower
  publisher: PLOS Computational Biology                 # From Manubot
  date: '2020-12-04'                                    # Normalized from Manubot
  link: https://doi.org/c7np                            # From Manubot
  orcid: 0000-0002-4655-3773                            # From input source
  plugin: sources.py                                     # Plugin tracking
  file: sources.yaml                                     # File tracking
  type: paper                                           # Preserved from input
  description: Lorem ipsum _dolor_ **sit amet**        # Preserved from input
  image: https://journals.plos.org/...                  # Preserved from input
  buttons:                                              # Preserved from input
  - type: manubot
    link: https://greenelab.github.io/meta-review/
  tags:                                                 # Preserved from input
  - open science
  - collaboration
  repo: greenelab/meta-review                           # Preserved from input
```

**Manubot-Generated Fields**:
- `id`, `title`, `authors`, `publisher`, `date`, `link`

**Source-Preserved Fields**:
- `type`, `description`, `image`, `buttons`, `tags`, `repo`

**Metadata Fields** (added by cite.py):
- `plugin`: Source plugin filename
- `file`: Input data filename
- `orcid`: ORCID if from ORCID source

## Processing Pipeline Details

### cite.py Orchestration (Lines 1-206)

**Stage 1: Plugin Execution** (Lines 26-95)
- Execution order: google-scholar → pubmed → orcid → sources
- For each plugin:
  - Loads corresponding data files (`_data/{plugin}*.*`)
  - Validates format (must be list of dicts)
  - Calls plugin's `main(entry)` function
  - Appends `plugin` and `file` metadata
- Result: List of source entries from all plugins

**Stage 2: Duplicate Merging** (Lines 97-110)
- Finds entries with matching non-blank IDs
- Merges later entries into earlier ones via `dict.update()`
- Removes empty entries
- Result: Deduplicated source list

**Stage 3: Manubot Enrichment** (Lines 113-171)
- For each source with an `id`:
  - Calls `cite_with_manubot(_id)` from util.py
  - Caches results for 90 days
  - Updates citation with source fields (source overrides Manubot)
  - Formats date to YYYY-MM-DD
- Error handling:
  - Fatal error for user sources (sources.py)
  - Warning for metasources (orcid.py, etc.)
- Result: Enriched citations with full metadata

**Stage 4: Output** (Lines 173-206)
- Saves to `_data/citations.yaml` with warning header
- Reports errors and warnings
- Exits with code 1 if errors occurred

### Manubot Integration (util.py Lines 186-252)

**Function**: `cite_with_manubot(_id)`

**Caching**:
```python
@cache.memoize(name="manubot", expire=90 * (60 * 60 * 24))  # 90 days
```
Cache location: `./_cite/.cache`

**Execution**:
```python
commands = ["manubot", "cite", _id, "--log-level=WARNING"]
output = subprocess.Popen(commands, stdout=subprocess.PIPE).communicate()
```

**Metadata Extraction** (Lines 207-250):
- Parses Manubot JSON response
- Extracts fields from CSL-JSON format:
  - Citation ID (line 214)
  - Title (line 214)
  - Authors: Formatted as "Given Family" (lines 216-222)
  - Publisher: container-title > publisher > collection-title (lines 224-228)
  - Date: Normalized to YYYY-MM-DD (lines 238-246)
  - Link: URL field (line 249)

**Supported Identifiers**:
- `doi:10.1234/example`
- `pmid:12345678`
- `pmcid:PMC1234567`
- `arxiv:1234.5678`
- `url:https://...`

### Plugin Details

#### sources.py (Lines 1-6)
Simple pass-through:
```python
def main(entry):
    return [entry]
```
Returns entry unchanged as single-item list.

#### orcid.py (Lines 1-140)

**API**: `https://pub.orcid.org/v3.0/{ORCID}/works`

**Caching**: 24 hours

**Processing**:
1. Query ORCID for works (line 14)
2. Filter by relationship type: self, version-of, part-of (lines 37-41)
3. Filter by Manubot-citable types (lines 51-52)
4. Sort by preference (DOI preferred) (lines 56-64)
5. For each work:
   - If citable ID exists: Create source with `id` (lines 88-93)
   - If no ID: Preserve title/publisher/date manually (lines 96-132)

**ID Preference Order**: DOI > other Manubot-supported types

#### pubmed.py (Lines 1-46)

**API**: NCBI Entrez eSearch

**Input**: `term` field from pubmed.yaml

**Processing**:
- Searches PubMed with term (max 1000 results)
- Returns sources with `id: pubmed:{PMID}`

#### google-scholar.py (Lines 1-61)

**API**: SerpAPI Google Scholar

**Authentication**: Requires `GOOGLE_SCHOLAR_API_KEY` environment variable

**Input**: `gsid` (Google Scholar ID) from google-scholar.yaml

**Processing**:
- Queries author profile (max 100 articles)
- Google Scholar doesn't provide Manubot IDs
- Returns sources with manual fields: title, authors, publisher, date, link

## Display System

### Citation Template (citation.html Lines 1-109)

**Two Modes**:
1. **Lookup mode**: `{% include citation.html lookup="Title or ID" %}`
   - Searches `site.data.citations` for matching ID or title
2. **Direct mode**: `{% include citation.html id="..." title="..." %}`
   - Uses provided citation data directly

**Two Styles**:
1. **Basic** (default): Title, authors, details only
2. **Rich** (`style="rich"`): Adds image, description, buttons, tags

**Rendering Elements**:
- Type icon (top-right, from types.yaml)
- Image (if rich style, lazy-loaded)
- Title (linked to publication)
- Authors (first 5, tooltip if >10)
- Publisher · Date · ID
- Description (markdown, if rich style)
- Buttons (custom actions, if rich style)
- Tags (filterable, if rich style)

### List Component (list.html)

**Usage**: `{% include list.html data="citations" component="citation" style="rich" %}`

**Processing**:
- Loads `site.data.citations`
- Groups by year (extracted from date field)
- Sorts years descending
- Within year, sorts citations by date descending
- Renders each via citation.html

**Found in**: `research/index.md:27`

### Search System (search.js Lines 1-214)

**Search Syntax**:
- `term1 term2` - All terms must match (AND)
- `"full phrase"` - At least one phrase must match (OR)
- `"tag: tagname"` - At least one tag must match (OR)

**Searchable Content**:
- Element text (innerText)
- Tooltip attributes (data-tooltip)
- Search attributes (data-search)

**Interactive Features**:
- Real-time filtering (1000ms debounce)
- URL query parameter updates
- Term highlighting
- Results counter

## Automation Approaches

### GitHub Actions (Template Default)

The Greene Lab template includes automated citation updates via GitHub Actions.

#### Workflow: update-citations.yaml (Lines 1-102)

**Triggers**:
- `workflow_call`: Called by other workflows
- `workflow_dispatch`: Manual trigger

**Process**:
1. Checkout repository
2. Set up Python 3.11
3. Install dependencies from `_cite/requirements.txt`
4. Run `python _cite/cite.py` (15 min timeout)
5. Check if `_data/citations.yaml` changed
6. Either:
   - **Commit directly** (`inputs.open-pr != true`)
   - **Open PR** (`inputs.open-pr == true`)

**Environment**:
- `GOOGLE_SCHOLAR_API_KEY` from secrets

**Error Handling**:
- Cache committed on failure
- Changed files detection via `tj-actions/verify-changed-files`

#### Workflow: on-schedule.yaml (Lines 1-23)

**Trigger**: Weekly (Monday at 00:00 UTC)

**Process**:
- Calls `update-citations.yaml` with `open-pr: true`
- Only runs on user instances (not template repo itself)

**Result**: Automatic PR with weekly citation updates

### Manual Local Approach (Planned Implementation)

From implementation plan lines 2-3 of `.gitlab-ci.yml` and lines 830-889 of Phase 5:

**Current Approach**:
- Manubot runs **locally**, not in CI/CD
- User executes: `python _cite/cite.py` (or `manubot process --content-directory=.`)
- User commits generated `_data/citations.yaml`
- GitLab CI/CD only builds Jekyll site

**GitLab CI/CD** (`.gitlab-ci.yml` Lines 1-36):
```yaml
# Manual Local Manubot approach - Manubot runs locally, not in CI

image: ruby:3.2

before_script:
  - gem install bundler
  - bundle install --path vendor/bundle

pages:
  stage: deploy
  script:
    - bundle exec jekyll build -d public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

**No Python/Manubot in CI** - Citations must be generated locally before push.

### Comparison

| Feature | GitHub Actions (Template) | Manual Local (Planned) |
|---------|---------------------------|------------------------|
| Citation updates | Automated weekly | Manual before push |
| Trigger | Cron schedule + manual | User executes locally |
| PR creation | Yes (for review) | No |
| Dependencies in CI | Python + Manubot | Ruby + Jekyll only |
| Build time | ~5-10 min (includes Python) | ~1-3 min (Jekyll only) |
| API key storage | GitHub Secrets | Local .env file |
| Maintenance | Zero user action | Run script before push |

## Workflow Documentation

### Adding a Publication (Manual Approach)

From plan lines 1518-1549:

**Steps**:
1. Edit `_data/sources.yaml`, add entry:
   ```yaml
   - id: doi:10.1103/PhysRevD.XXX.XXXXXX
     buttons:
       - type: preprint
         text: arXiv
         link: https://arxiv.org/abs/XXXX.XXXXX
   ```

2. Run citation processor:
   ```bash
   cd site/
   python _cite/cite.py
   ```

3. Verify output:
   ```bash
   cat _data/citations.yaml  # Check new entry
   ```

4. Preview locally:
   ```bash
   bundle exec jekyll serve
   # Visit http://localhost:4000/research
   ```

5. Commit and push:
   ```bash
   git add _data/
   git commit -m "Add publication: [Short Title]"
   git push origin main
   ```

6. Wait for GitLab CI/CD deployment (1-3 minutes)

**Time Estimate**: ~2 minutes (from plan line 1520)

### Current Installation Status

From plan Phase 2 success criteria (lines 280-296):

**Verified Installations**:
- ✅ Ruby 3.3.10 installed
- ✅ Jekyll dependencies installed
- ✅ Manubot v0.6.1 installed (via npm)
- ✅ Site builds successfully locally
- ✅ Local server functional

**Installed Command**:
```bash
/Users/aflorio/Library/Python/3.9/bin/manubot process --content-directory=.
```

**Alternative** (via cite.py):
```bash
cd /Users/aflorio/Documents/GroupWebsite/site
python _cite/cite.py
```

### Environment Setup

**Required Environment Variables**:
- `GOOGLE_SCHOLAR_API_KEY` - SerpAPI key (optional, only if using Google Scholar plugin)

**Location**: `.env` file in site directory (loaded by util.py:8, 13)

**Not Required for Basic Usage**:
- DOI/ORCID/PubMed sources work without API keys
- Only Google Scholar requires SerpAPI subscription

## Current State

### Existing Citations

From `/Users/aflorio/Documents/GroupWebsite/site/_data/citations.yaml` (264 lines):

**Count**: 13 citations (estimated from file length)

**Sources**:
- ORCID plugin (majority): `plugin: orcid.py`, `file: orcid.yaml`
- Manual sources: `plugin: sources.py`, `file: sources.yaml`

**ORCID Profile**: 0000-0002-4655-3773 (Vincent Rubinetti - template default)

**Sample Entry** (Lines 3-19):
```yaml
- id: doi:10.1101/2025.06.19.660613
  title: Scalable data harmonization for single-cell image-based profiling...
  authors: [Dave Bunten, Jenna Tomkinson, ...]
  publisher: Cold Spring Harbor Laboratory
  date: '2025-06-25'
  link: https://doi.org/g9rfr3
  orcid: 0000-0002-4655-3773
  plugin: orcid.py
  file: orcid.yaml
```

### Site Configuration

From `/Users/aflorio/Documents/GroupWebsite/site/_config.yaml`:

**Site Title**: "QuIReal - Quantum Information and Real-time evolution in QFT" (line 1)

**ORCID in Config**: 0000-0002-7276-4515 (line 16) - Different from citations ORCID

**This indicates**: Need to update `_data/orcid.yaml` with correct ORCID for QuIReal group

## Template Documentation

### Official Greene Lab Docs

**README.md** (Line 15):
- Feature highlight: "Automatically generated citations from simple identifiers (DOI, PubMed, ORCID, and many more) using Manubot"

**HOWTO.md** (Lines 44-51):
```bash
# Using Manubot for Citations

manubot process --content-directory=.

# Reads from _data/citations.yaml
# Generates _data/citations-output.yaml with full metadata
```

**Note**: HOWTO references `citations-output.yaml` but actual output is `citations.yaml` (discrepancy)

### Quick Reference (HOWTO.md Lines 82-90)

| Task | Command |
|------|---------|
| Process citations | /Users/aflorio/Library/Python/3.9/bin/manubot process --content-directory=. |

## Related Research

This research complements:
- `/Users/aflorio/Documents/GroupWebsite/site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md` - Implementation plan
- `/Users/aflorio/Documents/GroupWebsite/site/thoughts/shared/research/2025-11-07-physics-group-website-design-static-site-generators.md` - Initial research on SSG selection

## Key Files Reference

**Citation Processing**:
- `site/_cite/cite.py:21` - Output file definition
- `site/_cite/cite.py:32` - Plugin execution order
- `site/_cite/cite.py:144` - Manubot call
- `site/_cite/util.py:186-252` - Manubot wrapper
- `site/_cite/plugins/sources.py:1-6` - Manual source plugin
- `site/_cite/plugins/orcid.py:1-140` - ORCID plugin

**Data Files**:
- `site/_data/citations.yaml` - Generated output (DO NOT EDIT)
- `site/_data/sources.yaml` - Manual input
- `site/_data/orcid.yaml` - ORCID IDs
- `site/_data/types.yaml:162-229` - Publication types and button types

**Display**:
- `site/_includes/citation.html:1-109` - Citation template
- `site/_includes/list.html` - List component
- `site/_styles/citation.scss` - Citation styling
- `site/research/index.md:17` - Highlighted citation
- `site/research/index.md:27` - Full citation list

**Automation**:
- `site/.github/workflows/update-citations.yaml:1-102` - GitHub Actions automation
- `site/.github/workflows/on-schedule.yaml:1-23` - Weekly schedule
- `site/.gitlab-ci.yml:1-36` - GitLab CI/CD (no Manubot)

## System Characteristics

### Strengths of Current System

1. **Multi-source aggregation**: Single command pulls from ORCID, PubMed, Google Scholar, manual sources
2. **Automatic metadata**: Manubot fetches titles, authors, journals, dates automatically
3. **Caching**: 90-day cache for Manubot, 24-hour cache for ORCID reduces API calls
4. **Flexible display**: Rich and basic styles, search/filter, responsive design
5. **Customizable**: Buttons, tags, descriptions, images can be added per publication
6. **Error handling**: Distinguishes user errors (fatal) from API errors (warnings)

### Current Limitations

1. **Manual execution**: User must remember to run `python _cite/cite.py` before pushing
2. **No CI automation**: GitLab CI doesn't run citation updates (by design in plan)
3. **ORCID mismatch**: Template default ORCID (0000-0002-4655-3773) differs from config (0000-0002-7276-4515)
4. **Documentation discrepancy**: HOWTO.md references `citations-output.yaml` but actual file is `citations.yaml`
5. **Google Scholar requires API key**: SerpAPI subscription needed for Google Scholar plugin
6. **Template sample data**: 13 citations from Vincent Rubinetti's profile, need replacement

### Manual vs Automated Trade-offs

**Manual Local Approach** (Planned):
- ✅ Simpler CI/CD (Jekyll only, faster builds)
- ✅ No secrets in GitLab (API keys stay local)
- ✅ User controls when citations update
- ❌ Requires manual execution before push
- ❌ Easy to forget to run citation update
- ❌ No automatic weekly refreshes

**Automated CI Approach** (GitHub Actions in template):
- ✅ Zero maintenance (weekly auto-updates)
- ✅ Never forget to update citations
- ✅ PR review for citation changes
- ❌ Longer CI builds (Python + Manubot installation)
- ❌ Requires API keys in CI secrets
- ❌ More complex CI configuration

## Phase 5 Implementation Context

### What Needs to Happen

Based on plan lines 830-889, Phase 5 publication tasks:

1. **Clear template data**:
   - Remove Vincent Rubinetti's ORCID from `_data/orcid.yaml`
   - Clear sample entries from `_data/sources.yaml`

2. **Add group ORCID**:
   - Update `_data/orcid.yaml` with group member ORCID (0000-0002-7276-4515 from config?)

3. **Add manual publications**:
   - Add 3-5 publications to `_data/sources.yaml` with DOIs
   - Include arXiv buttons, optional images/descriptions

4. **Generate citations**:
   - Run `python _cite/cite.py`
   - Verify `_data/citations.yaml` generated correctly

5. **Test display**:
   - Build locally: `bundle exec jekyll build`
   - Serve locally: `bundle exec jekyll serve`
   - Check `/research` page shows publications

6. **Commit and deploy**:
   - Git add `_data/` files
   - Commit with message
   - Push to GitLab
   - Verify GitLab Pages deployment

### Success Verification

**Automated Checks**:
```bash
# At least 3 DOIs
grep "doi:" site/_data/citations.yaml | wc -l  # Should be ≥ 3

# Citations file exists
test -f site/_data/citations.yaml && echo "OK"

# Local build succeeds
cd site && bundle exec jekyll build
```

**Manual Checks**:
- Visit deployed site `/research` page
- Verify 3+ publications display
- Check titles, authors, journals, dates look correct
- Test arXiv/PDF buttons work
- Verify search functionality works

### Current Blockers

None identified. System is ready for Phase 5 implementation:
- ✅ Manubot installed and working
- ✅ cite.py script functional
- ✅ Jekyll builds successfully
- ✅ GitLab CI/CD configured
- ✅ Display components working

**Only Required**: Replace template sample data with QuIReal publications

## Notes

1. **File naming discrepancy**: Implementation plan references `citations-output.yaml` but Greene Lab template uses `citations.yaml` as output. The plan may be based on older documentation. Actual file is `citations.yaml` (cite.py:21).

2. **ORCID update needed**: Config has 0000-0002-7276-4515 but citations data uses template default 0000-0002-4655-3773. Update `_data/orcid.yaml` to match group member(s).

3. **Manubot version**: Installed via npm (v0.6.1). Plan mentions both npm and pip installation methods. Current installation is npm-based.

4. **Cache location**: `./_cite/.cache` directory stores Manubot and plugin responses. This directory should be in `.gitignore`.

5. **Python version**: cite.py uses Python 3. Manubot installed in `/Users/aflorio/Library/Python/3.9/bin/`. GitHub Actions use Python 3.11.

6. **GitLab vs GitHub**: Template has GitHub Actions automation. Implementation uses GitLab with manual approach. The two approaches are mutually exclusive but functionally equivalent (automated vs manual timing).
