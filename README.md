# Static Site Generator

A Python-based static site generator that converts Markdown content into a fully 
functional website. Built as part of the Boot.dev backend development course.

## Features

- Markdown to HTML conversion: Transforms Markdown files into styled HTML pages
- Static file copying: Automatically copies CSS, images, and other static assets
- Template system: Uses a single HTML template for consistent page layout
- GitHub Pages deployment: Built-in support for GitHub Pages hosting
- Configurable base paths: Supports deployment to subdirectories

## Usage

### Local Development

Run the generator for local testing:

```python3 src/main.py```

This builds the site with a base path of `/` and outputs to the `docs/` directory.

### Production Build

For GitHub Pages deployment:

```./build.sh```

Make sure to update the `REPO_NAME` in `build.sh` to match your GitHub repository name.

### Content Creation

1. Add Markdown files to the content/ directory
2. Use nested folders to create URL paths (e.g., content/blog/post1/index.md becomes /blog/post1/)
3. Place static assets in the static/ directory

## Deployment

This project is configured for GitHub Pages deployment:

1. Push your code to GitHub
2. Enable GitHub Pages in repository settings
3. Set source to main branch and docs/ folder
4. Your site will be available at https://USERNAME.github.io/REPO_NAME/

## Testing

The project includes comprehensive unit tests:

```python3 -m unittest discover src/```

## Dependencies

- Python 3.x
- No external dependencies required (uses only standard library)

## License

This project was created as part of the Boot.dev backend development curriculum.

