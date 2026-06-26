# Ringkasan Manajerial — Case 03: Predictive Maintenance

**Kelompok 3 | Teknik Industri**

---

## Problem

Downtime mesin yang tidak terprediksi menyebabkan terhentinya proses produksi
secara mendadak, biaya perbaikan darurat yang jauh lebih mahal dibanding
perawatan terencana, serta gangguan pada jadwal pengiriman. Kondisi saat ini
adalah seluruh penanganan dilakukan secara reaktif — rata-rata response time
lebih dari 2 jam setelah downtime sudah terjadi.

Analisis ini membangun sistem prediksi berbasis data sensor mesin untuk mendeteksi
risiko downtime minimal 24 jam sebelum kejadian, sehingga tim maintenance dapat
bertindak preventif dengan sumber daya yang terencana.

---

## KPI Utama

| KPI | Definisi | Baseline | Target | Hasil Model |
|---|---|---|---|---|
| Recall Downtime | TP / (TP + FN) — dari semua mesin yang benar-benar akan downtime, berapa persen berhasil dideteksi | 0% (tidak ada sistem prediksi) | ≥ 80% | **95.5%** |
| False Alarm Rate | FP / (FP + TN) — dari semua mesin normal, berapa persen salah diprediksi downtime | 0% (tidak ada alarm) | ≤ 30% | **42.8%** |
| Downtime Avoidance | Proporsi downtime yang berhasil dicegah melalui tindakan preventif berbasis prediksi | 0 kejadian | ≥ 50% | **Belum dapat diukur — memerlukan data operasional aktual** |

---

## Hasil Model

Model terpilih adalah **Logistic Regression** dengan threshold 0.30, dilatih menggunakan
temporal split 80:20 (training: 1.920 baris data lebih awal, test: 480 baris data terbaru)
dan SMOTE untuk menangani class imbalance pada training set.

Dari **22 kejadian downtime** yang terjadi di periode test:

- **21 downtime berhasil dideteksi** oleh model lebih dari 24 jam sebelum terjadi,
  memberikan waktu yang cukup bagi teknisi untuk melakukan tindakan preventif terencana.
- **1 downtime tidak terdeteksi** dan berpotensi terjadi mendadak tanpa peringatan.
- **196 alarm palsu** dikirimkan ke teknisi — mesin diprediksi akan downtime namun
  kenyataannya tidak. Ini setara dengan rata-rata sekitar 1–2 pemeriksaan tidak
  perlu per hari kerja, yang masih lebih hemat dibanding 1 kejadian downtime mendadak.

Threshold 0.30 dipilih secara sengaja lebih rendah dari default 0.50 karena biaya
melewatkan satu downtime jauh lebih besar dibanding biaya mengirim teknisi untuk
memeriksa mesin yang ternyata baik-baik saja. Random Forest diuji sebagai pembanding
dan menunjukkan Recall hanya 27.3% pada threshold yang sama — jauh di bawah target —
sehingga Logistic Regression dipilih sebagai model final.

---

## Temuan Utama

**1. alarm_count dan last_maintenance_days adalah sinyal risiko terkuat**

Dari koefisien Logistic Regression, `last_maintenance_days` memiliki bobot terbesar
(|koef| = 0.866) diikuti `alarm_count` (|koef| = 0.713). Dari korelasi Pearson,
`alarm_count` adalah fitur paling berkorelasi dengan downtime (r = 0.182), dengan
median alarm saat downtime (2) dua kali lipat kondisi normal (1). Mesin yang lama
tidak dirawat dan sering memicu alarm adalah kombinasi risiko tertinggi yang harus
diprioritaskan untuk pemeriksaan.

**2. vibration_mm_s dan lubricant_level_pct melengkapi sinyal peringatan dini**

`vibration_mm_s` berada di posisi ketiga pada koefisien LR (|koef| = 0.451) dan
signifikan secara statistik (Mann-Whitney U, p < 0.0001) — median getaran saat
downtime 3.97 mm/s vs 3.35 mm/s kondisi normal. `lubricant_level_pct` berkorelasi
negatif (r = −0.096, p < 0.0001) — median pelumas saat downtime 38.5% jauh lebih
rendah dari kondisi normal 51.4%, konsisten dengan mekanisme fisik gesekan berlebih.

**3. MX-05 dan mesin-mesin di L3 mendominasi downtime rate**

Downtime rate rata-rata global adalah 2.79%. MX-05 di L1 adalah mesin paling
bermasalah (5.0%), hampir dua kali rata-rata global. Di L3, MX-11 (4.0%) dan
MX-07 (3.5%) berada di atas rata-rata. Lini L2 adalah yang paling stabil —
seluruh mesinnya berada di bawah rata-rata global.

**4. FAR 42.8% melampaui target dan harus dikelola aktif**

Dengan threshold 0.30, model menghasilkan 196 alarm palsu dari 458 kondisi normal
di test set. FAR ini melampaui target ≤ 30% dan merupakan trade-off yang disengaja
untuk memaksimalkan Recall. Harus dikelola melalui prioritisasi skor probabilitas
dan edukasi teknisi agar tidak terjadi alarm fatigue.

---

## Rekomendasi Operasional

| # | Rekomendasi | Target Pelaksana | Estimasi Dampak |
|---|---|---|---|
| 1 | Integrasikan output model Logistic Regression ke sistem SCADA atau MES. Kirim notifikasi otomatis ke teknisi ketika probabilitas prediksi melampaui threshold 0.30, diurutkan berdasarkan skor tertinggi. | Tim IT/OT + Maintenance Manager | Dari 22 downtime di periode evaluasi, 21 dapat dideteksi lebih dari 24 jam sebelumnya — memberikan waktu cukup untuk tindakan preventif terencana. |
| 2 | Tetapkan aturan eskalasi `alarm_count` sebagai lapisan peringatan kedua. Jika alarm suatu mesin dalam satu shift melebihi rata-rata historis + 2 standar deviasi, supervisor menerima notifikasi terpisah. | Supervisor Produksi | Menyediakan fallback manual yang aktif jika model mengalami degradasi, sekaligus membantu teknisi memvalidasi alarm sebelum merespons. |
| 3 | Jadwalkan inspeksi `lubricant_level_pct` setiap 7 hari dan tambahkan trigger otomatis jika level turun di bawah 30%. | Tim Maintenance | Mencegah kategori kerusakan akibat gesekan berlebih yang paling mudah dan paling murah dicegah melalui inspeksi rutin. |
| 4 | Laksanakan audit menyeluruh terhadap MX-05 di L1 (5.0%), MX-11 (4.0%) dan MX-07 (3.5%) di L3 dalam 2 minggu ke depan. | Maintenance Manager + Teknisi Senior | Jika downtime rate mesin-mesin tersebut turun ke rata-rata global (2.79%), estimasi pengurangan downtime mendadak di L1 dan L3 sebesar 20–40% dalam kuartal berikutnya. |

---

## Risiko Implementasi

**Model Drift**
Performa model akan menurun seiring waktu karena kondisi mesin berubah akibat
penuaan komponen, penggantian suku cadang, atau perubahan pola produksi. Recall
yang semula 95.5% dapat turun secara bertahap tanpa disadari. Model harus di-retrain
minimal setiap 3 bulan menggunakan data terbaru, dan Recall serta FAR dipantau
setiap bulan.

**False Alarm Fatigue**
FAR sebesar 42.8% berarti teknisi akan menerima cukup banyak alarm palsu dalam
operasional sehari-hari. Tampilkan skor probabilitas bersama setiap alarm agar
teknisi dapat memprioritaskan sendiri. Jika FAR aktual di lapangan konsisten
melebihi 50%, pertimbangkan menaikkan threshold ke 0.35 dan evaluasi ulang
dampaknya terhadap Recall.

**Ketergantungan Kualitas Sensor**
Model sepenuhnya bergantung pada data sensor yang akurat dan terkalibrasi. Sensor
rusak atau nilai tidak wajar — seperti pola `vibration_mm_s` = 999 mm/s yang
ditemukan saat profiling — akan menghasilkan prediksi yang tidak dapat dipercaya.
Perlu mekanisme validasi data masuk otomatis sebelum diumpankan ke model.

**Kepemilikan Data dan Keamanan**
Data sensor mesin mengandung informasi sensitif tentang kapasitas produksi dan
kondisi aset. Akses ke sistem prediksi harus dibatasi berdasarkan peran, dan data
historis harus memiliki kebijakan retensi yang jelas — berapa lama disimpan, siapa
yang berwenang mengakses, dan bagaimana prosedur penghapusannya.

**Bias pada Data Historis**
Model dilatih pada data historis yang mencerminkan kondisi masa lalu. Evaluasi
Recall dan FAR sebaiknya dilakukan per mesin dan per lini — bukan hanya secara
agregat — untuk memastikan tidak ada mesin yang secara konsisten luput dari deteksi.