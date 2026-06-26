"""
make_dataset.py — Case 03: Predictive Maintenance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Load Data
df = pd.read_csv("../data/raw/dataset_raw.csv")
df.head()

"""| Kolom | Tipe Data | Deskripsi Bisnis |
|---------|---------|---------|
| `timestamp` | Datetime | Waktu observasi kondisi mesin. Digunakan untuk analisis tren dan pola downtime dari waktu ke waktu. |
| `machine_id` | Kategorikal | Identitas unik mesin. Digunakan untuk segmentasi performa dan risiko downtime antar mesin. |
| `line` | Kategorikal | Lini produksi atau area operasi tempat mesin berada. Dapat digunakan untuk membandingkan tingkat risiko antar lini produksi. |
| `age_months` | Numerik | Umur mesin dalam bulan. Semakin tua mesin, semakin besar kemungkinan mengalami penurunan performa dan downtime. |
| `last_maintenance_days` | Numerik | Jumlah hari sejak maintenance terakhir dilakukan. Nilai yang tinggi dapat menunjukkan peningkatan risiko kerusakan karena maintenance yang tertunda. |
| `temp_c` | Numerik | Temperatur operasi mesin (°C). Temperatur tinggi dapat mengindikasikan overheating atau kondisi operasi yang tidak normal. |
| `vibration_mm_s` | Numerik | Tingkat getaran mesin (mm/s). Getaran berlebih sering menjadi indikator awal kerusakan komponen mekanis. |
| `current_a` | Numerik | Arus listrik yang digunakan mesin (Ampere). Nilai abnormal dapat mengindikasikan beban berlebih atau gangguan kelistrikan. |
| `load_pct` | Numerik (%) | Persentase beban operasi mesin terhadap kapasitas maksimalnya. Beban tinggi dalam jangka panjang dapat mempercepat keausan mesin. |
| `lubricant_level_pct` | Numerik (%) | Persentase pelumas yang tersedia pada mesin. Pelumas yang rendah dapat meningkatkan gesekan dan risiko kerusakan komponen. |
| `alarm_count` | Numerik | Jumlah alarm yang muncul selama periode observasi. Semakin banyak alarm dapat menunjukkan kondisi mesin yang tidak stabil. |
| `downtime_next_24h` | Biner (0/1) | Variabel target. Bernilai 1 jika mesin mengalami downtime dalam 24 jam setelah observasi dan 0 jika tidak. |
| `maintenance_ticket_closed` | Kategorikal/Numerik | Status penyelesaian tiket maintenance. Informasi ini baru diketahui setelah maintenance dilakukan sehingga berpotensi menyebabkan data leakage jika digunakan sebagai fitur model. |
| `failure_mode` | Kategorikal | Jenis kegagalan mesin yang terjadi. Berguna untuk analisis akar penyebab kerusakan, namun perlu dievaluasi karena kemungkinan baru diketahui setelah downtime terjadi. |
"""

# Lihat ringkasan informasi tiap kolom
df.info()

"""> Ringkasan
- Total baris: 2.400 entri (index 0–2399)
- Total kolom: 14
- hampir semua kolom sudah sesuai dengan format/type data kecuali timestamp yang mana seharusnya type data datetime
- ada indikasi missing value di kolom lubricant_level_pct karena jumlah baris tidak sama dengan bari kolom lain di mana seharusnya ada 2400 baris namun pada kolom tersebut hanya 2328 baris
"""

# Lihat nilai statistika deskriptif tiap kolom
df.describe()

"""> Ringkasan
- Adanya nilai ekstrem/outlier pada kolom vibration_mm_s, di mana nilai median 3.37, sedangkan nilai max 999.00
- Adanya data invalid pada load_pct, dapat dilihat pada nilai maxnya yakni 105% yang mana ini tidak masuk akal, karena seharusnya nilai maxnya adalah 100%
"""

# Melihat jumlah data duplikat
df.duplicated().sum()

"""> Ringkasan
- Dapat dilihat pada pengecekan duplikat pada data set, tidak terdapat satu pun baris yang duplikat
"""

# Melihat jumlah data kosong
df.isnull().sum()

"""> Ringkasan
- Dapat dilihat juga, pengecekan ulang untuk missing value pada data. Terdapat 72 baris yang missing value pada lubricant_level_pct
"""

# Cek Outlier
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for col, ax in zip(df.select_dtypes(include='number').columns, axes):
    Q1    = df[col].quantile(0.25)
    Q3    = df[col].quantile(0.75)
    IQR   = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_out = ((df[col] < lower) | (df[col] > upper)).sum()

    sns.boxplot(y=df[col], ax=ax, color='steelblue', flierprops=dict(marker='o', color='red', markersize=4))
    ax.set_title(f"{col}\n({n_out} outlier)", fontsize=10)
    ax.set_xlabel('')

plt.suptitle('Distribusi & Outlier Tiap Kolom Numerik', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

"""> Ringkasan
- Terdapat outlier di beberapa kolom, seoerti tempt_c, lalu vibration_mm_s, current_a,load_pct, dan alarm_count
"""

# Pengecekan proporsi target
df['downtime_next_24h'].value_counts()

"""> Ringkasan
- Proporsi data antara mesin yang kondisi normal(0) dan mengalami downtime(1) tidak seimbang, sehingga data mengalami imbalance

# Cleaning
"""

# Hapus Kolom Tak perlu
df = df.drop(columns=['maintenance_ticket_closed', 'failure_mode'])

"""Kedua kolom ini dihapus dikarenakan hanya tersedia **setelah** downtime terjadi(data leakage):
- failure_mode → diisi teknisi setelah mendiagnosis kerusakan
- maintenance_ticket_closed → tiket baru ada setelah mesin rusak dan ditangani

di mana akan menyebabkan model menjadi buruk jika tidak di hapus
"""

# Hapus Missing Value
df['lubricant_level_pct'] = df.groupby('machine_id')['lubricant_level_pct'].transform(
    lambda x: x.fillna(x.median())
)

"""Missing value pada lubricant_level_pct ditangani dengan mengisi menggunakan nilai median per machine_id, bukan dihapus.
Alasannya karena data sensor mesin bersifat time-series operasional setiap baris merepresentasikan kondisi mesin pada satu waktu tertentu. Jika baris yang memiliki missing value dihapus, kita kehilangan informasi kondisi mesin pada timestamp tersebut, padahal kolom-kolom lain seperti temp_c, vibration_mm_s, dan alarm_count pada baris yang sama masih valid dan berharga untuk analisis.

Penggunaan median per mesin dipilih karena setiap mesin memiliki karakteristik pelumas yang berbeda, sehingga nilai yang diisikan lebih merepresentasikan kondisi normal mesin itu sendiri dibanding median global seluruh dataset.
"""

# Menangani Data Invalid
df['load_pct'] = df['load_pct'].clip(upper=100)

"""Data invalid pada load_pct (nilai > 100%) ditangani dengan .clip(upper=100), bukan dihapus.
Alasannya karena nilai di atas 100% pada persentase beban mesin kemungkinan besar adalah kesalahan pembacaan sensor, bukan kondisi yang benar-benar tidak mungkin terjadi secara fisik. Mesin bisa saja sesaat beroperasi sedikit di atas kapasitas nominal, namun sensor mencatat nilai yang sedikit melebihi batas karena toleransi kalibrasi atau noise.
Dengan .clip(upper=100), nilai yang melebihi batas domain valid dikembalikan ke nilai maksimum yang masuk akal (100%), sehingga informasi bahwa mesin sedang dalam kondisi beban tinggi tetap dipertahankan. Jika baris tersebut dihapus, kita justru kehilangan data kondisi beban tinggi yang berpotensi sangat relevan untuk memprediksi downtime.
"""

# Menangani Outlier
vib_upper = df['vibration_mm_s'].quantile(0.99)
df['vibration_mm_s'] = df['vibration_mm_s'].clip(upper=vib_upper)

"""Outlier pada vibration_mm_s ditangani dengan .clip(upper=percentile 99) karena nilai ekstrem seperti 999 mm/s kemungkinan besar adalah noise sensor, bukan kondisi nyata mesin. Namun datanya tidak dihapus karena kolom lain pada baris tersebut tetap valid dan sayang untuk dibuang."""

# Ubah Format
df['timestamp'] = pd.to_datetime(df['timestamp'])

"""Hal ini dilakukan karena timestamp adalah data waktu, sehingga di perlukan format ulang menjadi type datetime"""

# Simpan Data Bersih
df.to_csv("../data/processed/dataset_clean.csv", index=False)

"""## Changelog Cleaning

| # | Kolom | Masalah | Tindakan | Alasan |
|---|-------|---------|----------|--------|
| 1 | `maintenance_ticket_closed`, `failure_mode` | Data leakage | Dihapus | Tersedia hanya setelah downtime terjadi |
| 2 | `lubricant_level_pct` | 72 missing values | Imputasi median per `machine_id` | Data sensor time-series — baris tidak boleh dihapus; median per mesin lebih representatif dari median global |
| 3 | `load_pct` | Nilai > 100% (error sensor) | `.clip(upper=100)` | Nilai di atas batas domain dikembalikan ke batas valid; data kondisi beban tinggi dipertahankan |
| 4 | `vibration_mm_s` | Outlier ekstrem (999 mm/s = error sensor) | `.clip(upper=percentil_99)` | Noise sensor, bukan kondisi nyata; baris lain tetap valid |
| 5 | `timestamp` | Tipe object, bukan datetime | `pd.to_datetime()` | Diperlukan untuk analisis temporal |
"""

# ── Sanity Check setelah Cleaning ─────────────────────────────────────────────
print("=" * 55)
print("SANITY CHECK — Verifikasi hasil cleaning")
print("=" * 55)

# Load ulang dari file yang sudah disimpan untuk memastikan hasil benar-benar tersimpan
df_check = pd.read_csv("../data/processed/dataset_clean.csv", parse_dates=["timestamp"])

# 1. Tidak ada missing value tersisa
missing = df_check.isnull().sum()
print("\n1. Missing value tersisa:")
if missing.sum() == 0:
    print("   OK — tidak ada missing value.")
else:
    print(missing[missing > 0])

# 2. load_pct tidak ada yang melebihi 100
invalid_load = (df_check["load_pct"] > 100).sum()
print(f"\n2. Nilai load_pct > 100: {invalid_load}")
print(f"   {'OK — tidak ada nilai invalid.' if invalid_load == 0 else 'MASIH ADA — perlu diperiksa ulang.'}")

# 3. vibration_mm_s sudah di-clip, tidak boleh ada nilai ekstrem seperti 999
vib_max = df_check["vibration_mm_s"].max()
print(f"\n3. Nilai maksimum vibration_mm_s setelah clipping: {vib_max:.2f} mm/s")
print(f"   {'OK — nilai ekstrem sudah ditangani.' if vib_max < 100 else 'PERLU DIPERIKSA — nilai masih terlalu tinggi.'}")

# 4. Kolom leakage sudah tidak ada
leaked_cols = [c for c in ["maintenance_ticket_closed", "failure_mode"] if c in df_check.columns]
print(f"\n4. Kolom leakage tersisa: {leaked_cols if leaked_cols else 'tidak ada'}")
print(f"   {'OK — kolom leakage sudah dihapus.' if not leaked_cols else 'PERINGATAN — kolom leakage masih ada.'}")

# 5. Tipe data timestamp sudah datetime
ts_type = df_check["timestamp"].dtype
print(f"\n5. Tipe data timestamp: {ts_type}")
print(f"   {'OK — sudah datetime.' if str(ts_type).startswith('datetime') else 'PERINGATAN — belum dikonversi ke datetime.'}")

# 6. Jumlah baris dan kolom final
print(f"\n6. Dimensi dataset bersih: {df_check.shape[0]} baris x {df_check.shape[1]} kolom")
print(f"   (dari 2400 baris awal, 14 kolom awal -> 2400 baris, 12 kolom setelah 2 kolom leakage dihapus)")

# 7. Distribusi target tidak berubah
print(f"\n7. Distribusi target downtime_next_24h:")
vc = df_check["downtime_next_24h"].value_counts()
for k, v in vc.items():
    print(f"   Kelas {k}: {v} baris ({v/len(df_check)*100:.1f}%)")

print("\n" + "=" * 55)
print("Sanity check selesai.")
print("=" * 55)