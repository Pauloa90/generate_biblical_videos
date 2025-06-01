#!/usr/bin/env python3
"""
Test script to verify all images are accessible before running video generation
"""

import requests
import json
import sys
from typing import Dict, List, Tuple

def load_config() -> Dict:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        return None

def test_image_url(url: str, image_name: str) -> Tuple[bool, str]:
    """Test if an image URL is accessible"""
    try:
        print(f"Testing {image_name}: {url}")
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            # Try to get content type
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                return True, f"✅ {image_name}: OK ({content_type})"
            else:
                return False, f"⚠️  {image_name}: Not an image ({content_type})"
        else:
            return False, f"❌ {image_name}: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ {image_name}: Error - {str(e)}"

def get_image_urls(config: Dict) -> Dict[str, str]:
    """Get all image URLs based on configuration"""
    image_source = config['image_source']
    urls = {}
    
    if image_source['type'] == 'github':
        base_url = image_source['github_base_url']
        # Ensure base URL ends with /
        if not base_url.endswith('/'):
            base_url += '/'
        
        images = ['David', 'Saul', 'Golias', 'bg1', 'bg2', 'bg3', 'bg4', 'bg5']
        for img in images:
            urls[img] = f"{base_url}{img}.png"
    
    elif image_source['type'] == 'google_drive':
        gdrive_template = "https://drive.google.com/uc?export=download&id={file_id}"
        for img_name, file_id in image_source['google_drive_ids'].items():
            if file_id and file_id != "YOUR_" + img_name.upper() + "_FILE_ID":
                urls[img_name] = gdrive_template.format(file_id=file_id)
    
    return urls

def main():
    """Main test function"""
    print("🔍 Biblical Videos Image Tester")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    if not config:
        return 1
    
    # Get image URLs
    image_urls = get_image_urls(config)
    
    if not image_urls:
        print("❌ No image URLs configured!")
        print("Please update config.json with your image locations.")
        return 1
    
    print(f"\nTesting {len(image_urls)} images...")
    print("-" * 50)
    
    # Test each image
    results = []
    all_passed = True
    
    for img_name, url in image_urls.items():
        passed, message = test_image_url(url, img_name)
        results.append((img_name, passed, message))
        if not passed:
            all_passed = False
    
    # Print results
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    for img_name, passed, message in results:
        print(message)
    
    print("\n" + "-" * 50)
    
    if all_passed:
        print("✅ All images are accessible! Ready to generate videos.")
        return 0
    else:
        print("❌ Some images failed. Please fix the issues before generating videos.")
        print("\nTips:")
        print("- For GitHub: Make sure images are committed and pushed")
        print("- For Google Drive: Ensure links are set to 'Anyone with link can view'")
        print("- Check that file names match exactly (case-sensitive)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
