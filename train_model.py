# ============================================================
# train_model.py
# Script untuk melatih model KNN dan generate grafik 
# Jalankan: python train_model.py
# ============================================================

# --- Import Library ---
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Wajib untuk server tanpa display monitor
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# KONFIGURASI PATH
# ============================================================

# Path dataset
DATASET_PATH = 'dataset/crop_recommendation.csv'

# Path untuk menyimpan model
MODEL_PATH = 'model/knn_model.pkl'
SCALER_PATH = 'model/scaler.pkl'

GRAFIK_PATH = 'static/img/training/'

# Pastikan folder tersedia, jika belum ada maka dibuat otomatis
os.makedirs('model', exist_ok=True)
os.makedirs(GRAFIK_PATH, exist_ok=True)
os.makedirs('static/img/prediction', exist_ok=True)
os.makedirs('static/img/tanaman', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# ============================================================
# STEP 1 — MEMUAT DATASET
# ============================================================

print("=" * 50)
print("   TRAINING MODEL KNN - REKOMENDASI TANAMAN")
print("=" * 50)
print()
print("[1] Memuat dataset...")

df = pd.read_csv(DATASET_PATH)

# Tampilkan info dasar dataset di terminal
print(f"    Dataset berhasil dimuat!")
print(f"    Total data     : {df.shape[0]} baris")
print(f"    Total fitur    : {df.shape[1] - 1} fitur")
print(f"    Total tanaman  : {df['label'].nunique()} jenis")
print(f"    Tanaman        : {', '.join(sorted(df['label'].unique()))}")
print(f"    Missing value  : {df.isnull().sum().sum()} (tidak ada)")

# ============================================================
# STEP 2 — PREPROCESSING DATA
# ============================================================

print()
print("[2] Preprocessing & Normalisasi data...")

# Pisahkan fitur (X) dan label (y)
X = df.drop('label', axis=1)  # Semua kolom kecuali label
y = df['label']               # Kolom label sebagai target

# Nama kolom fitur untuk digunakan nanti di grafik
fitur = X.columns.tolist()

# Normalisasi menggunakan MinMaxScaler
# Tujuan: menyamakan skala semua fitur agar KNN tidak bias
# terhadap fitur dengan nilai besar seperti rainfall
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Simpan scaler untuk digunakan saat prediksi di app.py
joblib.dump(scaler, SCALER_PATH)

print(f"    Normalisasi selesai (MinMaxScaler)")
print(f"    Scaler disimpan ke {SCALER_PATH}")

# ============================================================
# STEP 3 — SPLIT DATA TRAINING DAN TESTING
# ============================================================

print()
print("[3] Membagi data training dan testing...")

# Split 80% training, 20% testing
# random_state=42 agar hasil konsisten setiap kali dijalankan
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Stratify agar proporsi tiap kelas seimbang
)

print(f"    Data training  : {X_train.shape[0]} data (80%)")
print(f"    Data testing   : {X_test.shape[0]} data (20%)")

# ============================================================
# STEP 4 — MENCARI NILAI K OPTIMAL (ELBOW METHOD)
# ============================================================

print()
print("[4] Mencari nilai K optimal...")

# Coba nilai K dari 1 sampai 20
k_range = range(1, 21)
akurasi_list = []

for k in k_range:
    knn_temp = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
    knn_temp.fit(X_train, y_train)
    y_pred_temp = knn_temp.predict(X_test)
    akurasi_list.append(accuracy_score(y_test, y_pred_temp))

# Temukan K dengan akurasi tertinggi
k_optimal = k_range[akurasi_list.index(max(akurasi_list))]
akurasi_optimal = max(akurasi_list)

print(f"    K terbaik      : {k_optimal}")
print(f"    Akurasi K={k_optimal}  : {akurasi_optimal * 100:.2f}%")

# ============================================================
# STEP 5 — TRAINING MODEL KNN DENGAN K OPTIMAL
# ============================================================

print()
print(f"[5] Melatih model KNN dengan K={k_optimal}...")

# Buat dan latih model KNN dengan K optimal
# metric='euclidean' sesuai dengan konsep dasar KNN di modul
knn = KNeighborsClassifier(n_neighbors=k_optimal, metric='euclidean')
knn.fit(X_train, y_train)

print(f"    Model berhasil dilatih!")

# ============================================================
# STEP 6 — EVALUASI MODEL
# ============================================================

print()
print("[6] Evaluasi model...")

# Prediksi data testing
y_pred = knn.predict(X_test)

# Hitung metrik evaluasi
akurasi   = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall    = recall_score(y_test, y_pred, average='weighted')
f1        = f1_score(y_test, y_pred, average='weighted')

# Tampilkan hasil evaluasi di terminal
print(f"    Akurasi        : {akurasi * 100:.2f}%")
print(f"    Precision      : {precision * 100:.2f}%")
print(f"    Recall         : {recall * 100:.2f}%")
print(f"    F1-Score       : {f1 * 100:.2f}%")
print()
print("    Classification Report:")
print(classification_report(y_test, y_pred))

# ============================================================
# STEP 7 — MENYIMPAN MODEL
# ============================================================

print("[7] Menyimpan model...")

joblib.dump(knn, MODEL_PATH)

print(f"    Model disimpan ke {MODEL_PATH}")

# ============================================================
# STEP 8 — GENERATE GRAFIK U
# Semua grafik disimpan ke static/img/training/
# ============================================================

print()
print("[8] Generate grafik...")

# Warna palette konsisten untuk semua grafik
WARNA_UTAMA = '#2E86AB'
WARNA_SEKUNDER = '#A23B72'
WARNA_HIJAU = '#27AE60'

# --- GRAFIK 1: Confusion Matrix ---
print("    - Membuat confusion_matrix.png ...")

cm = confusion_matrix(y_test, y_pred, labels=knn.classes_)
plt.figure(figsize=(14, 12))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=knn.classes_,
    yticklabels=knn.classes_,
    linewidths=0.5
)
plt.title(
    f'Confusion Matrix — Model KNN (K={k_optimal})\nAkurasi: {akurasi*100:.2f}%',
    fontsize=14,
    fontweight='bold',
    pad=15
)
plt.xlabel('Prediksi', fontsize=12)
plt.ylabel('Aktual', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("      confusion_matrix.png         ✓")

# --- GRAFIK 2: Elbow Method ---
print("    - Membuat elbow_method.png ...")

plt.figure(figsize=(10, 5))
plt.plot(
    k_range,
    [a * 100 for a in akurasi_list],
    marker='o',
    color=WARNA_UTAMA,
    linewidth=2,
    markersize=6,
    label='Akurasi (%)'
)
# Tandai K optimal dengan garis merah
plt.axvline(
    x=k_optimal,
    color=WARNA_SEKUNDER,
    linestyle='--',
    linewidth=1.5,
    label=f'K Optimal = {k_optimal}'
)
plt.scatter(
    [k_optimal],
    [akurasi_optimal * 100],
    color=WARNA_SEKUNDER,
    s=100,
    zorder=5
)
plt.title(
    'Elbow Method — Pencarian Nilai K Optimal',
    fontsize=14,
    fontweight='bold'
)
plt.xlabel('Nilai K', fontsize=12)
plt.ylabel('Akurasi (%)', fontsize=12)
plt.xticks(k_range)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'elbow_method.png', dpi=300, bbox_inches='tight')
plt.close()
print("      elbow_method.png              ✓")

# --- GRAFIK 3: Akurasi per Nilai K (Bar Chart) ---
print("    - Membuat akurasi_per_k.png ...")

warna_bar = [WARNA_SEKUNDER if k == k_optimal else WARNA_UTAMA for k in k_range]
plt.figure(figsize=(12, 5))
bars = plt.bar(k_range, [a * 100 for a in akurasi_list], color=warna_bar, edgecolor='white')
# Tambahkan label nilai di atas tiap bar
for bar, akr in zip(bars, akurasi_list):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f'{akr*100:.1f}%',
        ha='center',
        va='bottom',
        fontsize=7.5
    )
plt.title(
    'Perbandingan Akurasi Model KNN per Nilai K',
    fontsize=14,
    fontweight='bold'
)
plt.xlabel('Nilai K', fontsize=12)
plt.ylabel('Akurasi (%)', fontsize=12)
plt.xticks(k_range)
plt.ylim(min([a*100 for a in akurasi_list]) - 2, 101)
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'akurasi_per_k.png', dpi=300, bbox_inches='tight')
plt.close()
print("      akurasi_per_k.png             ✓")

# --- GRAFIK 4: Heatmap Korelasi Fitur ---
print("    - Membuat heatmap_korelasi.png ...")

plt.figure(figsize=(9, 7))
korelasi = df[fitur].corr()
mask = np.triu(np.ones_like(korelasi, dtype=bool))  # Sembunyikan segitiga atas agar tidak redundan
sns.heatmap(
    korelasi,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    mask=mask,
    square=True,
    linewidths=0.5,
    annot_kws={'size': 10}
)
plt.title(
    'Heatmap Korelasi Antar Fitur',
    fontsize=14,
    fontweight='bold',
    pad=15
)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'heatmap_korelasi.png', dpi=300, bbox_inches='tight')
plt.close()
print("      heatmap_korelasi.png          ✓")

# --- GRAFIK 5: Distribusi Fitur (Histogram) ---
print("    - Membuat distribusi_fitur.png ...")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle(
    'Distribusi Nilai Setiap Fitur dalam Dataset',
    fontsize=14,
    fontweight='bold',
    y=1.02
)
axes = axes.flatten()
for i, kolom in enumerate(fitur):
    axes[i].hist(df[kolom], bins=30, color=WARNA_UTAMA, edgecolor='white', alpha=0.85)
    axes[i].set_title(kolom.upper(), fontsize=11, fontweight='bold')
    axes[i].set_xlabel('Nilai', fontsize=9)
    axes[i].set_ylabel('Frekuensi', fontsize=9)
    axes[i].grid(True, alpha=0.3)
# Sembunyikan subplot kosong jika fitur kurang dari 8
for j in range(len(fitur), len(axes)):
    axes[j].set_visible(False)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'distribusi_fitur.png', dpi=300, bbox_inches='tight')
plt.close()
print("      distribusi_fitur.png          ✓")

# --- GRAFIK 6: Distribusi Label Tanaman ---
print("    - Membuat distribusi_label.png ...")

label_counts = df['label'].value_counts().sort_values(ascending=True)
plt.figure(figsize=(10, 8))
bars = plt.barh(
    label_counts.index,
    label_counts.values,
    color=WARNA_HIJAU,
    edgecolor='white',
    alpha=0.85
)
# Tambahkan label jumlah di ujung tiap bar
for bar, val in zip(bars, label_counts.values):
    plt.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va='center',
        fontsize=9
    )
plt.title(
    'Distribusi Jumlah Data per Jenis Tanaman',
    fontsize=14,
    fontweight='bold'
)
plt.xlabel('Jumlah Data', fontsize=12)
plt.ylabel('Jenis Tanaman', fontsize=12)
plt.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(GRAFIK_PATH + 'distribusi_label.png', dpi=300, bbox_inches='tight')
plt.close()
print("      distribusi_label.png          ✓")

# ============================================================
# SELESAI
# ============================================================

print()
print("=" * 50)
print("   TRAINING SELESAI!")
print("=" * 50)
print(f"   Model     : {MODEL_PATH}")
print(f"   Scaler    : {SCALER_PATH}")
print(f"   Grafik    : {GRAFIK_PATH}")
print(f"   K Optimal : {k_optimal}")
print(f"   Akurasi   : {akurasi * 100:.2f}%")
print(f"   Precision : {precision * 100:.2f}%")
print(f"   Recall    : {recall * 100:.2f}%")
print(f"   F1-Score  : {f1 * 100:.2f}%")
print("=" * 50)
print("   Model siap digunakan di app.py")
print("=" * 50)