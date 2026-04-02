import os
import re
import requests
import time
import json

def get_extension_from_content_type(content_type):
    """Get file extension from HTTP content-type header"""
    mapping = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/webp': '.webp',
        'image/gif': '.gif',
        'image/bmp': '.bmp',
        'image/svg+xml': '.svg',
    }
    if content_type:
        content_type = content_type.split(';')[0].strip().lower()
        return mapping.get(content_type, '.jpg')
    return '.jpg'

def get_extension_from_url(url):
    """Guess file extension from URL path"""
    url_lower = url.lower().split('?')[0]
    for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.svg']:
        if url_lower.endswith(ext):
            return ext if ext != '.jpeg' else '.jpg'
    return None

def download_image(url, base_filename, folder_path):
    """Download image from URL and save to local path with correct extension"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            # Check if it's actually an image
            if content_type and not content_type.startswith('image/'):
                print(f"  ⚠ Skipped (not an image): {content_type}")
                return None
            
            ext = get_extension_from_content_type(content_type)
            # Fallback: try to guess from URL
            if ext == '.jpg' and content_type == '':
                url_ext = get_extension_from_url(url)
                if url_ext:
                    ext = url_ext
            
            filename = base_filename + ext
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded: {filename} ({len(response.content) / 1024:.1f} KB)")
            return filename
        else:
            print(f"  ⚠ HTTP {response.status_code} for: {url[:60]}...")
            return None
    except Exception as e:
        print(f"  ⚠ Error: {str(e)[:80]}")
        return None

def search_bing_images(keyword, num_results=5):
    """Search Bing Images and return list of image URLs"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    search_url = f"https://www.bing.com/images/search?q={requests.utils.quote(keyword)}&form=HDRSC2&first=1"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"  ⚠ Bing search returned status {response.status_code}")
            return []
        
        html = response.text
        image_urls = []
        
        # Bing encodes image metadata as HTML entities in 'm' attributes
        # The real source URLs are in 'murl' fields: murl&quot;:&quot;https://...&quot;
        encoded_murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&', html)
        for url in encoded_murls[:num_results]:
            image_urls.append(url)
        
        # Fallback: try direct JSON pattern (some Bing versions)
        if not image_urls:
            direct_murls = re.findall(r'"murl":"(https?://[^"]+)"', html)
            for url in direct_murls[:num_results]:
                url = url.replace('\\/', '/')
                image_urls.append(url)
        
        return image_urls
    
    except Exception as e:
        print(f"  ⚠ Search error: {str(e)[:80]}")
        return []

def search_and_download_images(keywords, download_folder):
    """Search for each keyword using Bing and download one image per keyword"""
    
    # Create download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Created folder: {download_folder}")
    
    downloaded_images = []
    
    for i, keyword in enumerate(keywords):
        print(f"\n{'='*50}")
        print(f"[{i+1}/{len(keywords)}] Searching for: {keyword}")
        print(f"{'='*50}")
        
        # Search for image URLs
        image_urls = search_bing_images(keyword)
        
        if not image_urls:
            print(f"✗ No images found for: {keyword}")
            continue
        
        print(f"  Found {len(image_urls)} image(s), attempting download...")
        
        # Create base filename from keyword
        base_filename = keyword.lower().replace(' ', '_').replace('&', 'and').replace("'", "")
        
        # Try downloading from the results until one succeeds
        downloaded = False
        for url in image_urls:
            saved_filename = download_image(url, base_filename, download_folder)
            if saved_filename:
                downloaded_images.append(saved_filename)
                downloaded = True
                break
        
        if not downloaded:
            print(f"✗ Could not download any image for: {keyword}")
        
        # Small delay between searches to be polite
        if i < len(keywords) - 1:
            time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"Download Summary:")
    print(f"Total keywords: {len(keywords)}")
    print(f"Successfully downloaded: {len(downloaded_images)}")
    print(f"Failed: {len(keywords) - len(downloaded_images)}")
    print(f"Images saved in: {download_folder}")
    print(f"{'='*50}")
    
    return downloaded_images

if __name__ == "__main__":
    # Your keywords
    keywords = [
    # Here pass the keywords
    ]
    
    # Save images next to the script (works on any OS)
    download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloaded_images")
    
    print("Starting image download using Bing Images...")
    downloaded = search_and_download_images(keywords, download_path)