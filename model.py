import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os

def fetch_html(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    exec_time = end - start
    print(f"[{url}] selesai dalam {exec_time:.2f} detik")
    return response.text, exec_time

def save_html(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def scrape_with_threading(urls, max_workers=5):
    results = []
    times = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # executor.map hanya mengembalikan hasil, tidak cocok untuk menyimpan waktu
        # Gunakan executor.submit untuk kontrol lebih lanjut
        futures = [executor.submit(fetch_html, url) for url in urls]
        for future in futures:
            html, exec_time = future.result()
            results.append(html)
            times.append(exec_time)
    return results, times

def create_index_page(urls, filenames):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hasil Scraping</title>
        <style>
            body { font-family: Arial; }
            a { display: block; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Hasil Scraping dari Berbagai URL</h1>
    """
    for i, url in enumerate(urls):
        html += f'<a href="{filenames[i]}" target="_blank">{url}</a>\n'
    html += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    urls = [
        "https://otakudesu.best/",
        "https://kusonime.com/",
        "https://classroom.itats.ac.id/",  
    ]

    print("Memulai scraping...")
    start_time = time.time()
    htmls, times = scrape_with_threading(urls, max_workers=8)
    end_time = time.time()

    print("\nWaktu eksekusi tiap URL:")
    for i, (url, t) in enumerate(zip(urls, times)):
        print(f"{i+1}. {url} -> {t:.2f}s")

    print(f"\nWaktu total eksekusi: {end_time - start_time:.2f} detik")

    filenames = [f"page_{i}.html" for i in range(len(urls))]
    for html, filename in zip(htmls, filenames):
        save_html(html, filename)

    create_index_page(urls, filenames)
    print("\nSelesai. File HTML disimpan dan index.html dibuat.")

if __name__ == "__main__":
    main()