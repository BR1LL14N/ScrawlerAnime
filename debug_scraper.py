import requests
from bs4 import BeautifulSoup

def debug_otakudesu():
    """Debug OtakuDesu HTML structure"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = 'https://otakudesu.best/ongoing-anime/'
    
    print(f"Fetching: {url}\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("=" * 80)
        print("HTML STRUCTURE ANALYSIS")
        print("=" * 80)
        
        # 1. Find all divs with common class patterns
        print("\n1. CHECKING COMMON DIV CLASSES:")
        common_classes = ['venz', 'col-anime', 'detpost', 'anime-item', 'post', 'entry']
        for cls in common_classes:
            items = soup.find_all('div', class_=cls)
            print(f"   - div.{cls}: {len(items)} items")
        
        # 2. Find all articles
        articles = soup.find_all('article')
        print(f"\n2. CHECKING ARTICLES:")
        print(f"   - <article> tags: {len(articles)}")
        
        # 3. Find divs containing images
        print(f"\n3. CHECKING DIVS WITH IMAGES:")
        divs_with_img = soup.find_all('div', recursive=True)
        divs_with_img = [d for d in divs_with_img if d.find('img')]
        print(f"   - Divs containing <img>: {len(divs_with_img)}")
        
        # 4. Sample first item
        print(f"\n4. SAMPLE FIRST ITEM HTML:")
        print("-" * 80)
        
        # Try to find the first anime item
        first_item = None
        
        # Try different selectors
        for selector in ['div.venz', 'div.col-anime', 'div.detpost', 'article']:
            items = soup.select(selector)
            if items:
                first_item = items[0]
                print(f"Found using selector: {selector}")
                break
        
        if not first_item and divs_with_img:
            first_item = divs_with_img[0]
            print(f"Using first div with image")
        
        if first_item:
            # Pretty print the HTML
            print(first_item.prettify()[:1000])  # First 1000 chars
            print("...")
            
            # Analyze structure
            print("\n5. STRUCTURE ANALYSIS OF FIRST ITEM:")
            print("-" * 80)
            
            # Find title
            titles = (
                first_item.find_all('h2') +
                first_item.find_all('h3') +
                first_item.find_all('h4')
            )
            print(f"   Headings (h2/h3/h4): {len(titles)}")
            for t in titles[:3]:
                print(f"      - {t.get('class', 'no-class')}: {t.text.strip()[:50]}")
            
            # Find links
            links = first_item.find_all('a')
            print(f"\n   Links (<a>): {len(links)}")
            for link in links[:3]:
                print(f"      - href: {link.get('href', 'N/A')[:50]}")
            
            # Find images
            imgs = first_item.find_all('img')
            print(f"\n   Images (<img>): {len(imgs)}")
            for img in imgs[:3]:
                print(f"      - src: {img.get('src', 'N/A')[:50]}")
                print(f"      - data-src: {img.get('data-src', 'N/A')[:50]}")
                print(f"      - alt: {img.get('alt', 'N/A')[:50]}")
            
            # Find all divs with classes
            divs = first_item.find_all('div', class_=True)
            print(f"\n   Divs with classes: {len(divs)}")
            for div in divs[:5]:
                classes = ' '.join(div.get('class', []))
                text = div.text.strip()[:30]
                print(f"      - .{classes}: {text}")
            
            # Find all spans with classes
            spans = first_item.find_all('span', class_=True)
            print(f"\n   Spans with classes: {len(spans)}")
            for span in spans[:5]:
                classes = ' '.join(span.get('class', []))
                text = span.text.strip()[:30]
                print(f"      - .{classes}: {text}")
        
        else:
            print("❌ Could not find any anime items!")
            print("\nSaving full HTML to 'debug_output.html' for manual inspection...")
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print("✓ Saved to debug_output.html")
        
        print("\n" + "=" * 80)
        print("RECOMMENDATIONS:")
        print("=" * 80)
        
        # Try to find the correct selector
        print("\nBased on the analysis, try these selectors:")
        print("1. soup.find_all('div', class_='venz')")
        print("2. soup.find_all('div', class_='col-anime')")
        print("3. soup.find_all('div', class_='detpost')")
        print("4. soup.find_all('article')")
        print("5. Check 'debug_output.html' file for manual inspection")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    debug_otakudesu()