# How to Run the Website Locally

This document explains how to run the chireal group website locally for development and testing.

## Prerequisites

The following software is required:

- **Ruby 3.3+**: `/opt/homebrew/opt/ruby@3.3/bin/ruby`
- **Bundler**: Installed with Ruby
- **Manubot**: `/Users/aflorio/Library/Python/3.9/bin/manubot` (for citation management)

## Starting the Local Development Server

```bash
cd /Users/aflorio/Documents/GroupWebsite/site
/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll serve
```

The site will be available at: **http://localhost:4000**

Press `Ctrl+C` to stop the server.

## Building the Site (Without Server)

To build the site without starting a server:

```bash
cd /Users/aflorio/Documents/GroupWebsite/site
/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll build
```

The built site will be in the `_site/` directory.

## Installing/Updating Dependencies

If you need to install or update Ruby gems:

```bash
cd /Users/aflorio/Documents/GroupWebsite/site
/opt/homebrew/opt/ruby@3.3/bin/bundle install
```

## Using Manubot for Citations

To process citations and fetch metadata from DOIs:

```bash
cd /Users/aflorio/Documents/GroupWebsite/site
/Users/aflorio/Library/Python/3.9/bin/manubot process --content-directory=.
```

This reads DOIs from `_data/citations.yaml` and generates `_data/citations-output.yaml` with full metadata.

## Adding News to the Homepage Banner

The homepage displays a rotating news carousel with the latest announcements. To add a new news item:

1. Edit `_data/news.yaml`
2. Add a new entry **at the top** of the file (newest first):

```yaml
- date: 2025-11-25
  text: "Your announcement text here"
  link: "https://example.com"
```

**Fields:**
- `date` - Publication date in YYYY-MM-DD format
- `text` - The announcement text (keep under 100 characters for best display)
- `link` - Optional URL; external links automatically open in a new tab

The homepage (`index.md`) displays the 3 most recent items. After editing, rebuild the site to see changes.

**Maintenance tip:** Periodically remove news items older than 6 months to keep the carousel relevant.

## Template Modifications

**Note**: We removed the `jekyll-last-modified-at` plugin from the original Greene Lab template due to Ruby 3.3 compatibility issues. This plugin is non-essential (it auto-generates last-modified dates from git history).

**Added compatibility gems** for Ruby 3.3+:
- csv
- base64
- bigdecimal
- logger

## Troubleshooting

**If the server won't start:**
1. Make sure you're in the correct directory: `/Users/aflorio/Documents/GroupWebsite/site`
2. Check that Ruby 3.3 is being used: `/opt/homebrew/opt/ruby@3.3/bin/ruby --version`
3. Try cleaning and rebuilding: `/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll clean`

**If you see warnings about "Logger not initialized properly":**
- These are harmless warnings from Jekyll 4.3.2 with Ruby 3.3
- The site will build and run correctly despite these warnings

**Port already in use:**
If port 4000 is already in use, you can specify a different port:
```bash
/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll serve --port 4001
```

## Quick Reference

| Task | Command |
|------|---------|
| Start server | `/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll serve` |
| Build site | `/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll build` |
| Clean build | `/opt/homebrew/opt/ruby@3.3/bin/bundle exec jekyll clean` |
| Process citations | `/Users/aflorio/Library/Python/3.9/bin/manubot process --content-directory=.` |
| Update gems | `/opt/homebrew/opt/ruby@3.3/bin/bundle install` |

## GitHub Repository and Deployment

- **Repository**: https://github.com/aflorio2/chireal-site
- **Live Site**: https://aflorio.science

### Deployment Process

Every push to the `main` branch automatically triggers GitHub Actions, which:
1. Sets up Ruby 3.3 and Python 3.11
2. Processes citations using the Python cite script
3. Builds the Jekyll site
4. Deploys to GitHub Pages

You can monitor deployments at: https://github.com/aflorio2/chireal-site/actions
