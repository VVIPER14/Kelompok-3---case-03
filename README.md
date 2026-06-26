# Predictive Maintenance Berbasis Sensor Mesin
**Case 03 — Tugas Besar Ilmu dan Analitika Data**
**Kelompok 3 | Teknik Industri**

| Nama Anggota | NIM |
|---|---|
| Suroso Aditya Wibowo | 2410932036 |
| Afif Gardana | 2410931009 |
| Alfi Mutawakkil Marwan | 2410932008 |

---

## Daftar Isi

1. [Problem Statement Industri](#1-problem-statement-industri)
2. [Keputusan yang Ingin Diambil](#2-keputusan-yang-ingin-diambil)
3. [Stakeholder](#3-stakeholder)
4. [KPI Utama](#4-kpi-utama)
5. [Batasan Sistem](#5-batasan-sistem)
6. [Data Source dan Unit Analisis](#6-data-source-dan-unit-analisis)
7. [Data Dictionary ](#7-data-dictionary)
8. [Cara Menjalankan Environment dan Analisis](#8-cara-menjalankan-environment-dan-analisis)
9. [Ringkasan Insight](#9-ringkasan-insight)
10. [Rekomendasi Operasional dan Estimasi Dampak](#10-rekomendasi-operasional-dan-estimasi-dampak)
11. [Risiko Implementasi dan Monitoring](#11-risiko-implementasi-dan-monitoring)

---

## 1. Problem Statement Industri

Downtime mesin yang tidak terprediksi merupakan salah satu sumber kerugian terbesar dalam operasional manufaktur. Ketika sebuah mesin berhenti secara mendadak di tengah proses produksi, dampaknya tidak hanya pada mesin itu sendiri, tetapi juga menjalar ke seluruh lini produksi: jadwal pengiriman terganggu, operator terpaksa menganggur, dan tim maintenance bekerja dalam kondisi darurat yang biayanya jauh lebih tinggi dibanding pekerjaan terencana.

Kondisi yang berlangsung saat ini adalah perawatan mesin dilakukan secara reaktif. Teknisi baru bergerak setelah mesin berhenti atau setelah operator melaporkan keluhan. Rata-rata waktu respons dalam kondisi ini mencapai lebih dari 2 jam setelah downtime terjadi, sementara kerusakan komponen sebenarnya sudah berkembang jauh sebelum tanda-tanda fisik terlihat oleh operator.

Data sensor yang tersedia pada setiap mesin — mencakup getaran, suhu, arus listrik, tingkat pelumas, dan jumlah alarm — sebenarnya mengandung sinyal peringatan dini yang selama ini belum dimanfaatkan secara sistematis. Analisis ini bertujuan membangun sistem prediksi yang dapat mendeteksi risiko downtime setidaknya 24 jam sebelum kejadian, sehingga tim maintenance memiliki cukup waktu untuk melakukan tindakan preventif secara terencana.

---

## 2. Keputusan yang Ingin Diambil

Ada dua keputusan operasional utama yang ingin dijawab melalui analisis ini.

Pertama, menentukan apakah suatu mesin perlu mendapatkan tindakan preventive maintenance sebelum downtime terjadi. Keputusan ini diambil berdasarkan output model prediksi yang membaca kondisi sensor mesin pada setiap jam observasi. Jika probabilitas prediksi melampaui threshold yang telah ditentukan, maka mesin tersebut masuk ke antrean pemeriksaan maintenance.

Kedua, memprioritaskan urutan penanganan ketika ada lebih dari satu mesin yang terdeteksi berisiko secara bersamaan. Karena sumber daya teknisi terbatas, model tidak hanya dituntut dapat mendeteksi mesin berisiko, tetapi juga menghasilkan skor probabilitas yang bisa digunakan sebagai dasar pengurutan prioritas penanganan.

---

## 3. Stakeholder

**Teknisi Maintenance** adalah pengguna langsung output model. Mereka menerima notifikasi atau daftar prioritas mesin yang perlu diperiksa, lalu melakukan tindakan preventif berdasarkan rekomendasi tersebut. Bagi mereka, yang paling kritis adalah tingkat kepercayaan terhadap alarm — terlalu banyak alarm palsu akan membuat mereka mengabaikan sistem.

**Manajer Produksi** berkepentingan memastikan lini produksi berjalan sesuai jadwal. Mereka membutuhkan informasi tentang mesin mana yang berisiko agar dapat menyesuaikan jadwal produksi atau menyiapkan mesin cadangan sebelum downtime terjadi.

**Manajer Maintenance** bertanggung jawab atas efisiensi penggunaan sumber daya tim teknisi dan anggaran maintenance. Mereka menggunakan output model untuk perencanaan jadwal preventive maintenance jangka menengah dan memantau performa model secara berkala.

---

## 4. KPI Utama

### a. Downtime Recall

KPI ini mengukur kemampuan model dalam mendeteksi mesin yang benar-benar akan mengalami downtime dalam 24 jam ke depan. Recall adalah metrik paling kritis dalam kasus ini karena konsekuensi melewatkan satu downtime (False Negative) jauh lebih mahal dibanding mengirim teknisi untuk memeriksa mesin yang ternyata normal (False Positive).

- **Rumus:** Recall = TP / (TP + FN)
- **Numerator:** True Positive (TP) — jumlah mesin yang benar-benar akan downtime dan berhasil diprediksi oleh model.
- **Denominator:** TP + FN — seluruh mesin yang sebenarnya akan mengalami downtime di periode test.
- **Satuan:** Persentase (%)
- **Baseline:** 0% (tidak ada sistem prediksi sebelumnya)
- **Target:** Recall ≥ 80%

### b. False Alarm Rate (FAR)

KPI ini mengukur seberapa sering model memberikan alarm downtime padahal mesin sebenarnya dalam kondisi normal. FAR yang terlalu tinggi menyebabkan alarm fatigue — teknisi mulai mengabaikan notifikasi karena terlalu sering terbukti salah.

- **Rumus:** FAR = FP / (FP + TN)
- **Numerator:** False Positive (FP) — jumlah mesin yang diprediksi downtime padahal kenyataannya tidak.
- **Denominator:** FP + TN — seluruh mesin yang sebenarnya tidak mengalami downtime.
- **Satuan:** Persentase (%)
- **Baseline:** 0% (tidak ada sistem prediksi sebelumnya)
- **Target:** FAR ≤ 30%

### c. Downtime Avoidance

KPI ini mengukur proporsi downtime yang berhasil dicegah melalui tindakan maintenance berdasarkan prediksi model. KPI ini baru dapat diukur secara akurat setelah sistem diterapkan secara operasional karena membutuhkan data tindakan aktual teknisi sebagai respons terhadap alarm.

- **Rumus:** Downtime Avoidance = Downtime yang berhasil dicegah / Total downtime potensial
- **Numerator:** Jumlah kejadian downtime yang berhasil dicegah karena ada tindakan preventif sebelum waktu kritis.
- **Denominator:** Total downtime yang diperkirakan akan terjadi tanpa intervensi.
- **Satuan:** Persentase (%)
- **Baseline:** 0% (belum ada mekanisme pencegahan prediktif)
- **Target:** ≥ 50% downtime potensial berhasil dihindari

---

## 5. Batasan Sistem

| Batasan | Penjelasan |
|---|---|
| Ketersediaan data real-time | Prediksi hanya valid jika semua sensor aktif mengirim data. Jika satu atau lebih sensor mati atau tidak terkalibrasi, output model tidak dapat dipercaya dan harus diabaikan. |
| Frekuensi re-training model | Model perlu di-retrain minimal setiap 3 bulan untuk mengantisipasi perubahan karakteristik mesin akibat penuaan komponen, penggantian suku cadang, atau perubahan kondisi operasional. |
| Latency keputusan | Prediksi harus tersedia dalam 5 menit setelah data sensor masuk ke sistem agar teknisi memiliki cukup waktu untuk merespons sebelum downtime terjadi. |
| Pengukuran Downtime Avoidance | KPI ini baru dapat dihitung setelah sistem berjalan secara operasional dan ada pencatatan tindakan teknisi yang terstruktur. Pada tahap evaluasi model historis, KPI ini tidak dapat dikuantifikasi langsung. |
| Interpretabilitas model | Model yang dipilih harus dapat menjelaskan alasan di balik setiap prediksi agar teknisi dapat memvalidasi secara logis sebelum mengambil tindakan. |

---

## 6. Data Source dan Unit Analisis

Dataset yang digunakan adalah dataset synthetic-realistic predictive maintenance yang terdiri dari 2.400 baris observasi dan 14 kolom. Dataset ini sengaja mengandung isu kualitas data seperti missing value, outlier, dan nilai tidak valid agar proses profiling dan cleaning dapat dipraktikkan.

**Unit analisis** adalah **mesin-jam (machine-hour)**: setiap baris merepresentasikan kondisi satu mesin pada satu titik waktu observasi. Kolom target `downtime_next_24h` menunjukkan apakah mesin tersebut mengalami downtime dalam 24 jam setelah titik observasi tersebut.

---

## 7. Data Dictionary 

Unit analisis: mesin-jam.

Target/fokus analisis awal: `downtime_next_24h`.

| Kolom | Tipe Awal | Deskripsi |
|---|---|---|
| `timestamp` | date/datetime atau kategori waktu | Waktu observasi. |
| `machine_id` | string/kategori | ID mesin. Gunakan untuk segmentasi dan analisis variasi antar mesin. |
| `line` | kategori | Lini produksi atau area operasi. |
| `age_months` | numeric/kategori | Kolom operasional. Definisi perlu dikaitkan dengan problem statement dan KPI. |
| `last_maintenance_days` | numeric | Kolom operasional. Definisi perlu dikaitkan dengan problem statement dan KPI. |
| `temp_c` | numeric | Temperatur proses atau mesin dalam derajat Celsius. |
| `vibration_mm_s` | numeric | Getaran mesin dalam mm/s. Nilai ekstrem dapat berarti gejala kerusakan atau error sensor. |
| `current_a` | numeric | Arus listrik mesin dalam ampere. |
| `load_pct` | numeric | Rasio atau persentase. Periksa denominator sebelum membuat agregasi. |
| `lubricant_level_pct` | numeric | Rasio atau persentase. Periksa denominator sebelum membuat agregasi. |
| `alarm_count` | numeric | Kolom operasional. Definisi perlu dikaitkan dengan problem statement dan KPI. |
| `downtime_next_24h` | binary 0/1 | Target 1 jika mesin mengalami downtime dalam 24 jam berikutnya. |
| `maintenance_ticket_closed` | numeric/kategori | Status tiket setelah kejadian. Kolom ini tidak tersedia saat prediksi awal. |
| `failure_mode` | numeric/kategori | Kolom operasional. Definisi perlu dikaitkan dengan problem statement dan KPI. |

### Dictionary Final (setelah profiling dan cleaning)

| Kolom | Tipe Final | Status | Deskripsi | Perubahan |
|---|---|---|---|---|
| `timestamp` | datetime64 | Digunakan (informasi) | Waktu observasi kondisi mesin. Digunakan untuk pengurutan temporal sebelum train-test split. | Dikonversi dari object ke datetime64 menggunakan `pd.to_datetime()`. |
| `machine_id` | object (kategorikal) | Digunakan (segmentasi) | ID unik mesin. Digunakan untuk segmentasi downtime rate per mesin, bukan sebagai fitur model. | Tidak ada perubahan. |
| `line` | object (kategorikal) | Digunakan (segmentasi) | Lini produksi tempat mesin beroperasi. Digunakan untuk perbandingan downtime rate antar lini, bukan sebagai fitur model. | Tidak ada perubahan. |
| `age_months` | float64 | Fitur model | Umur mesin dalam bulan. Tersedia saat keputusan dibuat. Berkorelasi positif lemah dengan downtime (r=0.028). | Tidak ada perubahan. |
| `last_maintenance_days` | float64 | Fitur model | Jumlah hari sejak maintenance terakhir. Tersedia saat keputusan dibuat. Fitur ketiga terkuat (r=0.123). | Tidak ada perubahan. |
| `temp_c` | float64 | Fitur model | Temperatur operasi mesin (°C). Tersedia real-time dari sensor. Median downtime (78.3°C) sedikit lebih tinggi dari normal (75.4°C). | Tidak ada perubahan. |
| `vibration_mm_s` | float64 | Fitur model | Getaran mesin (mm/s). Tersedia real-time. Fitur kedua terkuat (r=0.126); 79.1% baris downtime memiliki getaran di atas median normal. | Nilai di atas persentil ke-99 di-clip. Nilai 999 mm/s merupakan noise sensor. |
| `current_a` | float64 | Fitur model | Arus listrik mesin (Ampere). Tersedia real-time. Korelasinya dengan downtime sangat lemah (r=-0.020); kurang informatif sebagai sinyal peringatan dini. | Tidak ada perubahan. |
| `load_pct` | float64 | Fitur model | Persentase beban operasi terhadap kapasitas maksimal (domain: 0–100%). Korelasinya dengan downtime sangat lemah (r=-0.010). | Nilai > 100% di-clip ke 100. Nilai di atas batas domain merupakan error pembacaan sensor. |
| `lubricant_level_pct` | float64 | Fitur model | Persentase level pelumas. Korelasi negatif dengan downtime (r=-0.096); median saat downtime (38.5%) jauh lebih rendah dari normal (51.4%). | 72 missing value diisi dengan median per machine_id. Imputasi per mesin dipilih karena tiap mesin memiliki karakteristik pelumas yang berbeda. |
| `alarm_count` | float64 | Fitur model | Jumlah alarm selama periode observasi. Fitur dengan korelasi terkuat terhadap downtime (r=0.182); median saat downtime (2) dua kali lipat kondisi normal (1). | Tidak ada perubahan. |
| `downtime_next_24h` | int64 (biner 0/1) | Target | Bernilai 1 jika mesin mengalami downtime dalam 24 jam setelah observasi. Distribusi imbalanced: 2.333 normal (97.2%) vs 67 downtime (2.8%). | Tidak ada perubahan. |
| `maintenance_ticket_closed` | — | Dihapus (leakage) | Status penyelesaian tiket maintenance. Dihapus karena hanya tersedia setelah maintenance selesai — tidak dapat digunakan sebagai fitur prediksi real-time. | Dihapus sebelum analisis apapun menggunakan `df.drop()`. |
| `failure_mode` | — | Dihapus (leakage) | Jenis kegagalan mesin. Dihapus karena hanya diketahui setelah teknisi mendiagnosis kerusakan pasca downtime. | Dihapus sebelum analisis apapun menggunakan `df.drop()`. |

### Changelog Cleaning

| # | Kolom | Masalah | Tindakan | Alasan |
|---|---|---|---|---|
| 1 | `maintenance_ticket_closed`, `failure_mode` | Data leakage | Dihapus dari dataset | Hanya tersedia setelah kejadian downtime terjadi; tidak dapat digunakan sebagai fitur prediksi real-time |
| 2 | `lubricant_level_pct` | 72 missing values | Imputasi median per `machine_id` | Data sensor time-series — baris tidak boleh dihapus; median per mesin lebih representatif dari median global |
| 3 | `load_pct` | Nilai > 100% (maks 105%) — error sensor | `.clip(upper=100)` | Persentase tidak bisa melebihi 100% secara domain; informasi kondisi beban tinggi tetap dipertahankan |
| 4 | `vibration_mm_s` | Outlier ekstrem hingga 999 mm/s — noise sensor | `.clip(upper=persentil_99)` | Nilai 999 mm/s bukan kondisi mesin nyata; baris tidak dihapus karena kolom lain pada baris yang sama tetap valid |
| 5 | `timestamp` | Tipe object, seharusnya datetime | `pd.to_datetime()` | Diperlukan untuk pengurutan temporal sebelum train-test split agar tidak terjadi leakage temporal |

Dimensi akhir: 2.400 baris × 12 kolom (dari 14 kolom awal; tidak ada baris yang dihapus).
---

## 8. Cara Menjalankan Environment dan Analisis

### Prasyarat

Python 3.10 atau lebih baru.

### Instalasi Dependencies

```bash
pip install -r requirements.txt
```

### Urutan Menjalankan Analisis

Seluruh analisis harus dijalankan secara berurutan karena setiap notebook menggunakan output dari tahap sebelumnya.

**Langkah 1 — Profiling dan Cleaning**

Jalankan seluruh cell pada `notebooks/01_profiling_cleaning.ipynb`. Notebook ini membaca `data/raw/dataset_raw.csv`, melakukan profiling dan cleaning, lalu menyimpan hasilnya ke `data/processed/dataset_clean.csv`. Pastikan file raw tidak dimodifikasi secara manual.

**Langkah 2 — EDA dan Visualisasi**

Jalankan `notebooks/02_eda_visualisasi.ipynb`. Notebook ini membaca `data/processed/dataset_clean.csv` dan menyimpan seluruh grafik EDA ke `reports/figures/`.

**Langkah 3 — Model dan Evaluasi**

Jalankan `notebooks/03_model_evaluasi.ipynb`. Notebook ini menjalankan training, threshold tuning, dan evaluasi model Logistic Regression, serta menyimpan confusion matrix, precision-recall curve, dan feature importance ke `reports/figures/`.

**Alternatif via Script**

```bash
python src/make_dataset.py
python src/train_model.py
python src/evaluate.py
```

### Catatan Reproducibility

Seluruh proses menggunakan `random_state=42` secara konsisten di semua langkah (SMOTE, model). Split data menggunakan metode temporal (80% data awal untuk training, 20% data terbaru untuk test) sehingga tidak ada data leakage temporal. Path bersifat relatif terhadap direktori utama.

---

## 9. Ringkasan Insight

**Insight 1 — alarm_count dan last_maintenance_days adalah dua sinyal risiko terkuat, dengan peran berbeda di EDA dan model**

Dari korelasi Pearson, `alarm_count` memiliki hubungan terkuat dengan `downtime_next_24h` (r = 0.182, p < 0.0001), dengan median alarm saat downtime (2) dua kali lipat kondisi normal (1). Namun pada model Logistic Regression, `last_maintenance_days` muncul sebagai fitur dengan koefisien terbesar (|koef| = 0.866), diikuti `alarm_count` (|koef| = 0.713). Perbedaan urutan ini terjadi karena LR bekerja dengan bobot yang dipengaruhi distribusi fitur setelah StandardScaler, sedangkan korelasi Pearson tidak. Kesimpulannya: **kedua fitur ini secara konsisten merupakan sinyal terkuat** — mesin yang lama tidak dirawat dan sering memicu alarm adalah kombinasi risiko tertinggi yang harus diprioritaskan untuk pemeriksaan.

**Insight 2 — vibration_mm_s dan temp_c melengkapi sinyal risiko dengan dukungan statistik yang signifikan**

`vibration_mm_s` konsisten berada di posisi ketiga terkuat pada korelasi Pearson (r = 0.126) dan koefisien LR (|koef| = 0.451). Median getaran saat downtime adalah 3.97 mm/s dibanding 3.35 mm/s pada kondisi normal, dengan perbedaan yang signifikan secara statistik (Mann-Whitney U, p < 0.0001). `temp_c` juga signifikan (p = 0.0001) dengan median downtime 78.3°C vs normal 75.4°C. Sebaliknya, `load_pct` (p = 0.663), `current_a` (p = 0.174), dan `age_months` (p = 0.164) tidak signifikan — ketiga fitur ini tidak dapat diandalkan sebagai sinyal peringatan dini dalam dataset ini meskipun tetap diikutsertakan sebagai fitur model.

**Insight 3 — Pelumas rendah berkorelasi negatif signifikan dan mencerminkan risiko mekanis yang dapat dicegah**

`lubricant_level_pct` memiliki korelasi negatif yang signifikan dengan downtime (r = −0.096, p < 0.0001). Median level pelumas saat mesin akan downtime adalah 38.5%, jauh lebih rendah dibanding kondisi normal (51.4%). Ini konsisten secara fisik: pelumas yang berkurang menyebabkan gesekan antar komponen meningkat, mempercepat keausan, dan berujung pada kegagalan mekanis. Meskipun korelasinya tidak sekuat alarm atau getaran, kategori kerusakan akibat pelumas rendah adalah yang paling mudah dan paling murah dicegah melalui inspeksi rutin terjadwal.

**Insight 4 — L3 dan L1 memiliki downtime rate tertinggi; L2 paling stabil dengan semua mesin di bawah rata-rata global**

Downtime rate rata-rata global adalah 2.79% (67 downtime dari 2.400 observasi). Lini L3 mencatat rate tertinggi (3.17%), didorong oleh MX-11 (4.0%) dan MX-07 (3.5%). Lini L1 dan L4 menyusul dengan rate 3.00%; MX-05 di L1 adalah mesin paling bermasalah di seluruh fleet dengan rate 5.0% — hampir dua kali rata-rata global. Sebaliknya, seluruh mesin di Lini L2 berada di bawah rata-rata global (MX-10: 2.5%, MX-02: 2.0%, MX-06: 1.5%), menjadikan L2 lini paling stabil. Pola ini mengindikasikan kemungkinan adanya perbedaan sistemik — baik dari sisi kondisi lingkungan, pola penggunaan, maupun praktik maintenance — antara lini yang perlu ditelusuri lebih lanjut.

**Insight 5 — Logistic Regression dengan threshold 0.30 mencapai Recall 95.5% dan dipilih sebagai model operasional; FAR 42.8% perlu dikelola aktif**

Model terpilih adalah Logistic Regression dengan threshold 0.30, dilatih menggunakan temporal split 80:20 (1.920 baris training, 480 baris test) dan SMOTE untuk menangani class imbalance. Dari 22 kejadian downtime di periode test, 21 berhasil dideteksi (Recall = 95.5%, TP = 21, FN = 1), melampaui target ≥ 80%. FAR mencapai 42.8% (196 alarm palsu dari 458 kondisi normal di test set). Threshold 0.30 dipilih lebih rendah dari default 0.50 karena biaya melewatkan satu downtime jauh lebih besar dibanding biaya alarm palsu. Konsekuensinya, FAR mencapai 42.8% (196 alarm palsu dari 458 kondisi normal di test set) — melampaui target ≤ 30%. Trade-off ini disengaja: dalam konteks predictive maintenance, satu downtime mendadak yang tidak terdeteksi dampaknya jauh lebih besar dari beberapa alarm palsu yang mengharuskan teknisi memeriksa mesin yang ternyata normal. FAR yang tinggi ini harus dikelola aktif melalui mekanisme prioritisasi alarm dan edukasi teknisi agar tidak terjadi alarm fatigue.

---

## 10. Rekomendasi Operasional dan Estimasi Dampak

| # | Rekomendasi | Pelaksana | Estimasi Dampak |
|---|---|---|---|
| 1 | Integrasikan output model Logistic Regression ke sistem SCADA atau MES. Kirim notifikasi otomatis ke teknisi yang bertugas ketika probabilitas prediksi suatu mesin melampaui threshold 0.30, dengan urutan prioritas berdasarkan skor probabilitas tertinggi. | Tim IT/OT + Maintenance Manager | Dengan Recall 95.5%, dari 22 potensi downtime di periode evaluasi, 21 dapat dideteksi lebih dari 24 jam sebelumnya — memberikan waktu yang cukup untuk tindakan preventif terencana. |
| 2 | Tetapkan aturan eskalasi `alarm_count` sebagai lapisan peringatan kedua yang tidak bergantung pada model. Jika jumlah alarm suatu mesin dalam satu shift melebihi rata-rata historis ditambah 2 standar deviasi, supervisor produksi menerima notifikasi terpisah. Mekanisme ini sekaligus membantu mengurangi dampak FAR yang tinggi karena teknisi memiliki konteks tambahan sebelum merespons alarm model. | Supervisor Produksi | Menyediakan fallback manual yang tetap aktif jika model mengalami degradasi, sekaligus mengurangi alarm palsu yang tidak memiliki konfirmasi dari sistem alarm mesin. |
| 3 | Jadwalkan inspeksi `lubricant_level_pct` setiap 7 hari sekali dan tambahkan trigger otomatis jika level turun di bawah 30%. Dokumentasikan hasil inspeksi di sistem maintenance untuk keperluan audit dan pelatihan ulang model. | Tim Maintenance | Mencegah kategori kerusakan akibat gesekan berlebih yang merupakan salah satu penyebab downtime paling umum dan paling murah untuk diatasi melalui inspeksi rutin. |
| 4 | Laksanakan audit menyeluruh terhadap MX-05 di L1 (downtime rate 5.0%) dan mesin-mesin bermasalah di L3 — MX-11 (4.0%) dan MX-07 (3.5%) — dalam 2 minggu ke depan, mencakup pemeriksaan kondisi fisik komponen, kalibrasi sensor, dan tinjauan prosedur operasi standar. | Maintenance Manager + Tim Teknisi Senior | Jika downtime rate mesin-mesin tersebut berhasil diturunkan ke rata-rata global (2.79%), estimasi pengurangan downtime mendadak di L1 dan L3 sebesar 20–40% dalam kuartal berikutnya. |

---

## 11. Risiko Implementasi dan Monitoring

**Model Drift**

Performa model akan menurun seiring waktu karena kondisi mesin berubah akibat penuaan komponen, penggantian suku cadang, atau perubahan pola produksi. Recall yang semula 95.5% dapat turun secara bertahap tanpa disadari. Model harus di-retrain minimal setiap 3 bulan menggunakan data terbaru, dan metrik Recall serta FAR harus dipantau setiap bulan dengan membandingkan prediksi model terhadap kejadian downtime aktual yang tercatat.

**False Alarm Fatigue**

FAR sebesar 42.8% di data test berarti teknisi akan menerima cukup banyak alarm palsu dalam operasional sehari-hari. Jika tidak dikelola, teknisi akan mulai mengabaikan notifikasi dan sistem kehilangan nilainya. Mitigasi yang disarankan: tampilkan skor probabilitas bersama setiap alarm agar teknisi dapat memprioritaskan sendiri, kombinasikan dengan konfirmasi `alarm_count` sebagai filter kedua, dan pantau tingkat respons teknisi terhadap alarm secara berkala. Jika FAR aktual di lapangan konsisten melebihi 50%, pertimbangkan menaikkan threshold ke 0.35 dan evaluasi ulang dampaknya terhadap Recall.

**Ketergantungan pada Kualitas Sensor**

Model sepenuhnya bergantung pada data sensor yang akurat dan terkalibrasi. Sensor yang rusak atau mengirim nilai tidak wajar — seperti pola yang ditemukan pada `vibration_mm_s` (nilai 999 mm/s) selama profiling — akan menghasilkan prediksi yang tidak dapat dipercaya. Perlu ada mekanisme validasi data masuk secara otomatis sebelum diumpankan ke model, serta prosedur yang jelas tentang apa yang harus dilakukan teknisi jika satu atau lebih sensor tidak aktif atau mengirim nilai anomali.

**Kepemilikan Data dan Keamanan**

Data sensor mesin bersifat sensitif karena dapat mengungkapkan kapasitas produksi, pola downtime, dan kondisi aset perusahaan. Akses ke sistem prediksi harus dibatasi berdasarkan peran (teknisi hanya melihat notifikasi per mesin, manajer melihat dashboard agregat), dan data historis harus memiliki kebijakan retensi yang jelas — berapa lama disimpan, siapa yang berwenang mengaksesnya, dan bagaimana prosedur penghapusannya.

**Bias pada Data Historis**

Model dilatih pada data historis yang mencerminkan kondisi dan praktik maintenance masa lalu. Jika ada mesin tertentu yang mendapat perhatian maintenance lebih banyak di masa lalu, model mungkin memiliki performa yang tidak merata antar mesin. Evaluasi Recall dan FAR sebaiknya dilakukan juga per mesin dan per lini — bukan hanya secara agregat — untuk memastikan tidak ada mesin yang secara konsisten luput dari deteksi.