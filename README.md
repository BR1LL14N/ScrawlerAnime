# Anime Scraper - OtakuDesu & Kusonime

Program web scraping anime menggunakan Python dengan ThreadPoolExecutor. Data tersimpan dalam JSON terpisah dengan view HTML individual untuk setiap website.

## 🎯 Fitur Utama

- ✅ **Scraping 2 Website Anime**: OtakuDesu dan Kusonime
- ✅ **JSON Terpisah**: Data disimpan di `otakudesu.json` dan `kusonime.json`
- ✅ **View HTML Terpisah**: Tampilan khusus untuk setiap website
- ✅ **Gambar Anime**: Setiap anime menampilkan thumbnail/poster
- ✅ **Waktu Eksekusi Individual**: Tracking waktu per website
- ✅ **Parallel Scraping**: Menggunakan ThreadPoolExecutor
- ✅ **Multiple Routes**: Route terpisah untuk setiap website
- ✅ **REST API**: Endpoint JSON untuk integrasi

## 📁 Struktur Folder

```
anime-scraper/
│
├── scraper.py              # Script scraping utama
├── app.py                  # Flask web application
├── requirements.txt        # Dependencies
├── README.md              # Dokumentasi
│
├── templates/             # Template HTML
│   ├── index.html        # Halaman utama
│   ├── otakudesu.html    # View OtakuDesu
│   ├── kusonime.html     # View Kusonime
│   └── comparison.html   # Perbandingan
│
└── results/              # Folder hasil scraping (auto-created)
    ├── otakudesu.json    # Data OtakuDesu
    └── kusonime.json     # Data Kusonime
```

## 🚀 Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

atau install manual:

```bash
pip install flask requests beautifulsoup4 lxml
```

### 2. Jalankan Web Server

```bash
python app.py
```

### 3. Buka Browser

Akses: `http://localhost:5000`

## 🌐 Routes / Endpoint

### Web Routes (HTML Views)

| Route | Deskripsi |
|-------|-----------|
| `/` | Halaman utama dengan kontrol scraping |
| `/otakudesu` | View hasil scraping OtakuDesu dengan gambar |
| `/kusonime` | View hasil scraping Kusonime dengan gambar |
| `/comparison` | Perbandingan kedua website |

### API Routes (JSON)

| Route | Deskripsi |
|-------|-----------|
| `/api/otakudesu` | JSON data OtakuDesu |
| `/api/kusonime` | JSON data Kusonime |
| `/scrape-otakudesu` | Trigger scraping OtakuDesu |
| `/scrape-kusonime` | Trigger scraping Kusonime |
| `/scrape-all` | Scraping parallel kedua website |

## 📊 Data yang Di-scrape

### 🔴 OtakuDesu (`otakudesu.json`)

```json
{
  "success": true,
  "site": "OtakuDesu",
  "url": "https://otakudesu.cloud/ongoing-anime/",
  "timestamp": "2024-11-10T14:30:00",
  "execution_time": 2.34,
  "count": 15,
  "data": [
    {
      "title": "One Piece",
      "episode": "Episode 1234",
      "day": "Minggu",
      "rating": "Completed",
      "image": "https://...",
      "link": "https://..."
    }
  ]
}
```

**Field:**
- `title`: Judul anime
- `episode`: Episode terbaru
- `day`: Hari tayang
- `rating`: Status/rating
- `image`: URL gambar anime
- `link`: Link detail anime

### 🟢 Kusonime (`kusonime.json`)

```json
{
  "success": true,
  "site": "Kusonime",
  "url": "https://kusonime.com/",
  "timestamp": "2024-11-10T14:30:05",
  "execution_time": 1.87,
  "count": 15,
  "data": [
    {
      "title": "Naruto Shippuden",
      "date": "10 November 2024",
      "genre": "Action, Adventure",
      "summary": "Ringkasan anime...",
      "image": "https://...",
      "link": "https://..."
    }
  ]
}
```

**Field:**
- `title`: Judul anime
- `date`: Tanggal upload
- `genre`: Genre anime
- `summary`: Ringkasan singkat
- `image`: URL gambar anime
- `link`: Link detail anime

## 💻 Cara Menggunakan

### Dari Web Interface

1. **Buka halaman utama** (`http://localhost:5000`)

2. **Pilih metode scraping:**
   - **Scrape OtakuDesu**: Scraping OtakuDesu saja
   - **Scrape Kusonime**: Scraping Kusonime saja
   - **Scrape Semua**: Scraping kedua website secara parallel

3. **Lihat hasil:**
   - Klik tombol **View** untuk melihat tampilan dengan gambar
   - Klik tombol **JSON** untuk melihat raw data

### Dari Python Script

```python
from scraper import AnimeScraper

scraper = AnimeScraper()

# Scrape OtakuDesu
otaku_result = scraper.scrape_otakudesu()

# Scrape Kusonime
kuso_result = scraper.scrape_kusonime()

# Scrape parallel
parallel_result = scraper.scrape_parallel()
```

### Dari Command Line

```bash
python scraper.py
```

## 🔍 Cara Kerja ThreadPoolExecutor

Program menggunakan `concurrent.futures.ThreadPoolExecutor` untuk scraping parallel:

```python
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {
        executor.submit(scraper): scraper.__name__ 
        for scraper in scrapers
    }
    
    for future in as_completed(futures):
        result = future.result()
```

**Keuntungan:**
- ⚡ Scraping lebih cepat (2 website bersamaan)
- 🎯 Efisien untuk multiple websites
- 📊 Tracking waktu eksekusi individual
- 🔄 Parallel execution dengan synchronization

## 🎨 Fitur Tampilan

### Halaman OtakuDesu
- 🔴 Tema warna merah
- 📺 Tampilan grid dengan gambar anime
- ⏱️ Statistik waktu eksekusi
- 📅 Informasi episode dan jadwal

### Halaman Kusonime
- 🟢 Tema warna hijau
- 🎬 Card layout dengan poster anime
- 📝 Ringkasan anime
- 🏷️ Badge genre

### Halaman Comparison
- 📊 Grafik bar perbandingan waktu
- 🏆 Winner badge (website tercepat)
- 📈 Statistik lengkap kedua website
- 🔗 Quick links ke detail masing-masing

## ⚙️ Konfigurasi

### Mengubah Jumlah Anime

Edit di `scraper.py`:

```python
for item in anime_items[:15]:  # Ubah 15 ke jumlah yang diinginkan
```

### Mengubah Worker Threads

Edit di `scraper.py`:

```python
parallel_result = scraper.scrape_parallel(max_workers=4)  # Default: 2
```

### Mengubah Timeout

Edit di `scraper.py`:

```python
response = requests.get(url, headers=self.headers, timeout=20)  # Default: 10
```

## 🐛 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: No data scraped
- Website mungkin mengubah struktur HTML
- Periksa selector CSS di method scraping
- Pastikan website bisa diakses

### Error: Connection timeout
- Periksa koneksi internet
- Tingkatkan nilai timeout
- Website mungkin sedang down

### Gambar tidak muncul
- URL gambar mungkin expired/berubah
- Website memblokir hotlinking
- Placeholder akan muncul otomatis

## 📝 Contoh Output JSON

### OtakuDesu
```json
{
  "success": true,
  "site": "OtakuDesu",
  "execution_time": 2.34,
  "count": 15,
  "data": [...]
}
```

### Kusonime
```json
{
  "success": true,
  "site": "Kusonime",
  "execution_time": 1.87,
  "count": 15,
  "data": [...]
}
```

## 📄 License

Free to use for educational purposes.

## 🙏 Credits

- BeautifulSoup4 untuk HTML parsing
- Flask untuk web framework
- ThreadPoolExecutor untuk parallel processing

---

**Happy Scraping! 🎉**

Made with ❤️ for Anime Lovers