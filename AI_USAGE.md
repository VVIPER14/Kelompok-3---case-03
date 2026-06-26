# AI_USAGE.md

## Ringkasan Penggunaan

- Tools/model yang digunakan: ChatGPT (OpenAI), Claude (Anthropic)
- Bagian yang dibantu AI: pengecekan sintaks kode Python, debugging error,
  saran formulasi kalimat pada ringkasan manajerial dan README
- Bagian yang dikerjakan dan diverifikasi manual oleh kelompok: seluruh
  keputusan analitik mencakup definisi KPI, alasan cleaning, pemilihan fitur,
  pemilihan model, interpretasi metrik, insight EDA, dan rekomendasi operasional

## Log Bantuan AI

| Tanggal | Tujuan | Ringkasan prompt/pertanyaan | Output yang dipakai | Verifikasi manual |
|---|---|---|---|---|
| 14/6/2026 | Pengecekan sintaks matplotlib | Tanya cara menyimpan figure ke path tertentu dengan dpi tertentu | Baris `plt.savefig(...)` | Dicek manual, path disesuaikan dengan struktur folder kelompok |
| 14/6/2026 | Saran kalimat README | Minta saran kalimat untuk bagian problem statement | Draft kalimat | Direvisi seluruhnya oleh kelompok, isi dan argumen tetap dari kelompok |
| 14/6/2026 | Pengecekan sintaks threshold tuning | Tanya cara melakukan sweep threshold dengan confusion matrix | Contoh loop threshold | Logika dan nilai threshold yang dipilih (0.30) diputuskan kelompok berdasarkan hasil aktual |
| 14/6/2026 | Melakukan evaluasi total pada tugas besar yang sudah dibuat manual untuk memaksimalkan nilai yang ingin didapatkan |Lakukan evaluasi pada folder tugas besar, dengan ketentuan evaluasi berdasarkan file yang dilampirkan | Evaluasi Model dan Memperbarui hasil ringkasan manajerial dan file README, lalu evaluasi beberapa bagian pada notebooks seperti insignt data | Keputusan evaluasi bagian insign EDA |
| 15/6/2026 | Pembuatan isi folder src| Buat semua isi folder src bberdasarkan semua folder notebooks | File .py | Dicek apakah sudah sesuai dengan kode yang saya sudah buat di notebooks|
| 16/6/2026 | Perbaikan format readme| Evaluasi dan Format file Readme.md agar bagus | Readme.md | Dicek apakah sudah sesuai dengan output  yang pernah dibuat |

## Pernyataan Kelompok

Kami memahami seluruh keputusan analitik dalam tugas ini, termasuk definisi KPI,
cleaning, pemilihan fitur, model/evaluasi, visualisasi, insight, dan rekomendasi
operasional. Kami siap menjelaskan serta mempertahankan semua bagian tersebut
pada sesi defense.