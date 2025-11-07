---
date: 2025-11-07T12:44:07+0000
researcher: adrien
git_commit: N/A (not a git repository)
branch: N/A
repository: GroupWebsite
topic: "Modern Static Site Generators and Design Examples for Theoretical Physics Group Website"
tags: [research, website-design, static-site-generators, gitlab-pages, hugo, jekyll, astro, eleventy, academic-websites, free-templates, open-source, greene-lab, manubot, citation-management]
status: complete
last_updated: 2025-11-07
last_updated_by: adrien
last_updated_note: "Updated with final recommendation: Greene Lab template for GitLab Pages with detailed Manubot implementation guide covering three solutions (manual local, automated CI/CD, manual citations), comprehensive comparison, customization instructions, and implementation timeline"
---

# Research: Modern Static Site Generators and Design Examples for Theoretical Physics Group Website

**Date**: 2025-11-07T12:44:07+0000
**Researcher**: adrien
**Repository**: GroupWebsite

## Research Question

What are the best modern static site generators for creating a theoretical physics group website hosted on GitLab Pages, and what are examples of well-designed (non-institutional) academic/research group websites for design inspiration?

## Summary

This research comprehensively explores modern static site generators suitable for academic physics groups and provides extensive examples of well-designed research websites. The analysis covers four leading static site generators (Hugo, Jekyll, Astro, Eleventy) with detailed comparisons of their academic suitability, GitLab Pages compatibility, and ease of maintenance. Additionally, 60+ examples of modern, professionally-designed academic and research websites are documented, focusing on custom designs that break away from traditional institutional templates.

**Key Findings**:
- **Pascal Michaillat's Hugo Template** is the top minimalist recommendation - ultra-clean design matching Bhamla Lab aesthetic, near-perfect performance
- **al-folio (Jekyll)** is the most popular academic template with 14,400+ stars, comprehensive features, and active maintenance
- **Stanford ML Group's source code** is completely open-source (MIT license) and can be cloned/customized
- **Hugo with Hugo Blox** offers purpose-built academic features with blazing-fast builds for larger groups
- **Greene Lab Template (Jekyll)** provides best automation with Manubot-powered citation generation
- Modern academic websites favor minimalist designs, custom frameworks (Squarespace, custom static sites), and visual storytelling over traditional institutional CMS templates

## Detailed Findings

### Part 1: Static Site Generators for GitLab Pages

#### 1. Hugo with Hugo Blox

**Official Links**:
- Documentation: https://gohugo.io/documentation/
- Quick Start: https://gohugo.io/getting-started/quick-start/
- GitLab Pages Deployment: https://docs.gitlab.com/tutorials/hugo/
- Hugo Blox: https://docs.hugoblox.com/
- Research Group Template: https://hugoblox.com/templates/
- Live Demo: https://research-group.netlify.app/

**Academic Suitability**: 10/10

**Key Features**:
- **Blazing-fast build times**: Sub-second builds, ~250x faster than competitors
- **Built-in LaTeX support**: Native MathJax and KaTeX integration
- **Hugo Blox Research Group Template**: Purpose-built for academic groups
  - Automatic BibTeX publication import
  - Team member profiles with photos and bios
  - News and events sections
  - Built-in contact forms
  - Trusted by 250,000+ researchers worldwide
- **No dependencies**: Single binary, no Ruby/Python/Node.js required
- **Multi-language support**: Built-in internationalization

**GitLab Pages Compatibility**: Excellent
- Official GitLab tutorial available
- Template repository: https://gitlab.com/pages/hugo
- Simple CI/CD configuration

**Learning Curve**: Moderate
- Go templates require initial learning
- Hugo Blox templates minimize complexity
- Comprehensive documentation available

**Template Ecosystem**: Excellent (100+ themes)
- Hugo Blox Research Group (free demo, premium $99)
- Multiple academic-specific templates
- Extensive documentation theme options

**Performance**: Exceptional - fastest SSG available

**Community**: 84,500+ GitHub stars, very active

**Best For**:
- Large publication databases
- Multi-member research groups
- Teams wanting minimal maintenance
- Sites requiring fast builds

---

#### 2. Jekyll with Jekyll Scholar

**Official Links**:
- Documentation: https://jekyllrb.com/docs/
- Step-by-Step Tutorial: https://jekyllrb.com/docs/step-by-step/01-setup/
- Jekyll Scholar Plugin: https://github.com/inukshuk/jekyll-scholar
- GitLab Pages: https://docs.gitlab.com/user/project/pages/
- Academic Themes: https://jekyll-themes.com/category/research

**Academic Suitability**: 9/10

**Key Features**:
- **Most mature ecosystem**: Released 2008, most established SSG
- **Jekyll Scholar plugin**: Best-in-class BibTeX support
  - Automatic citation generation
  - Publication list formatting
  - Query capabilities for filtering publications
  - Multiple bibliography file support
- **Simple, blog-aware architecture**: Intuitive for content-focused sites
- **Liquid templating**: Easy-to-learn template language
- **Extensive plugin ecosystem**: Thousands of plugins available

**GitLab Pages Compatibility**: Excellent
- Official GitLab support with templates
- Jekyll Scholar works with GitLab Pages (unlike GitHub Pages due to security restrictions)

**Learning Curve**: Easy
- Most beginner-friendly SSG
- Extensive step-by-step tutorials

**Template Ecosystem**: Excellent - largest theme collection
- sbryngelson/academic-website-template
- petridish for research projects
- uwsampa/research-group-web
- Allan Lab template with YAML data sheets

**Performance**: Moderate - slower than Hugo/Eleventy
- 7-90 seconds for 1,000+ posts

**Community**: 51,000+ GitHub stars, oldest community

**Best For**:
- Sites heavily focused on publications
- Teams comfortable with Ruby
- Smaller sites (under 500 pages)
- Extensive customization needs

---

#### 3. Astro

**Official Links**:
- Documentation: https://docs.astro.build/
- Getting Started: https://docs.astro.build/en/getting-started/
- Tutorial: https://docs.astro.build/en/tutorial/1-setup/2/
- GitLab Pages Deployment: https://docs.astro.build/en/guides/deploy/gitlab/
- Math Support Guide: https://emasuriano.com/til/2024-06-24-adding-support-for-latex-in-astrojs/
- Starlight Docs Framework: https://starlight.astro.build/
- Themes: https://astro.build/themes/

**Academic Suitability**: 8/10

**Key Features**:
- **Islands architecture**: JavaScript loads only when needed (partial hydration)
- **Zero-JavaScript by default**: Static HTML for maximum performance
- **Framework flexibility**: Mix React, Vue, Svelte, Solid.js in one project
- **Content Collections API**: Type-safe content management
- **100+ integrations**: Tailwind CSS, MDX, various CMSs
- **Astro 5.0**: Server Islands, hybrid output modes

**GitLab Pages Compatibility**: Excellent
- Full official support
- Example repository: https://gitlab.com/pages/astro

**Learning Curve**: Moderate
- JavaScript/modern web development knowledge helpful
- Exceptional documentation quality

**Template Ecosystem**: Growing rapidly (375+ themes)
- Astro Academia - personal academic sites with CV, publications
- Astro Micro Academic - with math support, search, comments
- Academic Project - for research paper pages

**Performance**: Very Fast
- Among fastest SSGs
- Zero-JavaScript default with selective hydration

**Community**: 53,000+ GitHub stars, rapidly growing

**Best For**:
- Teams with JavaScript expertise
- Sites wanting modern interactive features
- Progressive enhancement approach
- Future-proof technology stack

---

#### 4. Eleventy (11ty)

**Official Links**:
- Documentation: https://www.11ty.dev/docs/
- Starter Projects: https://www.11ty.dev/docs/starter/
- 11ty Rocks Tutorials: https://11ty.rocks/
- MathJax Plugin: https://github.com/tsung-ju/eleventy-plugin-mathjax
- KaTeX Tutorial: https://benborgers.com/posts/eleventy-katex
- Themes: https://www.11tythemes.com/

**Academic Suitability**: 7/10

**Key Features**:
- **Simplest to learn**: Most accessible for beginners
- **Zero configuration**: Works out-of-the-box
- **Multiple template languages**: 10+ options (Nunjucks, Liquid, Handlebars, Markdown, etc.)
- **ESM support**: Modern JavaScript modules
- **Progressive enhancement**: Works without JavaScript
- **Lightweight**: No client-side framework required

**GitLab Pages Compatibility**: Excellent
- Full support, standard Node.js deployment

**Learning Curve**: Easiest
- Recommended for SSG beginners
- JavaScript-based advantage for Node.js developers

**Template Ecosystem**: Growing (83+ themes)
- Academic blog templates with citation support
- Course notes/documentation templates
- Fewer pre-built academic features than Hugo/Jekyll

**Performance**: Very Fast
- Second only to Hugo
- 4,000 Markdown files in 1.93 seconds

**Community**: 18,700+ GitHub stars, rapidly growing
- Used by Google Chrome Developers, CERN, Khan Academy

**Best For**:
- Teams new to static site generators
- Custom-built solutions
- Sites prioritizing flexibility
- JavaScript-comfortable developers

---

### Comparative Summary Table

| Feature | Hugo | Jekyll | Astro | Eleventy |
|---------|------|--------|-------|----------|
| **GitHub Stars** | ~84,500 | ~51,000 | ~53,000 | ~18,700 |
| **Build Speed** | Exceptional | Moderate | Very Fast | Very Fast |
| **Learning Curve** | Moderate | Easy | Moderate | Easiest |
| **LaTeX/Math Support** | Excellent | Excellent | Excellent | Good |
| **Academic Themes** | Excellent | Excellent | Growing | Limited |
| **BibTeX Support** | Built-in (Blox) | Best (Scholar) | Custom | Custom |
| **GitLab Pages** | Excellent | Excellent | Excellent | Excellent |
| **Documentation** | Excellent | Excellent | Exceptional | Excellent |
| **Academic Rating** | 10/10 | 9/10 | 8/10 | 7/10 |

---

### Recommendations

**Best Overall: Hugo with Hugo Blox** ✓
- Purpose-built for academic research groups
- Fastest build times
- Automatic BibTeX import
- Professional templates out-of-the-box
- Ideal for large publication databases

**Best for Bibliography Management: Jekyll with Jekyll Scholar** ✓
- Most sophisticated BibTeX/publication management
- Ideal for publication-focused sites
- Extensive customization options

**Most Modern/Flexible: Astro** ✓
- Cutting-edge technology
- Exceptional documentation
- Modern development experience
- Future-proof stack

**Simplest to Learn: Eleventy** ✓
- Zero-configuration
- Gentle learning curve
- Best for teams new to SSGs

---

### Part 1B: Best Free, Open-Source Templates

#### HUGO TEMPLATES

##### 1. Pascal Michaillat's Minimalist Hugo Template ⭐ TOP MINIMALIST PICK

**Live Demo**: https://pascalmichaillat.org/hugo-website/
**GitHub**: https://github.com/pmichaillat/hugo-website
**Documentation**: https://pascalmichaillat.org/b/
**License**: MIT
**Stars**: 278+ | **Forks**: 158+

**Why Recommended**:
- **Ultra-clean minimalist design** - matches Bhamla Lab aesthetic
- **Near-perfect PageSpeed scores** - optimized performance
- **PaperMod-based** - fast, flexible, customized for academics
- **Active maintenance** - updated 2024 (Hugo v0.147.2+)
- **Real adoption** - powers 30+ active research websites
- **Minimal dependencies** - no complex build tools
- **100% free and open source**

**Key Features**:
- KaTeX math support for LaTeX notation
- Automated archive generation with reverse chronology
- Keyword/tag system for papers and courses
- Academic social icons (CV, Google Scholar, Zoom)
- Organized content sections (papers, courses, data, projects)
- RSS feeds
- Mobile-responsive
- Grayscale design with slate blue accents

**Best For**: Groups wanting the cleanest, fastest, most minimalist approach

---

##### 2. Hugo Blox Research Group Theme (covered above)
See full details in Part 1, Section 1.

---

##### 3. Hugo PaperMod - Base Theme

**Live Demo**: https://adityatelange.github.io/hugo-PaperMod/
**GitHub**: https://github.com/adityatelange/hugo-PaperMod
**License**: MIT
**Stars**: 12,600+ | **Forks**: 3,300+

**Key Features**:
- Zero external dependencies (no webpack, nodejs)
- Three display modes: Regular, Home-Info, Profile
- Light/dark theme toggle
- Built-in search (Fuse.js)
- Performance optimized with asset pipelining
- SEO optimized
- 507+ projects using this theme

**Note**: This is the base theme that Pascal Michaillat's template builds upon.

---

#### JEKYLL TEMPLATES

##### 1. al-folio ⭐ TOP JEKYLL PICK

**Live Demo**: https://alshedivat.github.io/al-folio/
**GitHub**: https://github.com/alshedivat/al-folio
**License**: MIT
**Stars**: 14,400+ | **Forks**: 12,500+

**Why Recommended**:
- **Most popular academic Jekyll theme** - massive community
- **Comprehensive features** - everything needed for academic sites
- **Beautiful clean design** - academic elegance without flashiness
- **Very actively maintained** - updated in 2024-2025
- **Excellent documentation** - CUSTOMIZE.md guide included
- **100% free** - no premium features or hidden costs
- **Used by major conferences** - ICLR Blog, ICML workshops

**Key Features**:
- Automatic BibTeX publications via jekyll-scholar
- CV generation from JSON Resume or YAML
- Light/dark mode toggle with multiple color schemes
- Distill.pub-style blog post layouts
- Math typesetting (MathJax)
- Code syntax highlighting
- GitHub repository statistics integration
- Responsive project grid
- News/announcements, collections
- Tabs, galleries, charts, Mermaid diagrams
- Related posts functionality
- Atom/RSS feeds

**Best For**: Research groups wanting proven, feature-rich template with large community support

---

##### 2. Greene Lab Website Template

**Live Demo**: https://greenelab.github.io/lab-website-template/
**GitHub**: https://github.com/greenelab/lab-website-template
**Documentation**: https://greene-lab.gitbook.io/lab-website-template-docs
**License**: BSD-3-Clause
**Stars**: 501 | **Forks**: 417
**Latest Release**: v1.3.7 (July 30, 2025)

**Why Recommended**:
- **Best automation** - automated citations via Manubot
- **Very actively maintained** - updated July 2025
- **Comprehensive documentation** - dedicated GitBook
- **Clean minimalist design** - functionality-focused
- **Modern features** - automatic PR previews

**Key Features**:
- Automated citation generation (DOI, PubMed, ORCID via Manubot)
- Team member pages with bios and photos
- Blog with tags
- Pre-built components (tables, code blocks, figures)
- Citation thumbnails
- GitHub tag imports
- Mobile-responsive
- Subtle animations (floating bubbles, fade-ins)

**Best For**: Labs wanting automated publication management

---

##### 3. Allan Lab Template

**Live Website**: https://www.allanlab.org/
**GitHub**: https://github.com/allanlab/allanlab
**Documentation**: https://www.allanlab.org/aboutwebsite.html
**License**: MIT

**Why Recommended**:
- **Simple, proven approach** - original template inspiring many derivatives
- **Easy for beginners** - straightforward structure
- **Real-world usage** - actual research lab website
- **No attribution required** (though appreciated)

**Key Features**:
- Bootstrap-based responsive design
- YAML data files for publications, news, team members
- Markdown for pages
- Liquid templating
- GitHub Pages compatible

**Best For**: Beginners wanting simple, customizable starting point

---

##### 4. Academic Website Template (Spencer Bryngelson)

**GitHub**: https://github.com/sbryngelson/academic-website-template
**License**: MIT
**Stars**: 315+ | **Forks**: 397+
**Latest Release**: v0.3.1 (June 9, 2024)

**Key Features**:
- Jekyll Scholar for automatic bibliography
- DOI/PDF/arXiv/BIB/Abstract buttons
- Dropdown bibliography abstracts
- Font Awesome icons
- Dark theme (Bootswatch)
- 70+ real academic implementations

**Best For**: Academic sites wanting dark theme and sophisticated bibliography

---

##### 5. Petridish - Research Project Focused

**Live Demo**: https://peterdesmet.com/petridish/
**GitHub**: https://github.com/peterdesmet/petridish
**License**: MIT
**Stars**: 56 | **Forks**: 45
**Latest Release**: v3.1 (January 2025)

**Key Features**:
- Bootstrap 5 modern framework
- GitHub Pages optimized
- Comprehensive documentation
- Minimal dependencies (90.4% SCSS)

**Best For**: Research projects and lab websites

---

##### 6. UW SAMPA Research Group Template

**Live Example**: http://sampa.cs.washington.edu/
**GitHub**: https://github.com/uwsampa/research-group-web
**License**: CC BY-NC 4.0

**Key Features**:
- BibTeX-generated publication lists
- Personnel directory (professors, students, staff, alumni)
- News feed and blog
- Bootstrap responsive design

**Note**: Non-commercial license restriction

---

#### OTHER APPROACHES

##### Stanford ML Group - Custom Static Site

**Live Site**: https://stanfordmlgroup.github.io/
**GitHub**: https://github.com/stanfordmlgroup/stanfordmlgroup.github.io
**License**: MIT
**Stars**: 97 | **Forks**: 41

**Why Noteworthy**:
- **Exactly what you liked** - clean Stanford ML Group design
- **Completely open source** - full source code available
- **Simple technology** - Gulp + Pug static site
- **Base template available** - Start Bootstrap "New Age" template
- **MIT licensed** - free to use and modify

**Technical Stack**:
- Pug templates (12% of codebase)
- Gulp 3.9.1 build system
- Bootstrap CSS framework
- Start Bootstrap "New Age" base

**How to Use**:
```bash
git clone https://github.com/stanfordmlgroup/stanfordmlgroup.github.io.git
npm install -g gulp
npm install
gulp  # Build and run
```

**Best For**: Teams wanting to replicate exact Stanford ML Group design

---

### Template Comparison Table

| Template | Platform | Design Style | Maintenance | License | Best Feature |
|----------|----------|--------------|-------------|---------|--------------|
| **Michaillat** | Hugo | Ultra-minimalist | 2024 | MIT | Cleanest design |
| **al-folio** | Jekyll | Academic elegant | Very active | MIT | Most features |
| **Greene Lab** | Jekyll | Clean functional | Very active | BSD-3 | Automated citations |
| **Hugo Blox** | Hugo | Modern professional | Very active | MIT | Comprehensive |
| **Stanford ML** | Custom | Clean professional | Stable | MIT | Proven design |
| **Allan Lab** | Jekyll | Simple traditional | Stable | MIT | Beginner-friendly |

---

### Quick Decision Guide for Free Templates

**Choose Michaillat's Hugo Template if**:
- You want the cleanest, most minimalist design
- Performance is critical
- You prefer Hugo's speed

**Choose al-folio if**:
- You want all features included
- Large community support matters
- You prefer Jekyll

**Choose Greene Lab Template if**:
- Automated citations are priority
- You want excellent documentation
- Modern features are important

**Choose Stanford ML Group approach if**:
- You want their exact design
- Simple custom build is acceptable
- You liked their specific aesthetic

**Choose Hugo Blox if**:
- You want comprehensive out-of-the-box solution
- No-code builder appeals to you
- Academic features are priority

---

## Part 2: Design Examples - Modern Academic Websites

### Category 1: Academic Lab Websites (Custom-Designed)

#### Featured Modern Lab Sites

1. **Bhamla Lab** - https://bhamla.gatech.edu/
   - **Platform**: Squarespace
   - **Design**: Modern minimalist with green and orange accents, full-width hero sections, visual-first navigation with large image galleries
   - **Focus**: Biophysics research with emphasis on visual storytelling

2. **Campbell-Staton Group** - https://www.campbellstaton.com/
   - **Platform**: Squarespace
   - **Design**: Clean typography, generous whitespace, teal/turquoise accents, high-quality photography, inspired by comic books, street art, and Afro-futurism
   - **Focus**: Evolutionary biology in the Anthropocene

3. **Yeşilbaş Lab** - https://www.yesilbaslab.com/
   - **Platform**: Squarespace
   - **Design**: Modern scientific aesthetic with custom animations, sophisticated color scheme, animated GIFs for concepts
   - **Focus**: Martian water and astrobiology

4. **The Birds & The Trees** - https://www.thebirdsthetrees.com/
   - **Platform**: Squarespace
   - **Design**: Nature-focused color palette (greens, earth tones), high-quality imagery, clear mission-driven layout
   - **Focus**: Urban biodiversity conservation

5. **Barrett Lab** - https://www.meghan-barrett.com/
   - **Platform**: Squarespace
   - **Design**: Modern minimalist, neutral tones with dark accents, high-quality insect photography, grid-based responsive layout
   - **Tagline**: "Boldly empirical. Radically compassionate"

6. **Karen Sears Lab** - https://www.searslab.eeb.ucla.edu/
   - **Focus**: Evolutionary developmental biology

7. **Crowther Lab** - https://crowtherlab.com/
   - **Platform**: WordPress with Divi theme
   - **Design**: Clean modern aesthetic, blue (#2EA3F2) accents on white, responsive grid system, strong social media integration
   - **Focus**: Environmental science

8. **Lab to Land Institute** - https://www.labtoland.institute/
   - **Platform**: Wix
   - **Design**: Modern responsive design with grid-based layouts, rich typography

---

### Category 2: GitHub-Hosted Research Group Sites

9. **SLED Lab** (University of Michigan) - https://sled.eecs.umich.edu/
   - Modern static site generators

10. **Sky-Lab** (UW-Madison) - https://sky-lab-uw.github.io/
    - **Design**: "A simple, whitespace theme for academics" based on folio design

11. **DxD Lab** (KAIST) - https://dxd-lab.github.io/
    - **Focus**: Human-computer interaction in industrial design

12. **Cairn's Lab** - https://cairns-lab.github.io/
    - **Design**: Modern research group exploring science and technology

13. **LEEClab** - https://leeclab.github.io/
    - Uses Wowchemy's Research Group Template for Hugo

14. **Stanford Machine Learning Group** - https://stanfordmlgroup.github.io/
    - **Design**: Clean navigation with anchor links, projects gallery
    - **Led by**: Professor Andrew Ng

15. **Stanford Vision and Learning Lab (SVL)** - https://svl.stanford.edu/
    - **Design**: Modern build process, carousel/grid for research initiatives

16. **James Zou's Machine Learning Lab** - https://www.james-zou.com/
    - **Focus**: Reliable, human-compatible machine learning

17. **MIT Software Design Group** - https://sdg.csail.mit.edu/
    - **Platform**: WordPress with custom Twenty Twenty-Five MIT theme
    - **Design**: Minimal aesthetic with MIT red (#a31f34) accents, Inter font family, generous spacing

---

### Category 3: Biotech Startup Websites (Design Inspiration)

18. **Benchling** - https://benchling.com
    - **Design**: Polished, futuristic with clean white and blue color scheme, modern typography, interactive animations

19. **Ginkgo Bioworks** - https://ginkgo.bio
    - **Design**: Vibrant with white background and black accents, modular layout, dynamic animations

20. **Beam Therapeutics** - https://beamtx.com
    - **Design**: Teal accents, interactive team cards with hover effects

21. **Asimov** - https://asimov.com
    - **Design**: Minimalist typography, full-width layouts, blue-purple tones

22. **Antiverse** - https://antiverse.io
    - **Design**: Modular layout, hover animations, green highlights

23. **Wild Bio** - https://wildbio.tech
    - **Design**: Nature-inspired aesthetic, black-and-white design

24. **BioAge Labs** - https://bioagelabs.com
    - **Design**: Purple background, minimalist typography

25. **Illumina** - https://illumina.com
    - **Design**: Dynamic headers, structured navigation

---

### Category 4: AI/ML Website Design Inspiration

26. **Scale** - Dark mode with 3D abstract shapes, glass elements, duo-tone images

27. **ZenML** - Bright graphics with icons, pastel colors in flat design

28. **OpenAI** - Abstract with pastel AI art, minimalist fonts, muted gray background

29. **Deepgram** - Product-focused with animated demonstrations

30. **HeyGen** - Large text headings, video-heavy with animation, bright colors and gradients

31. **Cohere** - Abstract graphics with moving backgrounds, pastel colors

32. **Baseten** - Simple illustrations with subtle animations

---

## Design Trends for 2024-2025

### Key Characteristics of Modern Academic Sites

1. **Minimalism & White Space** - Clean layouts that let content breathe
2. **Bold Typography** - Large, impactful headings with readable body text
3. **High-Quality Imagery** - Professional photography and custom illustrations
4. **Dark Mode Options** - Especially popular in AI/ML communities
5. **Interactive Elements** - Animations, hover effects, dynamic content
6. **Mobile-First Design** - Responsive across all devices
7. **Custom Illustrations & Icons** - Unique branded elements
8. **Video Integration** - Product demos and research showcases
9. **Storytelling Approach** - Narrative-driven content presentation
10. **Modular Layouts** - Grid-based, flexible content blocks

### Popular Platforms Among Featured Sites

- **Squarespace** - Most popular among custom academic labs (Bhamla, Campbell-Staton, Yeşilbaş, Barrett, Birds & Trees)
- **WordPress** - With custom themes (Crowther Lab uses Divi)
- **Static Site Generators** - Hugo, Jekyll, Gatsby for GitHub-hosted sites
- **Wix** - Modern responsive capabilities
- **Custom Modern Frameworks** - React, Next.js for tech-forward groups

---

## Open Source Templates & Resources

### Website Templates

1. **Greene Lab Website Template** - https://greenelab.github.io/lab-website-template/
   - GitHub: https://github.com/greenelab/lab-website-template
   - Features: Automatic citations, GitHub tag imports, pre-built components

2. **UW SAMPA Research Group Template** - https://github.com/uwsampa/research-group-web
   - Jekyll-based, Bootstrap framework, BibTeX management
   - Example: sampa.cs.washington.edu

3. **Academic Website Template** - https://github.com/sbryngelson/academic-website-template
   - Jekyll/Liquid/Bootstrap for academics

4. **Academic Responsive Template** - https://github.com/dmsl/academic-responsive-template

5. **Research Lab Website** - https://github.com/photonlines/Research-Lab-Website
   - Simple static research lab template

### Design Showcase Platforms

- **Awwwards** - https://www.awwwards.com/ - Premier website design awards
- **CSS Design Awards** - https://www.cssdesignawards.com/ - CSS innovation recognition
- **Siteinspire** - https://www.siteinspire.com/ - Curated complete website experiences
- **Minimal Gallery** - https://minimal.gallery/ - Minimalist design curation
- **Admire The Web** - More selective than Awwwards

### Educational Resources

- **Impact Media Lab: 8 Best Academic Lab Websites** - https://www.impactmedialab.com/scicomm/8-best-academic-lab-websites-to-inspire-your-lab-site
- **Thomas Digital: 40 Best Lab Websites** - https://thomasdigital.com/industry/lab-website-design
- **Samuel Crane: Great Lab Websites** - https://www.samuelcrane.com/post/great-lab-websites/
- **22 AI Websites for Design Inspiration** - https://motiontactic.com/blog/22-ai-websites-for-design-inspiration-in-2024/
- **14 Best Biotech Website Design Examples** - https://www.webstacks.com/blog/biotech-website-design

---

## Part 3: GitLab Pages Implementation

### Key GitLab Pages Features

**Official Documentation**: https://docs.gitlab.com/user/project/pages/

- **Supports any static site generator** - no restrictions
- **Free SSL/TLS certificates** via Let's Encrypt
- **Custom domains**: Up to 150 per site
- **CI/CD integration**: Seamless deployment via GitLab pipelines
- **Access control**: Public or restricted to project members
- **Maximum site size**: 1 GB on GitLab.com
- **Automatic HTTPS**: For .gitlab.io domains

### Modern Deployment Configuration (2025)

```yaml
default:
  image: ruby:3.2

workflow:
  rules:
    - if: $CI_COMMIT_BRANCH

create-pages:
  stage: deploy
  script:
    - gem install bundler
    - bundle install
    - bundle exec jekyll build -d public
  pages: true
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  environment: production
```

### Hugo-Specific Configuration

**Source**: https://gohugo.io/hosting-and-deployment/hosting-on-gitlab/

```yaml
default:
  image: golang:1.25.3-bookworm

variables:
  HUGO_VERSION: 0.152.2
  DART_SASS_VERSION: 1.93.2

pages:
  script:
    - hugo --gc --minify
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Custom Domain Setup

**DNS Configuration for Root Domains**:
```
A Record:    35.185.44.232
AAAA Record: 2600:1901:0:7b8a::
TXT Record:  gitlab-pages-verification-code=[your-code]
```

**For Subdomains**:
```
CNAME Record: namespace.gitlab.io
TXT Record:   _gitlab-pages-verification-code.subdomain
```

**SSL/TLS**: Automatic via Let's Encrypt (recommended)

### Performance Optimization

**Caching Configuration**:
```yaml
cache:
  paths:
    - vendor/
    - node_modules/
    - .npm/
```

**Media Optimization**:
```yaml
variables:
  FF_USE_FASTZIP: "true"
  ARTIFACT_COMPRESSION_LEVEL: "fastest"
```

### Limitations

- **Static-only hosting**: No server-side processing (PHP, ASP, etc.)
- **Storage limit**: 1 GB maximum on GitLab.com
- **Rate limiting**: 1,000 requests per IP every 50 seconds
- **No built-in CDN**: Unlike Netlify (though GitLab.com uses CloudFlare)
- **No serverless functions**: Cannot run backend code
- **Redirect limit**: 1,000 redirects maximum

### GitLab Pages vs Alternatives

| Feature | GitLab Pages | GitHub Pages | Netlify |
|---------|--------------|--------------|---------|
| **Integration** | Seamless GitLab | Tight GitHub | Any Git provider |
| **Custom Domains** | 150 per site | 1 per site | Multiple |
| **Pricing** | Free | Free (public) | Free tier + paid |
| **Serverless Functions** | No | No | Yes |
| **Form Handling** | No | No | Yes |
| **Rollbacks** | Git revert | Git revert | One-click |
| **DNS Management** | External | External | Built-in |

---

## Code References

- Hugo GitLab CI example: https://gitlab.com/pages/hugo
- Jekyll GitLab CI example: https://gitlab.com/pages/jekyll
- Astro GitLab CI example: https://gitlab.com/pages/astro

## Related Research

This research document should be supplemented with:
- Specific theme selection for chosen SSG
- Content migration strategy (if moving from existing site)
- Team training plan for chosen platform
- Custom domain acquisition and DNS configuration
- Analytics and tracking implementation plan

## Open Questions

1. What is the preferred SSG based on team technical skills?
2. Is there an existing domain, or does one need to be purchased?
3. What is the expected site size (number of publications, team members)?
4. Are there specific design preferences (color schemes, layouts)?
5. What content management workflow is preferred (direct Git commits vs. web-based CMS)?
6. Are there accessibility requirements (WCAG compliance)?
7. What analytics platform should be integrated (Google Analytics, Plausible, etc.)?

## Key Takeaways

### For Static Site Generators:
- **Hugo with Hugo Blox** is the clear winner for physics groups needing out-of-the-box academic features
- All four generators work excellently with GitLab Pages
- Build speed differences become significant for large sites (1000+ pages)
- LaTeX/math support is excellent across all major SSGs

### For Design Inspiration:
- Modern academic sites favor custom designs over institutional templates
- **Squarespace** is surprisingly popular among independent research labs
- **Minimalism** and **visual storytelling** are dominant trends
- GitHub-hosted sites using Hugo/Jekyll can achieve professional results
- Biotech startups offer excellent design inspiration with modern aesthetics

### Final Recommendation: Greene Lab Template for GitLab Pages

After comprehensive analysis considering BibTeX citation management, ease of maintenance, design flexibility, and GitLab Pages compatibility, **Greene Lab Website Template emerges as the optimal choice** for a theoretical physics group website.

---

## Why Greene Lab Template?

**Live Demo**: https://greenelab.github.io/lab-website-template/
**GitHub**: https://github.com/greenelab/lab-website-template
**Documentation**: https://greene-lab.gitbook.io/lab-website-template-docs

### Key Advantages:

1. **Automated Citation Management via Manubot**
   - Paste DOIs, PubMed IDs, or ORCID IDs
   - Automatic metadata fetching
   - No manual BibTeX maintenance
   - Citation thumbnails and formatting

2. **Researcher-Friendly Design**
   - Clean, minimalist, functional aesthetic
   - Built by scientists for scientists
   - Dedicated GitBook documentation
   - Pre-built components for common needs

3. **Simple Content Management**
   - YAML files for all content (team, projects, citations)
   - Markdown for pages
   - No complex CLI tools required
   - Straightforward customization

4. **Active Maintenance**
   - Updated July 2025 (v1.3.7)
   - 501 stars, 417 forks
   - 20 contributors
   - Used by multiple research labs

5. **100% Free and Open Source**
   - BSD-3-Clause license
   - No premium tiers
   - No paid features
   - Complete functionality included

---

## Greene Lab on GitLab Pages: Detailed Implementation Guide

### Understanding the GitLab Pages Limitation

**The Challenge:**

Greene Lab Template is **designed for GitHub Pages** with GitHub Actions for automation. The primary difference when using GitLab Pages is **Manubot citation automation**.

**On GitHub Pages (default setup):**
1. Add DOI to `_data/citations.yaml`
2. Push to GitHub
3. GitHub Actions automatically runs Manubot
4. Manubot fetches citation metadata
5. Site rebuilds with complete citations
6. **Fully automated, zero manual work**

**On GitLab Pages:**
- GitLab doesn't have Greene Lab's pre-configured GitHub Actions
- Manubot citation fetching needs manual setup
- **Three solutions available** (detailed below)

---

## Solution 1: Manual Local Manubot (Recommended - Simplest)

### Overview
Run Manubot on your local machine before pushing to GitLab. This is the **simplest and most reliable approach**.

### One-Time Setup

**Install Manubot:**
```bash
# Using npm (recommended)
npm install --global manubot

# Or using Python pip
pip3 install manubot
```

**Verify installation:**
```bash
manubot --version
```

### Workflow for Adding Publications

**Step-by-step process:**

```bash
# 1. Add citation to YAML file
vim _data/citations.yaml

# Add new entry (just the identifier):
- id: doi:10.1371/journal.pcbi.1007128
  # That's all! Manubot fetches the rest

# 2. Run Manubot locally to fetch metadata
manubot process --content-directory=.

# This creates/updates _data/citations-output.yaml with full citation data

# 3. Commit and push to GitLab
git add _data/citations.yaml _data/citations-output.yaml
git commit -m "Add new publication on quantum field theory"
git push origin main

# 4. GitLab CI/CD builds site with complete citations
# (No Manubot needed in CI - just standard Jekyll build)
```

### GitLab CI/CD Configuration

**`.gitlab-ci.yml` (simple Jekyll build):**
```yaml
image: ruby:3.2

pages:
  stage: deploy
  before_script:
    - gem install bundler
    - bundle install
  script:
    - bundle exec jekyll build -d public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Time Investment

**Per publication addition:**
- Edit YAML: 30 seconds
- Run Manubot: 5-10 seconds
- Commit and push: 30 seconds
- **Total: ~1-2 minutes**

**Comparison:**
- al-folio with BibTeX: Edit .bib, push (~1 minute)
- Hugo Blox with CLI: Edit .bib, run import, push (~2 minutes)
- **Greene Lab with Manubot: Competitive, with better automation**

### Advantages of This Approach

✅ **Simple setup** - no complex CI/CD configuration
✅ **Reliable** - you control when Manubot runs
✅ **Fast** - Manubot runs locally (not waiting for CI)
✅ **Debuggable** - see Manubot output immediately
✅ **Works offline** - can prepare citations without internet (push later)
✅ **No CI time** - GitLab CI just builds Jekyll (faster)

### Disadvantages

⚠️ **Manual step** - remember to run Manubot before pushing
⚠️ **Requires local setup** - need npm/Python on your machine
⚠️ **Not fully automated** - GitHub Pages approach is more automatic

### Making it Easier: Shell Alias

**Add to `.bashrc` or `.zshrc`:**
```bash
# Alias for Greene Lab publication workflow
alias add-pub='manubot process --content-directory=. && git add _data/'

# Usage:
# 1. Edit _data/citations.yaml
# 2. Run: add-pub
# 3. git commit -m "..." && git push
```

---

## Solution 2: Automated Manubot in GitLab CI/CD

### Overview
Configure GitLab CI/CD to run Manubot automatically, replicating GitHub Actions behavior.

### GitLab CI/CD Configuration

**`.gitlab-ci.yml` (with Manubot automation):**
```yaml
image: node:lts

variables:
  BUNDLE_PATH: vendor/bundle

cache:
  paths:
    - vendor/bundle
    - node_modules/

before_script:
  # Install Ruby and Bundler
  - apt-get update -qq
  - apt-get install -y ruby-full build-essential
  - gem install bundler
  - bundle install --jobs $(nproc)
  # Install Manubot
  - npm install --global manubot

stages:
  - build
  - deploy

# Run Manubot to fetch citations
process_citations:
  stage: build
  script:
    - manubot process --content-directory=.
  artifacts:
    paths:
      - _data/citations-output.yaml
    expire_in: 1 hour
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# Build and deploy site
pages:
  stage: deploy
  dependencies:
    - process_citations
  script:
    - bundle exec jekyll build -d public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Workflow for Adding Publications

**Simplified workflow:**
```bash
# 1. Add citation to YAML file
vim _data/citations.yaml

- id: doi:10.1371/journal.pcbi.1007128

# 2. Commit and push
git add _data/citations.yaml
git commit -m "Add new publication"
git push origin main

# 3. GitLab CI/CD automatically:
#    - Runs Manubot to fetch metadata
#    - Builds Jekyll site
#    - Deploys to GitLab Pages
```

**Just like GitHub Pages!** Fully automated.

### Advantages

✅ **Fully automated** - no manual Manubot runs
✅ **GitHub-like workflow** - just push DOIs
✅ **No local setup** - Manubot runs in CI
✅ **Easier for collaborators** - they just edit YAML

### Disadvantages

⚠️ **Complex CI/CD config** - more moving parts
⚠️ **Longer CI time** - Manubot adds ~30-60 seconds to build
⚠️ **Harder to debug** - Manubot errors happen in CI
⚠️ **Internet-dependent** - CI must fetch citations
⚠️ **Uses CI minutes** - (free tier: 400 minutes/month on GitLab.com)

### When to Use This Approach

**Choose automated CI/CD Manubot if:**
- Multiple collaborators contributing
- You want zero local setup
- You prioritize convenience over CI complexity
- You're comfortable debugging CI/CD issues

---

## Solution 3: Manual Citations (No Manubot)

### Overview
Skip Manubot entirely and manually enter citation data. Still uses Greene Lab's template and design.

### Configuration

**Modify `_data/citations.yaml` structure:**
```yaml
# Manual entry (no Manubot)
- id: custom-2024-quantum
  title: "Quantum Field Theory in Curved Spacetime"
  authors:
    - John Doe
    - Jane Smith
  publisher: Physical Review D
  date: 2024-03-15
  link: https://doi.org/10.1103/PhysRevD.109.064023
  image: images/publications/quantum-2024.png
  description: |
    We investigate quantum field theory in curved spacetime
    and derive new results for black hole thermodynamics.
  tags:
    - quantum field theory
    - general relativity
    - black holes
  buttons:
    - type: paper
      link: https://arxiv.org/abs/2403.12345
    - type: pdf
      link: papers/doe-2024-quantum.pdf
```

### Workflow

```bash
# 1. Manually enter citation details
vim _data/citations.yaml

# 2. Commit and push
git add _data/citations.yaml
git commit -m "Add new publication"
git push origin main

# 3. GitLab builds site (no Manubot needed)
```

### GitLab CI/CD Configuration

**`.gitlab-ci.yml` (simplest possible):**
```yaml
image: ruby:3.2

pages:
  script:
    - gem install bundler
    - bundle install
    - bundle exec jekyll build -d public
  artifacts:
    paths:
      - public
  only:
    - main
```

### Advantages

✅ **Simplest CI/CD** - just Jekyll, no Manubot
✅ **No dependencies** - no npm/Python needed
✅ **Full control** - customize citation display exactly
✅ **No external dependencies** - no DOI fetching failures
✅ **Fastest CI** - no Manubot processing time

### Disadvantages

⚠️ **Most manual work** - type all citation details
⚠️ **Error-prone** - manual entry = typos possible
⚠️ **No automation** - loses Manubot's main benefit
⚠️ **More maintenance** - updating citations requires manual edits

### When to Use This Approach

**Choose manual citations if:**
- Small number of publications (~10-20)
- You want absolute simplicity in CI/CD
- You have custom citation requirements
- You prefer full manual control

---

## Comparison: Three Manubot Solutions

| Aspect | Manual Local | Automated CI/CD | Manual Citations |
|--------|--------------|-----------------|------------------|
| **Setup Complexity** | ⭐⭐⭐⭐ (npm install) | ⭐⭐⭐ (CI config) | ⭐⭐⭐⭐⭐ (none) |
| **Workflow Simplicity** | ⭐⭐⭐⭐ (one command) | ⭐⭐⭐⭐⭐ (just push) | ⭐⭐⭐ (manual entry) |
| **CI/CD Complexity** | ⭐⭐⭐⭐⭐ (simple Jekyll) | ⭐⭐⭐ (Manubot + Jekyll) | ⭐⭐⭐⭐⭐ (simple Jekyll) |
| **Per-Publication Time** | ~1-2 min | ~1 min | ~3-5 min |
| **Automation** | Semi-automated | Fully automated | Manual |
| **Debugging** | ⭐⭐⭐⭐⭐ (local) | ⭐⭐⭐ (CI logs) | ⭐⭐⭐⭐⭐ (no automation) |
| **Collaborator-Friendly** | ⭐⭐⭐ (need setup) | ⭐⭐⭐⭐⭐ (just git) | ⭐⭐⭐⭐ (just YAML) |
| **Reliability** | ⭐⭐⭐⭐⭐ (you control) | ⭐⭐⭐⭐ (CI-dependent) | ⭐⭐⭐⭐⭐ (no external deps) |
| **Best For** | Solo/small teams | Multiple collaborators | Very small labs |

---

## Recommended Approach: Manual Local Manubot

**For most physics groups, Solution 1 (Manual Local Manubot) is optimal because:**

1. ✅ **Balance of automation and simplicity**
   - Still gets Manubot benefits (auto-fetch metadata)
   - Simpler CI/CD than automated approach
   - More reliable than depending on CI

2. ✅ **Easy to debug**
   - See Manubot output immediately
   - Fix issues locally before pushing
   - No waiting for CI to fail/succeed

3. ✅ **Fast iteration**
   - Test citation formatting locally
   - Preview with `bundle exec jekyll serve`
   - Push only when ready

4. ✅ **Low maintenance**
   - Simple GitLab CI (just Jekyll)
   - Fewer moving parts to break
   - Standard Jekyll deployment

5. ✅ **Still better than alternatives**
   - Easier than maintaining .bib files (Hugo Blox)
   - Better automation than jekyll-scholar
   - More structured than manual entry

### Quick Start Guide

**1. Initial Setup (one-time, ~10 minutes):**
```bash
# Fork Greene Lab template
# Clone to your machine
git clone https://gitlab.com/yourgroup/yoursite.git
cd yoursite

# Install Manubot
npm install --global manubot

# Install Jekyll dependencies
bundle install

# Test locally
bundle exec jekyll serve
# Visit http://localhost:4000
```

**2. Add Your First Publication:**
```bash
# Edit citations file
vim _data/citations.yaml

# Add:
- id: doi:10.1103/PhysRevD.109.064023

# Process with Manubot
manubot process --content-directory=.

# Preview locally
bundle exec jekyll serve

# Commit and deploy
git add _data/
git commit -m "Add first publication"
git push origin main
```

**3. Future Additions (ongoing, ~2 minutes each):**
```bash
# Add DOI to citations.yaml
# Run: manubot process --content-directory=.
# Commit and push
```

---

## Greene Lab Customization for Physics Groups

### Brand Customization

**Change colors (`_styles/variables.scss`):**
```scss
// Replace Greene Lab's blue with your colors
$primary: #8B0000;      // Dark red (theoretical physics theme)
$accent: #DAA520;       // Gold
$background: #FFFFFF;

// Fonts
$font-heading: "Computer Modern Serif", serif;  // LaTeX-like
$font-body: "Source Sans Pro", sans-serif;
```

**Update site info (`_config.yaml`):**
```yaml
title: Your Lab Name
tagline: Theoretical Physics Research Group
description: Quantum field theory and gravitational physics
baseurl: ""
url: https://yourlab.gitlab.io

# Contact info
email: contact@yourlab.org
twitter: yourlab
github: yourlab
```

### Content Customization

**Team members (`_data/members.yaml`):**
```yaml
- name: Prof. Jane Doe
  image: images/team/jane-doe.jpg
  role: pi
  affiliation: Your University
  description: Quantum field theory in curved spacetime
  links:
    home-page: https://jane-doe.com
    email: jane@university.edu
    orcid: 0000-0002-1234-5678
    google-scholar: abc123xyz

- name: Dr. John Smith
  role: postdoc
  description: Black hole thermodynamics
  links:
    email: john@university.edu
```

**Projects (`_data/projects.yaml`):**
```yaml
- title: Quantum Field Theory in Curved Spacetime
  image: images/projects/qft-curved.jpg
  description: |
    We develop new techniques for studying quantum fields
    in curved spacetime backgrounds.
  links:
    website: https://project-site.org
  tags:
    - quantum field theory
    - general relativity
```

### Adding Physics-Specific Features

**LaTeX math support (already included in Greene Lab):**
```markdown
---
title: Research
---

Our work focuses on the Wheeler-DeWitt equation:

$$\hat{H} | \Psi \rangle = 0$$

We study quantum gravitational effects in black hole backgrounds.
```

**Add arXiv links to citations:**
```yaml
- id: doi:10.1103/PhysRevD.109.064023
  buttons:
    - type: preprint
      text: arXiv
      link: https://arxiv.org/abs/2403.12345
```

---

## Migration Path from Other Templates

### If Currently Using al-folio

**Citation migration:**
```bash
# Export BibTeX from al-folio
# Convert to Manubot format (DOI extraction script)

# Simple Python script:
import bibtexparser

with open('_bibliography/papers.bib') as f:
    bib = bibtexparser.load(f)

for entry in bib.entries:
    if 'doi' in entry:
        print(f"- id: doi:{entry['doi']}")
```

### If Currently Using Hugo Blox

**Content migration:**
- Team members: Hugo Blox author files → Greene Lab YAML
- Publications: BibTeX → Manubot DOIs
- Projects: Hugo page bundles → Greene Lab YAML

**Automated migration script available in Greene Lab docs.**

---

## Long-Term Maintenance Considerations

### Regular Tasks

**Weekly/Monthly (adding publications):**
- Time: 2 minutes per publication
- Frequency: As papers published
- Skill: Basic (edit YAML, run command)

**Quarterly (updates):**
- Update Ruby gems: `bundle update`
- Update Manubot: `npm update -g manubot`
- Time: 5 minutes

**Yearly (major updates):**
- Review Greene Lab template updates
- Merge upstream changes if desired
- Update Jekyll version if needed
- Time: 1-2 hours

### Team Training

**Onboarding new lab members:**
1. Clone repository
2. Install Manubot (5 minutes)
3. Learn YAML editing (10 minutes)
4. Practice adding citation (5 minutes)
5. **Total: 20 minutes**

Much easier than learning Hugo, BibTeX management, or complex CI/CD.

---

## Addressing Common Concerns

### "Is manual Manubot really better than automated al-folio BibTeX?"

**Comparison:**

**al-folio (jekyll-scholar):**
- Edit `.bib` file (must know BibTeX syntax)
- Maintain correct formatting
- Handle special characters, escaping
- Debug BibTeX parsing errors
- Push

**Greene Lab (manual Manubot):**
- Add DOI to YAML (simple identifier)
- Run `manubot process`
- Manubot handles all formatting
- Push

**Both are ~1-2 minutes.** Greene Lab is arguably easier because:
- No BibTeX syntax knowledge needed
- Just paste DOI (copy from journal website)
- Manubot handles all formatting automatically
- Fewer things to go wrong

### "Should I use automated CI/CD Manubot instead?"

**Use automated CI/CD if:**
- ✅ 3+ regular contributors
- ✅ You're comfortable with CI/CD debugging
- ✅ Convenience > simplicity

**Use manual local Manubot if:**
- ✅ Solo or 2-person team
- ✅ You prefer simpler CI/CD
- ✅ You want local preview before pushing
- ✅ Reliability > convenience

**For most small academic groups: manual local is better.**

---

## Implementation Timeline

### Week 1: Setup
- Fork Greene Lab template
- Install Manubot locally
- Configure GitLab Pages CI/CD
- Customize colors/branding
- **Time: 4-6 hours**

### Week 2: Content
- Add team members
- Add existing publications (bulk Manubot)
- Create project pages
- Write about section
- **Time: 6-8 hours**

### Week 3: Polish
- Customize styling
- Add images
- Test on mobile
- Configure custom domain
- **Time: 4-6 hours**

### Week 4: Launch
- Final review
- Soft launch to group
- Gather feedback
- Make adjustments
- Public launch
- **Time: 2-4 hours**

**Total: 16-24 hours spread over 4 weeks**

---

## Final Implementation Strategy

**Recommended approach for theoretical physics group:**

1. **Choose Greene Lab Template**
   - Best automation (Manubot)
   - Clean, functional design
   - Researcher-friendly
   - Active maintenance

2. **Use Manual Local Manubot**
   - Simple CI/CD setup
   - Reliable workflow
   - Easy to debug
   - Fast iteration

3. **Deploy to GitLab Pages**
   - Free hosting
   - Custom domain support
   - SSL certificates
   - Integrated CI/CD

4. **Customize Design**
   - Update colors/fonts
   - Add lab branding
   - Modify layouts as needed
   - Keep design clean

5. **Maintain Regularly**
   - Add publications as published
   - Update team member info
   - Post news/blog updates
   - Keep dependencies updated

**This approach provides:**
- ✅ Excellent citation management (easier than BibTeX)
- ✅ Clean, professional design
- ✅ Simple maintenance
- ✅ GitLab Pages compatibility
- ✅ Long-term sustainability
- ✅ Researcher-friendly workflow

---

## Additional Resources

### Static Site Generator Resources
- **Hugo Documentation**: https://gohugo.io/documentation/
- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **Astro Documentation**: https://docs.astro.build/
- **Eleventy Documentation**: https://www.11ty.dev/docs/

### GitLab Pages Resources
- **GitLab Pages Main Docs**: https://docs.gitlab.com/user/project/pages/
- **GitLab CI/CD Docs**: https://docs.gitlab.com/ci/
- **Custom Domains and SSL**: https://docs.gitlab.com/user/project/pages/custom_domains_ssl_tls_certification/
- **Example Projects**: https://gitlab.com/pages

### Design Resources
- **Awwwards**: https://www.awwwards.com/
- **Siteinspire**: https://www.siteinspire.com/
- **CSS Design Awards**: https://www.cssdesignawards.com/
- **Minimal Gallery**: https://minimal.gallery/

### Math/LaTeX Support
- **MathJax**: https://www.mathjax.org/
- **KaTeX**: https://katex.org/
- **remark-math** (Astro/MDX): https://github.com/remarkjs/remark-math
