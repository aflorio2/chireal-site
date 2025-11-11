---
date: 2025-11-11 13:34:40 CET
researcher: Adrien Florio
git_commit: 937bd59a6f626ad3427668f1f8960feafbbb4d17
branch: main
repository: site
topic: "Jekyll Website Architecture for CV-Style Personal Page Customization"
tags: [research, codebase, jekyll, personal-page, cv, templating, members]
status: complete
last_updated: 2025-11-11
last_updated_by: Adrien Florio
---

# Research: Jekyll Website Architecture for CV-Style Personal Page Customization

**Date**: 2025-11-11 13:34:40 CET
**Researcher**: Adrien Florio
**Git Commit**: 937bd59a6f626ad3427668f1f8960feafbbb4d17
**Branch**: main
**Repository**: site

## Research Question

How does the current Jekyll website architecture work, and what existing patterns can be used to customize personal pages in a CV-like fashion (similar to https://aleksas.eu/cv/) with sections for general information, education, experience, and outreach projects?

## Summary

The Jekyll website uses a **collection-based architecture** for managing team member profiles. The current system generates individual member pages automatically from markdown files in the `_members/` collection. Each member page uses the `member` layout which displays a floating portrait with contact links alongside biographical content.

The site architecture is highly modular with:
- **3 layouts** (default, member, post)
- **32 reusable components** in `_includes/`
- **Data-driven content** from YAML files in `_data/`
- **Custom theme** (no external theme dependency)
- **Type system** defining icons, links, and templates for 50+ types

To create CV-style personal pages, you can leverage the existing `member` layout and customize the markdown content structure to include CV sections (Education, Experience, Outreach Projects). The current member files already support rich markdown content with sections, and the layout automatically handles portrait display, contact links, and publication linking.

## Detailed Findings

### Reference CV Structure (https://aleksas.eu/cv/)

The reference site uses the **al-folio** Jekyll theme and organizes CV content into four main sections:

1. **General Information**: Name, pronunciation (phonetic and IPA), nationality
2. **Education**: Three degrees listed chronologically (earliest to latest) with institutions, dates, achievements, dissertation titles, and advisor information
3. **Experience**: Professional positions (2014-present) in reverse chronological order with institutional affiliations and key responsibilities
4. **Outreach Projects**: Community engagement activities since 2020 with organizational roles

**Layout Features**:
- Clean, hierarchical structure using date ranges as organizing elements
- Indented subsections for details
- Top navigation
- Downloadable PDF version
- Footer credits Jekyll and al-folio theme

### Current Jekyll Architecture

#### Directory Structure

The site is located at `/Users/aflorio/Documents/GroupWebsite/site/` with the following structure:

```
site/
├── _config.yaml              # Main Jekyll configuration
├── _layouts/                 # Page layouts (3 files)
│   ├── default.html          # Base HTML structure
│   ├── member.html           # Team member pages
│   └── post.html             # Blog post pages
├── _includes/                # Reusable components (32 files)
│   ├── head.html             # Meta tags, styles, scripts
│   ├── header.html           # Site header with navigation
│   ├── footer.html           # Site footer with links
│   ├── content.html          # Content section processor
│   ├── portrait.html         # Member portraits
│   ├── button.html           # Link buttons
│   ├── citation.html         # Publication citations
│   ├── card.html             # Project cards
│   ├── feature.html          # Feature sections
│   ├── list.html             # Generic list renderer
│   └── ...                   # 22 other components
├── _data/                    # YAML data files
│   ├── types.yaml            # Icon/link type definitions
│   ├── projects.yaml         # Project data
│   ├── citations.yaml        # Publication data (auto-generated)
│   ├── orcid.yaml            # ORCID data
│   ├── inspire-hep.yaml      # InspireHEP citation data
│   └── sources.yaml          # Publication sources
├── _members/                 # Team member markdown (3 files)
│   ├── adrien-florio.md
│   ├── franz-sattler.md
│   └── vasundhara-krishnan.md
├── _posts/                   # Blog post markdown (3 files)
├── _styles/                  # SCSS stylesheets (45 files)
├── _scripts/                 # JavaScript files (7 files)
├── _plugins/                 # Custom Jekyll plugins (5 Ruby files)
├── _cite/                    # Citation fetching system (Python)
├── images/                   # Image assets
│   ├── team/                 # Member photos (4 files)
│   ├── publications/         # Publication thumbnails (26 files)
│   └── ...                   # Other images
├── index.md                  # Homepage
├── team/index.md             # Team listing page
├── research/index.md         # Research/publications page
├── projects/index.md         # Projects showcase
├── blog/index.md             # Blog listing
├── about/index.md            # About page
└── contact/index.md          # Contact page
```

#### Jekyll Configuration (`_config.yaml:1-82`)

**Site Properties**:
- Title: "QuIReal - Quantum Information and Real-time evolution in QFT"
- Subtitle: "Adrien Florio's Emmy Noether group"
- Custom theme: `theme: null` (line 59)
- Base URL: Empty string for root deployment
- URL: GitLab Pages at `https://qcreate-website-fa4cbb.pages.ub.uni-bielefeld.de`

**Collections Configuration** (`_config.yaml:40-46`):
```yaml
collections:
  members:
    output: true
  posts:
    output: true
```

**Front Matter Defaults** (`_config.yaml:23-38`):
- All markdown files: `default` layout
- Members collection: `member` layout
- Posts collection: `post` layout

**Plugins** (`_config.yaml:49-53`):
- `jekyll-spaceship` - Enhanced markdown
- `jekyll-sitemap` - Automatic sitemap
- `jekyll-redirect-from` - URL redirection
- `jekyll-feed` - RSS feed

**Asset Directories**:
- Sass: `_styles/` (line 63)
- Scripts: `_scripts/` (configured separately)

### Member Profile System

#### Member File Pattern (`_members/*.md`)

**Front Matter Structure**:
```yaml
---
name: "Full Name"
image: images/team/photo.jpg
role: pi  # or postdoc, phd, undergrad, programmer, mascot
affiliation: "Institution Name"
aliases:
  - "A. Name"
  - "A Name"
links:
  email: email@university.edu
  orcid: 0000-0002-XXXX-XXXX
  google-scholar: SCHOLAR_ID
  inspirehep: https://inspirehep.net/authors/XXXXX
  github: username
  home-page: https://example.com
---
```

**Content Structure** (examples from `_members/adrien-florio.md:15-32`):
```markdown
Biography paragraph with introduction.

## Research Interests

Bulleted list or paragraph describing research focus:
- Topic 1
- Topic 2
- Topic 3

## Background

Educational and career history.

## Selected Publications

[Auto-linked via aliases]
```

**Role Types Available** (`_data/types.yaml:5-28`):
- `pi` / `principal-investigator` - Microscope icon
- `postdoc` - Glasses icon
- `phd` - Graduation cap icon
- `undergrad` - User-graduate icon
- `programmer` - Code icon
- `mascot` - Dog icon

**Link Types Available** (`_data/types.yaml:46-133`):
- `email` - Automatically creates mailto: link
- `phone` - Automatically creates tel: link
- `address` - Map location icon
- `home-page` - House icon
- `orcid` - Links to https://orcid.org/[ID]
- `google-scholar` - Links to Google Scholar profile
- `inspirehep` - Links to INSPIRE-HEP profile
- `github` - Links to GitHub profile
- `twitter`, `bluesky`, `linkedin` - Social media profiles

#### Member Layout (`_layouts/member.html:1-51`)

The layout inherits from `default` and creates a two-column structure:

**Left Column (Floating)** (`member.html:5-19`):
- Member portrait via `portrait.html` include
- Contact buttons from `page.links` using `button.html` include

**Right Column (Main Content)** (`member.html:21`):
- Rendered markdown content from member file

**Bottom Section** (`member.html:23-39`):
- Auto-generated link to search for member's publications on research page
- Uses `aliases` field to create comprehensive search

**Flow**:
1. Captures portrait and contact buttons into `floatcontent` variable
2. Includes `float.html` to display floating sidebar
3. Renders page content (markdown)
4. Generates publication search link using aliases

#### Portrait Component (`_includes/portrait.html:1-51`)

**Lookup Mechanism** (`portrait.html:1-8`):
```liquid
{% if include.lookup %}
  {% assign member = site.members
    | where_exp: "member", "member.slug == include.lookup"
    | first
  %}
{% else %}
  {% assign member = include %}
{% endif %}
```

**Rendering** (`portrait.html:12-51`):
- Links to member page (unless already on that page)
- Displays role icon from `types.yaml`
- Shows circular portrait image (lazy loaded)
- Displays name, role description, and affiliation

**Styling** (`_styles/portrait.scss:1-62`):
- Default: 175px width, vertical layout
- `data-style="small"`: 100px width
- `data-style="tiny"`: Horizontal layout, 50px image

#### Float Component (`_includes/float.html:1-12`)

Creates floating sidebar that wraps on mobile (`_styles/float.scss:1-33`):
- Floats left by default (or right with `data-flip`)
- Max-width: 50%
- Responsive: Stacks on screens < 600px

### Team Listing Page (`team/index.md:1-29`)

**Front Matter**:
```yaml
---
title: Team
nav:
  order: 3
  tooltip: About our team
---
```

**Content Structure**:
1. Heading with icon
2. Group description paragraph
3. Section break
4. PI portraits: `{% include list.html data="members" component="portrait" filter="role == 'pi'" %}`
5. Other member portraits: `{% include list.html data="members" component="portrait" filter="role != 'pi'" %}`
6. Section break
7. Recruitment section with contact button

### List Component (`_includes/list.html:1-59`)

Generic component for rendering data collections:

**Data Loading** (`list.html:1-6`):
- Loads from `site.data[name]` or `site[name]` collection
- Applies filter expression via custom `data_filter`

**Year Grouping** (`list.html:8-12`):
- Groups items by year from `date` property
- Sorts years descending (newest first)

**Rendering** (`list.html:14-59`):
- Loops through years and items
- Dynamically includes specified component (e.g., `portrait.html`, `citation.html`)
- Passes all possible properties to component

**Usage Examples**:
- Team page: `component="portrait"` with `filter="role == 'pi'"`
- Research page: `component="citation"` with `style="rich"`
- Projects page: `component="card"` with `filter="group == 'featured'"`

### Button Component (`_includes/button.html:1-34`)

Creates styled link buttons with icons:

**Type Resolution** (`button.html:1-2`):
```liquid
{% assign button = include %}
{% assign button = button | hash_default: site.data.types[include.type] %}
```

**Link Processing** (`button.html:4-10`):
- Replaces `$VALUE` placeholder in type template with actual value
- Detects absolute vs. relative URLs
- Handles mailto: and tel: links

**Rendering** (`button.html:11-34`):
- Displays icon and optional text
- Adds tooltip from type definition
- Opens external links in new tab
- Supports different styles (bare, etc.)

### Type System (`_data/types.yaml:1-229`)

Central configuration file defining icons, text, tooltips, and link templates for 50+ types:

**Team Roles** (lines 5-28): 6 roles with icons and descriptions
**General Links** (lines 30-72): Website, email, phone, address, search
**Social Media** (lines 74-133): ORCID, Google Scholar, INSPIRE-HEP, GitHub, Twitter, Bluesky, LinkedIn, etc.
**Alert Types** (lines 135-160): Tip, help, info, success, warning, error
**Publication Types** (lines 162-197): Paper, book, article, journal, preprint
**Software Types** (lines 199-229): Docs, source, server, app, data, package

**Example Type Definition**:
```yaml
orcid:
  icon: fa-brands fa-orcid
  text: ORCID
  tooltip: ORCID
  link: https://orcid.org/$VALUE
```

### Section System (`_includes/section.html:1-10`, `_includes/content.html:1-38`)

**Section Break Syntax**:
```liquid
{% include section.html %}
{% include section.html background="images/bg.jpg" dark=true size="wide" %}
```

**Processing Flow**:
1. `section.html` outputs `<!-- section break -->` comment with metadata tags
2. `content.html` splits page content on section breaks
3. Extracts metadata using regex: `<dark>`, `<background>`, `<size>`
4. Wraps each section in `<section>` element with data attributes and styles

**Section Sizes**:
- `page` (default): Standard content width
- `wide`: Wider content area
- `full`: Full-width section

### Citation System

**Auto-Generated Data** (`_data/citations.yaml:1`):
- Comment: "DO NOT EDIT, GENERATED AUTOMATICALLY"
- Fetched from ORCID, INSPIRE-HEP, Google Scholar

**Citation Structure**:
```yaml
- id: arXiv:XXXX.XXXXX
  title: "Paper Title"
  authors:
    - Author One
    - Author Two
  publisher: Journal Name
  date: YYYY-MM-DD
  link: https://arxiv.org/abs/XXXX.XXXXX
  buttons:
    - type: preprint
      link: https://arxiv.org/abs/XXXX.XXXXX
  image: images/publications_highlights/image.png
  tags: [Theory-HEP, Condensed Matter]
```

**Citation Component** (`_includes/citation.html:1-109`):
- Lookup by ID or title search
- Displays type icon, title, authors (truncated), publisher, date
- Rich style shows image, description, buttons, tags

**Research Page** (`research/index.md:1-34`):
- Highlighted publications section with featured papers
- Full publication list with search functionality
- Uses `list.html` with `component="citation"` and `style="rich"`

### Member Page URL Generation

**Automatic URL Creation**:
- File: `_members/adrien-florio.md`
- Slug: `adrien-florio` (derived from filename)
- URL: `/team/adrien-florio/`

**Member Lookup in Liquid**:
```liquid
{% assign member = site.members | where: "slug", "adrien-florio" | first %}
{{ member.url }}  <!-- outputs: /team/adrien-florio/ -->
```

### About Page Pattern (`about/index.md:1-73`)

The about page demonstrates a multi-section content structure:

**Front Matter**:
```yaml
---
title: About
nav:
  order: 4
  tooltip: About our research group
---
```

**Content Sections**:
1. Title with icon
2. Introduction paragraph
3. Section break
4. Mission statement
5. Section break
6. Research areas with H3 subsections
7. Section break
8. Facilities & Resources
9. Section break
10. Collaborations
11. Section break
12. Join Us with contact button

**Pattern**: Alternates between content blocks and `{% include section.html %}` for visual separation

## Code References

Key files for CV-style customization:

- `_config.yaml:40-46` - Collections configuration
- `_layouts/member.html:1-51` - Member page layout
- `_includes/portrait.html:1-51` - Portrait component
- `_includes/button.html:1-34` - Contact button component
- `_includes/float.html:1-12` - Floating sidebar wrapper
- `_includes/list.html:1-59` - Generic list renderer
- `_data/types.yaml:5-28` - Role definitions
- `_data/types.yaml:46-133` - Link type definitions
- `_members/adrien-florio.md:1-32` - Example member profile
- `team/index.md:1-29` - Team listing page
- `about/index.md:1-73` - About page pattern
- `_styles/portrait.scss:1-62` - Portrait styling
- `_styles/float.scss:1-33` - Float layout styling

## Architecture Documentation

### Current Design Patterns

**1. Collection-Based Member Management**
- Members stored as individual markdown files in `_members/` collection
- Each file generates a dedicated page at `/team/[slug]/`
- Front matter defines metadata (name, role, links)
- Markdown content defines biography and sections

**2. Component-Based UI**
- Atomic components: `icon.html`, `button.html`, `section.html`
- Composite components: `portrait.html`, `citation.html`, `card.html`
- Layout components: `float.html`, `list.html`, `grid.html`
- All components accept parameters via `include` syntax

**3. Data-Driven Content**
- Type system in `types.yaml` defines 50+ type templates
- Publications auto-fetched from ORCID/INSPIRE-HEP
- Projects defined in `projects.yaml`
- Components merge include parameters with type defaults

**4. Responsive Layout Strategy**
- Float component: Sidebar on desktop, stacked on mobile
- Portrait component: Multiple size variants (default, small, tiny)
- Section system: Configurable widths (page, wide, full)
- Mobile breakpoint: 600px

**5. Publication Linking**
- Member `aliases` field defines name variations
- Member layout generates search link: `/research/?search="A. Florio" "A Florio"`
- Research page searches citations by author name

### Templating Flow

**Page Generation Flow**:
1. User creates markdown file in `_members/`
2. Jekyll applies `member` layout via front matter defaults
3. Layout renders portrait + contact buttons in floating sidebar
4. Layout renders markdown content in main area
5. Layout generates publication search link
6. Jekyll outputs HTML file at `/team/[slug]/index.html`

**Component Resolution Flow**:
1. Layout includes component: `{% include button.html type="email" link="user@example.com" %}`
2. Component loads type definition from `types.yaml`
3. Component merges include parameters with type defaults
4. Component processes link template: replaces `$VALUE` with actual value
5. Component renders HTML with merged properties

**List Rendering Flow**:
1. Page includes list: `{% include list.html data="members" component="portrait" filter="role == 'pi'" %}`
2. List loads data from `site.members` collection
3. List applies filter: keeps only members where `role == 'pi'`
4. List groups by year (if date field exists)
5. List loops through filtered data
6. List dynamically includes portrait component for each member
7. List passes all member properties to portrait component

## How to Create CV-Style Personal Pages

### Option 1: Customize Member Markdown Content

**Current Capability**: Member files already support rich markdown with sections.

**Steps**:
1. Edit your member file (e.g., `_members/adrien-florio.md`)
2. Add CV sections using markdown headings:

```markdown
---
name: Adrien Florio
image: images/team/adrien-florio.jpg
role: pi
affiliation: Bielefeld University
aliases:
  - A. Florio
links:
  email: adrien.florio@uni-bielefeld.de
  orcid: 0000-0002-XXXX-XXXX
---

Adrien Florio is the Principal Investigator of the QuIReal Emmy Noether research group.

## Education

**PhD in Physics** - University Name, 2012-2017
- Dissertation: "Title of Dissertation"
- Advisor: Prof. Name

**Master of Science in Physics** - University Name, 2010-2012
- Thesis: "Title of Thesis"

**Bachelor of Science in Physics** - University Name, 2007-2010

## Professional Experience

**Emmy Noether Group Leader** - Bielefeld University, 2023-present
- Leading research group on quantum information and real-time evolution
- Managing team of postdocs and PhD students
- Developing computational methods for quantum field theory

**Postdoctoral Researcher** - Institution Name, 2019-2023
- Research on quantum entanglement in high-energy physics
- Collaboration with experimental groups

**PhD Researcher** - Institution Name, 2012-2017
- Dissertation research on quantum field theory
- Teaching assistant for undergraduate courses

## Research Interests

- Quantum information in curved spacetime
- Real-time evolution in quantum field theory
- Quantum entanglement in high-energy physics
- Computational methods for quantum field theory

## Outreach & Service

**Co-organizer** - Physics Department Open House, 2024-present
- Organizing public lectures and demonstrations

**Reviewer** - Physical Review Letters, JHEP, 2020-present

**Mentor** - Graduate student mentoring program, 2021-present

## Selected Publications

[Auto-linked via aliases]
```

3. The existing `member` layout will display:
   - Portrait and contact links in floating sidebar
   - All CV sections in main content area
   - Link to publications at bottom

### Option 2: Create Custom CV Layout

**If you need different styling or structure**:

1. Create new layout file: `_layouts/cv.html`
2. Inherit from `default` or `member` layout
3. Customize section display, styling, or ordering
4. Add front matter to member file: `layout: cv`

### Option 3: Create Dedicated CV Page

**For a separate CV page distinct from team profile**:

1. Create `cv/index.md` in root directory
2. Use custom layout or inline HTML/CSS
3. Link from member profile or navigation menu
4. Optionally generate PDF version

## Styling Considerations

**Current Styles**:
- Portrait: Circular image, 175px default width (`_styles/portrait.scss`)
- Buttons: Icon + text, bare style for sidebar (`_styles/button.scss`)
- Float: 50% width on desktop, full width on mobile (`_styles/float.scss`)
- Headings: Consistent typography from theme (`_styles/heading.scss`)

**For CV Styling**:
- Consider date formatting for education/experience entries
- Add custom styles for indented subsections
- Style reverse chronological ordering
- Consider print-friendly CSS for PDF generation

## Related Research

No previous research documents found in `thoughts/shared/research/` on this topic.

## Open Questions

1. **CV Layout Preference**: Should the CV content be:
   - Within the existing member profile page (Option 1)?
   - A separate dedicated CV page linked from the profile (Option 3)?
   - A custom layout variant (Option 2)?

2. **PDF Generation**: Is a downloadable PDF version of the CV needed?
   - If yes, consider using CSS `@media print` or a PDF generation plugin

3. **Date Formatting**: Should education/experience entries use structured data?
   - Could create a custom `_data/cv.yaml` file for structured CV entries
   - Could use YAML front matter in member file for CV sections

4. **Publication Integration**: How should publications be displayed in CV context?
   - Currently auto-linked via aliases at bottom of page
   - Could integrate citation components directly into CV sections
   - Could show selected publications vs. all publications

5. **Timeline Visualization**: Should chronological information be visualized?
   - Could add CSS timeline styling for experience/education sections
   - Could create custom timeline component

6. **Multilingual Support**: Is translation needed for CV content?
   - Jekyll supports multiple languages through plugins
   - Could create separate CV files per language

7. **Section Ordering**: Should CV sections be reorderable via front matter?
   - Could define section order in YAML
   - Could create flexible CV template that reads section configuration

## Next Steps

Based on this research, the recommended approach for creating a CV-style personal page is:

1. **Immediate**: Customize the markdown content in `_members/adrien-florio.md` to add CV sections (Education, Experience, Outreach) using markdown headings and lists. This requires no code changes and works with the existing `member` layout.

2. **Short-term**: Add custom CSS to `_styles/` for CV-specific styling:
   - Date formatting for chronological entries
   - Indentation for subsections
   - Print-friendly styles for PDF generation

3. **Optional**: If the floating portrait layout doesn't work for CV content:
   - Create `_layouts/cv.html` that modifies the `member` layout
   - Adjust float positioning or remove float entirely
   - Customize section ordering and display

4. **Future**: Consider creating a structured data approach:
   - Define CV entries in YAML format
   - Create custom components for rendering education/experience
   - Enable easier maintenance and potential reuse across multiple members
