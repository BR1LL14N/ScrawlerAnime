import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
from datetime import datetime
import os

class AnimeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.results_dir = 'results'
        os.makedirs(self.results_dir, exist_ok=True)
        
    def scrape_otakudesu(self, max_pages=4):
        """Scrape anime list from OtakuDesu with pagination."""
        start_time = time.time()
        # URL dasar diubah sesuai permintaan
        base_url = 'https://otakudesu.best/ongoing-anime/'
        # List untuk menampung semua anime dari semua halaman
        all_anime = [] 
        
        print(f"[Otakudesu] Mulai scraping. Target: {max_pages} halaman.")
        
        try:
            for page in range(1, max_pages + 1):
                if page == 1:
                    url = base_url
                else:
                    url = f'{base_url}page/{page}/'
                
                print(f"[Otakudesu] Scraping halaman {page}: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status() # Cek jika ada error HTTP
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                anime_items = soup.find_all('div', class_='detpost')
                
                # Jika tidak ada item, berarti halaman sudah habis
                if not anime_items:
                    print(f"[Otakudesu] Halaman {page} kosong. Berhenti.")
                    break
                
                page_item_count = 0
                for item in anime_items: # Hapus limit [:15]
                    try:
                        title_elem = item.find('h2', class_='jdlflm')
                        title = title_elem.text.strip() if title_elem else 'N/A'
                        
                        link_elem = item.find('a') 
                        link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
                        
                        img_elem = item.find('img')
                        image = img_elem['src'] if img_elem and 'src' in img_elem.attrs else 'https://via.placeholder.com/150'
                        
                        episode_elem = item.find('div', class_='epz')
                        episode = episode_elem.text.strip() if episode_elem else 'N/A'
                        
                        day_elem = item.find('div', class_='epztipe')
                        day = day_elem.text.strip() if day_elem else 'N/A'
                        
                        rating_elem = item.find('div', class_='bt')
                        rating = rating_elem.text.strip() if rating_elem else 'N/A'
                        
                        all_anime.append({
                            'title': title,
                            'episode': episode,
                            'day': day,
                            'rating': rating,
                            'image': image,
                            'link': link,
                            'source_page': page # Info tambahan
                        })
                        page_item_count += 1
                    except Exception as e:
                        print(f"Error parsing OtakuDesu item: {e}")
                        continue
                
                print(f"[Otakudesu] Selesai halaman {page}, {page_item_count} item ditemukan.")
                time.sleep(0.5) # Jeda antar request halaman
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'success': True,
                'site': 'OtakuDesu',
                'url': base_url, # URL dasar
                'pages_scraped': page if page > 1 else 1,
                'timestamp': datetime.now().isoformat(),
                'execution_time': execution_time,
                'data': all_anime,
                'count': len(all_anime)
            }
            
            with open(f'{self.results_dir}/otakudesu.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ OtakuDesu scraped: {len(all_anime)} anime (dari {page if page > 1 else 1} halaman) in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            result = {
                'success': False,
                'site': 'OtakuDesu',
                'timestamp': datetime.now().isoformat(),
                'execution_time': execution_time,
                'error': str(e),
                'data': all_anime # Kembalikan data yg sudah didapat sblm error
            }
            with open(f'{self.results_dir}/otakudesu.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            return result
    
    def scrape_kusonime(self, max_pages=4):
        """Scrape anime list from Kusonime with pagination."""
        start_time = time.time()
        base_url = 'https://kusonime.com/'
        all_anime = []
        pages_successfully_scraped = 0 # Pelacak halaman yang sukses

        print(f"[Kusonime] Mulai scraping. Target: {max_pages} halaman.")
        
        try:
            for page in range(1, max_pages + 1):
                if page == 1:
                    url = base_url
                else:
                    url = f'https://kusonime.com/page/{page}/'
                
                print(f"[Kusonime] Scraping halaman {page}: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # --- PERBAIKAN 1: LOGIKA SELECTOR GANDA ---
                # Halaman 1 (homepage) menggunakan 'div.detpost'
                # Halaman 2, 3, dst (arsip) menggunakan 'article'
                posts = soup.find_all('div', class_='detpost')
                if not posts:
                    print(f"[Kusonime] 'div.detpost' tidak ditemukan di hal {page}, mencoba 'article'...")
                    posts = soup.find_all('article')
                # --- BATAS PERBAIKAN 1 ---

                if not posts:
                    print(f"[Kusonime] Halaman {page} kosong (tidak ada 'detpost' atau 'article'). Berhenti.")
                    break
                
                page_item_count = 0
                for post in posts: # Hapus limit
                    try:
                        # --- PERBAIKAN 2: LOGIKA PARSING FLEKSIBEL ---
                        # Menggunakan logika parsing Anda sebelumnya yang lebih robust
                        
                        title_elem = post.find(['h2', 'h1'], class_=['episodeye', 'title'])
                        if not title_elem:
                            title_elem = post.find('a', rel='bookmark')
                        title = title_elem.text.strip() if title_elem else 'N/A'
                        
                        link_elem = post.find('a', rel='bookmark') or post.find('a')
                        link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
                        
                        img_elem = post.find('img')
                        image = img_elem['src'] if img_elem and 'src' in img_elem.attrs else 'https://via.placeholder.com/150'
                        
                        # Coba ambil tanggal dari 'fa-clock-o' (di homepage) atau 'time' (di arsip)
                        date_elem = post.find('i', class_='fa-clock-o')
                        if date_elem:
                            date = date_elem.parent.text.strip()
                        else:
                            date_elem = post.find('time') or post.find('span', class_='date')
                            date = date_elem.text.strip() if date_elem else 'N/A'
                        
                        # Coba ambil genre dari 'fa-tag' (di homepage) atau 'romaji' (di arsip)
                        genre_p = post.find('i', class_='fa-tag')
                        if genre_p:
                            genre_links = genre_p.parent.find_all('a')
                            genre = ', '.join([a.text.strip() for a in genre_links])
                        else:
                            genre_elem = post.find('span', class_='romaji')
                            genre = genre_elem.text.strip() if genre_elem else 'N/A'
                        
                        # Summary (jika ada)
                        summary_elem = post.find('div', class_='excerpt') or post.find('p')
                        summary_text = summary_elem.text.strip() if summary_elem else 'N/A'
                        
                        # Pastikan summary bukan text genre atau date
                        if summary_text in [genre, date]:
                            summary = 'N/A'
                        else:
                            summary = summary_text[:100] + '...' if summary_text != 'N/A' else 'N/A'
                        # --- BATAS PERBAIKAN 2 ---

                        all_anime.append({
                            'title': title,
                            'date': date,
                            'genre': genre,
                            'summary': summary,
                            'image': image,
                            'link': link,
                            'source_page': page
                        })
                        page_item_count += 1
                    except Exception as e:
                        print(f"Error parsing Kusonime item: {e} | {post.text[:50]}...")
                        continue
                
                print(f"[Kusonime] Selesai halaman {page}, {page_item_count} item ditemukan.")
                pages_successfully_scraped = page # Tandai halaman ini sukses
                time.sleep(0.5) 

            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'success': True,
                'site': 'Kusonime',
                'url': base_url,
                'pages_scraped': pages_successfully_scraped, # Gunakan pelacak yang akurat
                'timestamp': datetime.now().isoformat(),
                'execution_time': execution_time,
                'data': all_anime,
                'count': len(all_anime)
            }
            
            with open(f'{self.results_dir}/kusonime.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Kusonime scraped: {len(all_anime)} anime (dari {pages_successfully_scraped} halaman) in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            result = {
                'success': False,
                'site': 'Kusonime',
                'url': base_url,
                'pages_scraped': pages_successfully_scraped, # Tampilkan halaman terakhir yg sukses
                'timestamp': datetime.now().isoformat(),
                'execution_time': execution_time,
                'error': str(e),
                'data': all_anime
            }
            with open(f'{self.results_dir}/kusonime.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            return result
    
    def scrape_parallel(self, max_workers=2, max_pages_per_site=1):
        """Scrape websites in parallel using ThreadPoolExecutor with pagination."""
        print(f"Starting parallel scraping... (Target: {max_pages_per_site} halaman per situs)")
        start_time = time.time()
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit jobs dengan parameter max_pages_per_site
            future_otaku = executor.submit(self.scrape_otakudesu, max_pages=max_pages_per_site)
            future_kuso = executor.submit(self.scrape_kusonime, max_pages=max_pages_per_site)

            futures = {future_otaku: "Otakudesu", future_kuso: "Kusonime"}
            
            for future in as_completed(futures):
                site_name = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error besar dalam thread {site_name}: {e}")
                    results.append({
                        'success': False, 
                        'site': site_name, 
                        'error': str(e), 
                        'data': [], 
                        'count': 0,
                        'timestamp': datetime.now().isoformat(),
                        'execution_time': 0
                    })
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n✓ Total parallel execution time: {total_time:.2f}s")
        print(f"✓ Results saved to '{self.results_dir}/' directory")
        
        return {
            'method': 'Parallel (ThreadPoolExecutor)',
            'total_execution_time': total_time,
            'results': results
        }

if __name__ == '__main__':
    scraper = AnimeScraper()
    # Contoh: Scrape 2 halaman dari setiap situs
    print("--- MENJALANKAN SCRAPE UNTUK 2 HALAMAN ---")
    scraper.scrape_parallel(max_pages_per_site=2)
    
    # print("\n--- MENJALANKAN SCRAPE UNTUK 1 HALAMAN (DEFAULT) ---")
    # scraper.scrape_parallel(max_pages_per_site=1)