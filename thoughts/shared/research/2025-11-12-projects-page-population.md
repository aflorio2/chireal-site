---
date: 2025-11-12T13:10:17+0100
researcher: Claude (Sonnet 4.5)
git_commit: 14d296ab18a65e275968c3a335bca5e8f2c2cb4b
branch: main
repository: QCReaTE-website
topic: "How to Populate the Projects Page in Greene Lab Website Template"
tags: [research, codebase, greene-lab-template, projects, website-setup]
status: complete
last_updated: 2025-11-12
last_updated_by: Claude (Sonnet 4.5)
---

# Research: How to Populate the Projects Page in Greene Lab Website Template

**Date**: 2025-11-12T13:10:17+0100
**Researcher**: Claude (Sonnet 4.5)
**Git Commit**: 14d296ab18a65e275968c3a335bca5e8f2c2cb4b
**Branch**: main
**Repository**: QCReaTE-website

## Research Question

In the context of the Greene Lab website setup plan (`site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`), how should the Projects page be populated for the QuIReal research group website?

## Summary

The Greene Lab template provides a dedicated Projects page (`projects/index.md`) distinct from the Research page, designed for showcasing software tools, datasets, computational resources, and ongoing research initiatives. The Projects page uses a card-based display system with data managed through `_data/projects.yaml`, featuring a two-tier structure: "Featured" projects (3-5 highlighted items) and "More" projects (complete listing with smaller cards). The page includes tag filtering, search functionality, and supports linking to GitHub repositories, external websites, and demos.

For QuIReal (quantum information and real-time evolution in QFT), the Projects page should showcase computational tools (lattice simulators, analysis frameworks), numerical datasets, tutorials, and collaborative initiatives, with brief 2-4 sentence descriptions and 800x400px visualization images.

## Detailed Findings

### Current State of QuIReal Site

**Existing Structure** (as of commit 14d296a):
- Projects page exists at `site/projects/index.md:1-28`
- Projects data file at `site/_data/projects.yaml:1-48` contains 5 sample Greene Lab entries
- No `images/projects/` directory created yet
- Research page (`site/research/index.md:1-35`) currently displays only publications
- Page navigation: Research (order: 1), Projects (order: 2)

**Current projects.yaml Content**:
The file contains placeholder data with 5 sample projects:
- "Cool Dataset", "Cool Package", "Cool Tutorial" (tagged as resources)
- "Cool Web App", "Cool Web Server" (tagged as software)
All entries use Lorem ipsum descriptions and placeholder images (`images/photo.jpg`)

### Greene Lab Template: Projects Page Architecture

**Page Structure** (`site/projects/index.md:1-28`):

```markdown
---
title: Projects
nav:
  order: 2
  tooltip: Software, datasets, and more
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

[Intro text - Line 10-11]

{% include tags.html tags="publication, resource, website" %}
{% include search-info.html %}
{% include section.html %}

## Featured
{% include list.html component="card" data="projects" filter="group == 'featured'" %}

{% include section.html %}

## More
{% include list.html component="card" data="projects" filter="!group" style="small" %}
```

**Key Components**:
- **Line 8**: Icon display (wrench icon for projects)
- **Line 13**: Tag filtering system for visitor-side filtering
- **Lines 19-21**: Featured section - displays projects with `group: featured` in YAML
- **Lines 25-27**: More section - displays all other projects (without group field) in smaller cards

**Display Component** (`site/_includes/card.html:1-48`):
The card component renders each project with:
- Clickable image thumbnail (lines 3-16)
- Title as link (lines 19-30)
- Subtitle (lines 33-35)
- Description with Markdown support (lines 37-41)
- Tags and GitHub repo badges (lines 43-45)

**List Controller** (`site/_includes/list.html:1-60`):
The list component handles:
- Data loading from `site.data[include.data]` (line 2)
- Filtering by custom criteria (line 5)
- Year grouping (lines 8-12, for dated items)
- Component rendering with all fields passed through (lines 25-57)

### Projects Data Schema

**Required Fields** (`_data/projects.yaml`):
```yaml
- title: String           # Project name (required)
  description: String     # 2-4 sentence description (required)
```

**Optional But Recommended Fields**:
```yaml
  subtitle: String        # Brief tagline
  group: featured         # Use "featured" for highlighted projects
  image: String           # Path to project image (e.g., images/projects/name.jpg)
  link: URL               # Link to project page/repo/demo
  repo: owner/repo        # GitHub repository (auto-generates badges)
  tags:                   # Category tags for filtering
    - tag1
    - tag2
```

**Image Specifications**:
- **Size**: 800x400px (2:1 aspect ratio recommended)
- **File size**: < 500KB each
- **Format**: JPG or PNG
- **Naming**: Descriptive lowercase with hyphens (e.g., `cosmolattice-sim.jpg`)
- **Content**: Visualizations, diagrams, screenshots, plots from papers

### Conceptual Distinction: Projects vs Research

**Research Page** (`site/research/index.md:1-35`):
- Purpose: Published academic papers, scholarly publications
- Data source: `_data/citations.yaml` → `_data/citations-output.yaml` (auto-generated via Manubot)
- Content: Papers with DOIs, arXiv links, journal metadata
- Updates: Automatic via Manubot DOI resolution

**Projects Page** (`site/projects/index.md:1-28`):
- Purpose: Software tools, datasets, computational resources, ongoing initiatives
- Data source: `_data/projects.yaml` (manually curated)
- Content: Reusable outputs, code repositories, educational materials
- Updates: Manual entry in YAML file

**For QuIReal Specifically**:
- **Research**: Papers on thermalization, entanglement, gauge theories, lattice QFT
- **Projects**: Simulation codes, lattice configurations, tensor network tools, quantum computing implementations, tutorials

### Best Practices from Greene Lab Community

**From Web Research** (Greene Lab template gallery and documentation):

1. **Project Count**:
   - Featured: 3-5 most important projects
   - Total: 5-15 projects typical for academic groups
   - More than 20 projects may require additional organization

2. **Description Length**: 2-4 sentences maximum
   - Sentence 1: What the project is
   - Sentence 2: Technical approach or key features
   - Sentence 3-4: Applications or significance

3. **Visual Consistency**:
   - Use similar styling/color schemes for all project images
   - Consider creating consistent template for visualizations
   - Physics groups often use: simulation screenshots, Feynman diagrams, lattice visualizations, phase diagrams

4. **Linking Strategy**:
   - All projects should link somewhere (GitHub repo, project website, paper, or demo)
   - GitHub `repo` field adds credibility with auto-generated badges
   - For multi-component projects, link to main hub page

5. **Tagging Conventions**:
   - Common tags for physics groups: software, simulation, dataset, tutorial, resource, analysis
   - Tags enable visitor-side filtering on the page
   - Keep tags broad (3-6 unique tags across all projects)

6. **Project Lifecycle**:
   - Some labs create "Legacy" section for older/archived projects
   - Consider moving completed projects to "More" section
   - Keep Featured section for active/maintained projects

7. **Update Frequency**:
   - Add new projects as they reach usable state
   - Update descriptions when major versions release
   - Refresh images if visualization improves

### Example Lab Implementations

**From Greene Lab Gallery Research**:

1. **Greene Lab** (https://greenelab.com/):
   - Renamed "Projects" to "Tools"
   - 4 featured tools, ~10 more tools
   - Separate "Affiliated Organizations" and "Legacy" sections
   - Emphasis on "100% open-source, and free for anyone"

2. **Rokita Lab** (https://rokitalab.com/):
   - Clear separation: Research (scientific investigations) vs Projects (tools and data)
   - Project descriptions emphasize reusability and open science
   - Links to publications alongside project links

3. **CAMP Lab** (https://camp-lab.org/):
   - Uses "Code and Data" instead of "Projects"
   - Organizes by research topic tags
   - Includes team member details for each project

4. **CU DBMI Software Engineering Team** (https://cu-dbmi.github.io/set-website/):
   - Uses "Portfolio" instead of "Projects"
   - Focus on web applications and data pipelines
   - Prominent screenshots/demos

**Pattern**: Computational/bioinformatics labs use separate Projects page; experimental labs often integrate into Research page only.

## Code References

### Key Files:
- `site/projects/index.md:1-28` - Projects page structure
- `site/_data/projects.yaml:1-48` - Projects data file (currently sample data)
- `site/_includes/card.html:1-48` - Card component for project display
- `site/_includes/list.html:1-60` - List controller for rendering projects
- `site/_includes/tags.html` - Tag filtering component
- `site/research/index.md:1-35` - Research page for comparison

### Display Logic:
- Featured projects filter: `site/projects/index.md:21` - `filter="group == 'featured'"`
- More projects filter: `site/projects/index.md:27` - `filter="!group"` (no group field)
- Card component image: `site/_includes/card.html:10-14` - Lazy loading with fallback
- Card description: `site/_includes/card.html:38-40` - Markdown support via `markdownify`

## Architecture Documentation

### Data Flow:

1. **Projects YAML** (`_data/projects.yaml`) → **Jekyll data loader** → **List component** → **Card component** → **HTML output**

2. **Page Organization**:
   ```
   projects/index.md
   ├── Front matter (title, nav order, tooltip)
   ├── Icon + page title
   ├── Intro text (lines 10-11)
   ├── Tag filter (line 13)
   ├── Search info (line 15)
   ├── Featured section (lines 19-21)
   │   └── list.html → card.html (group == 'featured')
   └── More section (lines 25-27)
       └── list.html → card.html (!group, style=small)
   ```

3. **Component Hierarchy**:
   ```
   list.html (controller)
   ├── Loads data from site.data.projects
   ├── Applies filter criteria
   ├── Groups by year (if applicable)
   └── For each project:
       └── Includes card.html
           ├── Renders image
           ├── Renders title + link
           ├── Renders subtitle
           ├── Renders description (Markdown)
           └── Renders tags + repo badges
   ```

4. **Styling**:
   - Card component has `data-style` attribute for variations
   - Small style applied to "More" section: `style="small"`
   - Responsive design handled by template CSS

### File Organization Convention:

```
site/
├── projects/
│   └── index.md              # Projects page
├── _data/
│   └── projects.yaml         # Projects data
├── _includes/
│   ├── card.html             # Project card component
│   ├── list.html             # List controller
│   └── tags.html             # Tag filtering
└── images/
    └── projects/             # Project images (needs creation)
        ├── project1.jpg
        ├── project2.jpg
        └── ...
```

## Recommendations for QuIReal

### Step-by-Step Implementation:

**1. Create Images Directory**:
```bash
mkdir -p site/images/projects/
```

**2. Identify QuIReal Projects**:
Based on research focus (quantum information, real-time evolution, lattice QFT), typical projects might include:
- Lattice field theory simulators (e.g., CosmoLattice-related codes)
- Tensor network libraries for QFT
- Quantum computing implementations (IBM Q, Google Cirq)
- Analysis frameworks for entanglement/thermalization
- Numerical datasets (lattice configurations, correlation functions)
- Educational materials (lecture notes, Jupyter notebooks)

**3. Prepare Project Images**:
- Create visualizations: phase diagrams, lattice configurations, Feynman diagrams, simulation results
- Use consistent color scheme matching site theme (purple/cyan)
- Export at 800x400px, optimize to < 500KB
- Name descriptively: `lattice-simulator.jpg`, `entanglement-analysis.jpg`

**4. Update projects.yaml**:
Replace sample data with real entries. Example structure:

```yaml
# Featured project 1
- title: CosmoLattice Extensions
  subtitle: Real-time evolution in expanding universe
  group: featured
  image: images/projects/cosmolattice.jpg
  link: https://github.com/quireal/cosmolattice-extension
  description: >
    Extensions to CosmoLattice for studying real-time quantum field evolution
    in curved spacetime. Implements advanced diagnostics for entanglement
    entropy and out-of-equilibrium thermalization in gauge theories.
  repo: quireal/cosmolattice-extension
  tags:
    - software
    - simulation

# Featured project 2
- title: Tensor Network QFT Toolkit
  subtitle: Efficient algorithms for lattice gauge theory
  group: featured
  image: images/projects/tensor-network.jpg
  link: https://github.com/quireal/tnqft
  description: >
    Tensor network methods for real-time evolution of gauge theories.
    Enables computation of entanglement measures and quantum information
    probes in strongly-coupled systems.
  repo: quireal/tnqft
  tags:
    - software
    - quantum-computing

# More projects
- title: Lattice QCD Configurations Database
  subtitle: High-precision numerical datasets
  image: images/projects/lattice-data.jpg
  link: https://data.quireal.org
  description: >
    Open dataset of lattice configurations for QCD thermalization studies.
    Includes metadata, analysis scripts, and documentation for reproducibility.
  tags:
    - dataset
    - resource
```

**5. Update Page Intro** (`projects/index.md:10-11`):
Replace Lorem ipsum with:
```markdown
Our group develops open-source tools, datasets, and educational resources for
studying quantum information and real-time evolution in quantum field theory.
All projects are freely available to support reproducible research in theoretical
physics and quantum computing.
```

**6. Customize Tags** (`projects/index.md:13`):
Update to relevant categories:
```markdown
{% include tags.html tags="software, simulation, dataset, tutorial, quantum-computing" %}
```

**7. Test Locally**:
```bash
cd site/
bundle exec jekyll serve
# Visit http://localhost:4000/projects
```

**8. Commit and Deploy**:
```bash
cd site/
git add _data/projects.yaml images/projects/ projects/index.md
git commit -m "Populate Projects page with QuIReal research tools and datasets"
git push origin main
```

### Content Guidelines for QuIReal:

**Project Types to Consider**:
1. **Simulation Software**: Lattice codes, real-time evolution engines
2. **Analysis Tools**: Entanglement calculators, correlation function analyzers
3. **Quantum Computing**: IBM Q/Cirq implementations, circuit libraries
4. **Datasets**: Lattice configurations, numerical results, benchmarks
5. **Educational**: Tutorials, Jupyter notebooks, lecture materials
6. **Collaborative**: Multi-institution projects, computing infrastructure

**Writing Style**:
- Technical but accessible to physics graduate students
- Emphasize: capabilities, applications, availability
- Mention: publications using the tool (link to Research page)
- Highlight: open-source nature, reproducibility

**Image Content Ideas**:
- Simulation results: field configurations, time evolution plots
- Entanglement entropy vs time plots
- Lattice structure diagrams
- Phase diagrams (temperature vs coupling)
- Quantum circuit diagrams
- Feynman diagrams for processes studied
- Screenshots of GUI tools (if applicable)

## Historical Context (from thoughts/)

**Related Planning Document**: `site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`

**Phase 5 Planning** (lines 734-1063):
The setup plan outlines Phase 5 as "Content Population (Team, Publications, Projects)" with these specifications for projects:

- **Timeline**: Part of 6-8 hour Phase 5
- **File**: `_data/projects.yaml` (line 891)
- **Image specs**: 800x400px, < 500KB, descriptive filenames (lines 942-947)
- **Structure example**: Lines 896-941 show sample theoretical physics projects
- **Success criteria**: Lines 1041 (2+ projects in YAML), 1054-1055 (projects display with images)

**Current Phase Status** (from plan):
- Phase 1-4: Completed (template forked, environment setup, CI/CD configured, site branded as QuIReal)
- Phase 5: Team members added (3 members), publications pending, **projects not yet populated**
- Phase 6: Not started (polish and launch)

**QuIReal Branding** (completed 2025-11-09, lines 719-730):
- Site rebranded from QCReaTE to QuIReal
- Focus: "Quantum Information and Real-time evolution in QFT"
- Custom purple/cyan theme applied
- Logo created with quantum notation |χ⟩

**Next Steps Per Plan** (line 1062):
After populating projects in Phase 5, should proceed to Phase 6 for final polish, testing, and launch.

## Related Research

**Previous Research Document**: `site/thoughts/shared/research/2025-11-07-physics-group-website-design-static-site-generators.md`
- Research comparing static site generators
- Decision rationale for Greene Lab template
- Platform decision (GitLab Pages)
- Manual Local Manubot approach

**Implementation Plan**: `site/thoughts/shared/plans/2025-11-07-greene-lab-website-setup.md`
- Complete 6-phase implementation roadmap
- Phase 5 includes projects population
- Timeline: 16-24 total hours
- Maintenance workflow documented

## Open Questions

1. **Specific QuIReal Projects**: Which computational tools/datasets from the group's research should be prioritized for the Projects page?

2. **Image Creation**: Does the group have existing visualizations suitable for project images, or should new graphics be created?

3. **GitHub Repository Structure**: Are QuIReal projects in a unified GitHub organization (e.g., github.com/quireal/) or distributed across individual accounts?

4. **Project Maturity**: Which projects are mature enough for public listing vs. still in development?

5. **External Hosting**: Are datasets hosted on external platforms (Zenodo, OSF, institutional repos) that should be linked?

6. **Legacy Projects**: Are there older tools from group members' previous work that should be included in a "Legacy" or "Contributed" section?

7. **Collaborative Projects**: How to attribute multi-institution collaborative projects (list all partners, link to main project site)?

8. **Tutorial Format**: Should educational materials be listed as separate projects or integrated into project descriptions?

## External Resources

### Greene Lab Template Documentation:
- **Main Documentation**: https://greene-lab.gitbook.io/lab-website-template-docs
- **Projects Page Demo**: https://greenelab.github.io/lab-website-template/projects/
- **GitHub Repository**: https://github.com/greenelab/lab-website-template
- **Repo Structure Guide**: https://greene-lab.gitbook.io/lab-website-template-docs/basics/repo-structure
- **Edit Pages Guide**: https://greene-lab.gitbook.io/lab-website-template-docs/basics/edit-pages
- **List Component Docs**: https://greene-lab.gitbook.io/lab-website-template-docs/components/list
- **Gallery of Example Sites**: https://greene-lab.gitbook.io/lab-website-template-docs/introduction/gallery

### Template Files Referenced:
- **Projects page structure**: https://github.com/greenelab/lab-website-template/blob/main/projects/index.md
- **Projects data file**: https://github.com/greenelab/lab-website-template/blob/main/_data/projects.yaml
- **Card component**: https://github.com/greenelab/lab-website-template/blob/main/_includes/card.html
- **List component**: https://github.com/greenelab/lab-website-template/blob/main/_includes/list.html

### Example Lab Websites:
- **Greene Lab** (tools focus): https://greenelab.com/
- **Su Lab** (projects page): https://sulab.org/
- **CAMP Lab** (code and data): https://camp-lab.org/
- **Rokita Lab** (research vs projects): https://rokitalab.com/
- **CU DBMI SET** (portfolio approach): https://cu-dbmi.github.io/set-website/

## Conclusion

The Projects page in the Greene Lab template provides a flexible, maintainable system for showcasing computational tools, datasets, and research outputs. For QuIReal, populating this page requires:

1. Creating project images directory (`images/projects/`)
2. Identifying 5-10 key projects (lattice codes, analysis tools, datasets, tutorials)
3. Preparing 800x400px visualization images
4. Updating `_data/projects.yaml` with real project entries
5. Customizing page intro text and tags
6. Testing locally and deploying via Git

The page structure is already correctly configured in the QuIReal site. The main remaining task is content creation: gathering project information, creating/optimizing images, and writing concise descriptions. This aligns with Phase 5 of the implementation plan and should take approximately 2-4 hours depending on project count and image preparation needs.

The Projects page serves a distinct purpose from the Research page: while Research showcases published papers, Projects highlights reusable computational tools and resources that support both the group's research and the broader physics community.
