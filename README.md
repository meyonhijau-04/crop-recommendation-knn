# Sistem Rekomendasi Tanaman Berbasis KNN

Aplikasi web berbasis Flask yang menggunakan algoritma
K-Nearest Neighbors (KNN) untuk merekomendasikan jenis
tanaman yang cocok berdasarkan kondisi tanah dan iklim.

---

## Fitur Utama

- Mode Petani — input sederhana berupa pertanyaan,
  tanpa perlu mengetahui nilai teknis N, P, K, pH
- Mode Ahli — input nilai teknis langsung (N, P, K,
  temperature, humidity, pH, rainfall)
- Upload CSV — prediksi banyak data sekaligus
- Download hasil prediksi dalam format CSV dan Excel
- Grafik visualisasi hasil prediksi (radar chart,
  pie chart, bar chart)
- Grafik jurnal resolusi tinggi (confusion matrix,
  elbow method, heatmap korelasi, dll)
- Tampilan modern dengan dark mode dan light mode
- Mendukung 22 jenis tanaman

---

## Struktur Project
crop-recommendation-knn/
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── img/
│       ├── training/
│       ├── prediction/
│       └── tanaman/
├── templates/
│   ├── index.html
│   ├── form_teknis.html
│   ├── form_petani.html
│   ├── result.html
│   ├── result_petani.html
│   ├── result_bulk.html
│   └── about.html
├── dataset/
│   ├── crop_recommendation.csv
│   └── contoh_input.csv
├── uploads/
├── model/
│   └── knn_model.pkl
├── notebook/
│   └── explorasi_data.ipynb
├── app.py
├── train_model.py
├── konversi_petani.py
├── info_tanaman.py
├── requirements.txt
└── README.md

---

## Cara Menjalankan

### 1. Clone Repository
git clone https://github.com/username/crop-recommendation-knn.git
cd crop-recommendation-knn

### 2. Install Library
pip install -r requirements.txt

### 3. Siapkan Dataset
Letakkan file dataset di:
dataset/crop_recommendation.csv

### 4. Training Model
Jalankan perintah berikut untuk melatih model
dan generate grafik:
python train_model.py

Setelah selesai akan muncul:
- File model di `model/knn_model.pkl`
- File scaler di `model/scaler.pkl`
- 6 grafik PNG di `static/img/training/`

### 5. Jalankan Aplikasi
python app.py

### 6. Buka di Browser
http://localhost:5000

---

## Dataset

- Sumber  : Kaggle — Crop Recommendation Dataset
- Penulis : Atharva Ingle
- Total   : 2200 data, 22 jenis tanaman
- Fitur   : N, P, K, temperature, humidity, pH, rainfall
- Link    : https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

---

## Teknologi

- Python 3.10+
- Flask 3.0
- Scikit-Learn 1.4
- Pandas & NumPy
- Matplotlib & Seaborn
- Bootstrap 5
- HTML, CSS, JavaScript

---

## Grafik yang Dihasilkan

### Grafik Jurnal (static/img/training/)
- confusion_matrix.png
- elbow_method.png
- akurasi_per_k.png
- heatmap_korelasi.png
- distribusi_fitur.png
- distribusi_label.png

### Grafik Web (static/img/prediction/)
- Radar chart profil lahan vs rata-rata tanaman
- Pie chart distribusi hasil prediksi bulk
- Bar chart jumlah tanaman hasil prediksi bulk

---

## Deployment

Aplikasi dapat di-deploy ke platform gratis seperti:
- Render  : https://render.com
- Railway : https://railway.app

---

## Pembuat

- Nama      : Selsa Shafana Alfiyani
- NIM       : 301240041
- Program Studi : Teknik Informatika
- Mata Kuliah   : Praktikum Kecerdasan Buatan
- Dosen         : Mohammad Bayu Anggara, S.Kom., M.Kom.
