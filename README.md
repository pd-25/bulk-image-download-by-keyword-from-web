# Image Download Scraper

A small Python project for searching Bing Images by keywords and downloading the first available image result for each keyword.

## What it does

- uses `requests` to query Bing Images search results
- parses image URLs from the returned HTML
- downloads image content and saves it locally
- chooses file extensions based on HTTP `Content-Type` or URL suffix
- creates a `downloaded_images/` folder automatically

## Project structure

- `main.py` - main script with all search and download logic
- `requirements.txt` - list of Python dependencies
- `static/` - existing folder with category image collections (not directly used by `main.py`)
- `virtualenv/` - local Python virtual environment

## Requirements

- Python 3
- `requests`

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Usage

1. Open `main.py`
2. Add keywords to the `keywords` list near the bottom of the file
3. Run the script:

```bash
python main.py
```

4. Downloaded images are saved to `downloaded_images/`

## Notes

- This project scrapes Bing search results HTML and may break if Bing changes its page structure.
- The script currently downloads one image per keyword.
- If the returned content is not an image, the script skips that URL and tries the next one.

## Example

```python
keywords = [
    "organic vegetables",
    "sustainable fashion",
    "eco friendly packaging",
]
```

## License

This repository does not include a license file. Add one if you want to make the project reusable by others.
