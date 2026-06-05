# ============================================================
# app.py
# ============================================================

import os
import uuid
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    jsonify
)
from werkzeug.utils import secure_filename
from konversi_petani import konversi_jawaban_petani, PERTANYAAN_PETANI
from info_tanaman import get_info_tanaman, get_semua_tanaman

# ============================================================
# KONFIGURASI
# ============================================================

app = Flask(__name__)
app.secret_key = 'crop-knn-secret-key-2024'

app.config['UPLOAD_FOLDER']      = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {'csv'}

# ============================================================
# BUAT SEMUA FOLDER YANG DIBUTUHKAN
# Diletakkan di sini agar dieksekusi saat startup
# baik via python app.py maupun via gunicorn (Render/Railway)
# ============================================================

for folder in [
    'uploads',
    'model',
    os.path.join('static', 'img', 'training'),
    os.path.join('static', 'img', 'prediction'),
    os.path.join('static', 'img', 'tanaman'),
    'dataset',
]:
    os.makedirs(folder, exist_ok=True)

# ============================================================
# FILTER JINJA
# ============================================================

@app.template_filter('tojson_safe')
def tojson_safe_filter(data):
    return json.dumps(data, ensure_ascii=False)

# ============================================================
# LOAD MODEL DAN SCALER
# ============================================================

MODEL_PATH  = 'model/knn_model.pkl'
SCALER_PATH = 'model/scaler.pkl'

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model belum ditemukan! Jalankan: python train_model.py"
    )

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(
        "Scaler belum ditemukan! Jalankan: python train_model.py"
    )

model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ============================================================
# KONSTANTA
# ============================================================

FITUR_KOLOM = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

FITUR_LABEL = {
    'N'          : 'Nitrogen (N)',
    'P'          : 'Fosfor (P)',
    'K'          : 'Kalium (K)',
    'temperature': 'Suhu (°C)',
    'humidity'   : 'Kelembapan (%)',
    'ph'         : 'pH Tanah',
    'rainfall'   : 'Curah Hujan (mm)',
}

NILAI_DEFAULT = {
    'N'          : 50,
    'P'          : 53,
    'K'          : 48,
    'temperature': 25.0,
    'humidity'   : 71.0,
    'ph'         : 6.5,
    'rainfall'   : 103.0,
}

FITUR_RANGE = {
    'N'          : {'min': 0,   'max': 140, 'step': 1,    'satuan': ''},
    'P'          : {'min': 5,   'max': 145, 'step': 1,    'satuan': ''},
    'K'          : {'min': 5,   'max': 205, 'step': 1,    'satuan': ''},
    'temperature': {'min': 8,   'max': 43,  'step': 0.1,  'satuan': '°C'},
    'humidity'   : {'min': 14,  'max': 99,  'step': 0.1,  'satuan': '%'},
    'ph'         : {'min': 3.5, 'max': 9.9, 'step': 0.01, 'satuan': ''},
    'rainfall'   : {'min': 20,  'max': 298, 'step': 0.1,  'satuan': 'mm'},
}

# ============================================================
# FUNGSI HELPER
# ============================================================

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def prediksi_satu(nilai_dict):
    input_array = np.array([[
        nilai_dict['N'],
        nilai_dict['P'],
        nilai_dict['K'],
        nilai_dict['temperature'],
        nilai_dict['humidity'],
        nilai_dict['ph'],
        nilai_dict['rainfall'],
    ]])

    input_scaled   = scaler.transform(input_array)
    label_prediksi = model.predict(input_scaled)[0]
    proba          = model.predict_proba(input_scaled)[0]
    kelas          = model.classes_
    proba_dict     = dict(zip(kelas, proba))
    top3           = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    kepercayaan    = proba_dict[label_prediksi] * 100

    return {
        'label'      : label_prediksi,
        'kepercayaan': round(kepercayaan, 2),
        'top3'       : [
            {
                'label'       : t[0],
                'nama_id'     : get_info_tanaman(t[0])['nama_id'],
                'probabilitas': round(t[1] * 100, 2),
            }
            for t in top3
        ],
    }


def generate_grafik_radar(nilai_dict, label):
    # Gunakan nilai min/max hardcoded agar tidak perlu baca CSV
    # dan tidak bergantung pada filesystem saat deployment
    df_min = {
        'N': 0, 'P': 5, 'K': 5,
        'temperature': 8, 'humidity': 14,
        'ph': 3.5, 'rainfall': 20
    }
    df_max = {
        'N': 140, 'P': 145, 'K': 205,
        'temperature': 43, 'humidity': 99,
        'ph': 9.9, 'rainfall': 298
    }
    # Rata-rata global dataset sebagai pembanding
    rata_tanaman = {
        'N': 50.0, 'P': 53.0, 'K': 48.0,
        'temperature': 25.0, 'humidity': 71.0,
        'ph': 6.5, 'rainfall': 103.0
    }

    nilai_user_norm = [
        (nilai_dict[f] - df_min[f]) / (df_max[f] - df_min[f])
        for f in FITUR_KOLOM
    ]
    nilai_rata_norm = [
        (rata_tanaman[f] - df_min[f]) / (df_max[f] - df_min[f])
        for f in FITUR_KOLOM
    ]

    label_fitur = [FITUR_LABEL[f] for f in FITUR_KOLOM]
    N           = len(label_fitur)
    angles      = [n / float(N) * 2 * np.pi for n in range(N)]
    angles     += angles[:1]

    nilai_user_norm += nilai_user_norm[:1]
    nilai_rata_norm += nilai_rata_norm[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    ax.plot(angles, nilai_user_norm, 'o-', linewidth=2,
            color='#2E86AB', label='Input Anda')
    ax.fill(angles, nilai_user_norm, alpha=0.25, color='#2E86AB')

    ax.plot(angles, nilai_rata_norm, 'o-', linewidth=2,
            color='#A23B72',
            label='Rata-rata ' + get_info_tanaman(label)['nama_id'])
    ax.fill(angles, nilai_rata_norm, alpha=0.25, color='#A23B72')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(label_fitur, size=9)
    ax.set_ylim(0, 1)

    plt.title(
        'Profil Lahan vs Rata-rata ' + get_info_tanaman(label)['nama_id'],
        size=12, fontweight='bold', pad=20
    )
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    plt.tight_layout()

    # Pastikan folder ada sebelum simpan
    folder_prediction = os.path.join('static', 'img', 'prediction')
    os.makedirs(folder_prediction, exist_ok=True)

    nama_file   = 'radar_' + uuid.uuid4().hex[:8] + '.png'
    path_simpan = os.path.join(folder_prediction, nama_file)
    plt.savefig(path_simpan, dpi=150, bbox_inches='tight')
    plt.close()

    return nama_file


def generate_grafik_bulk(hasil_list):
    label_counts = {}
    for h in hasil_list:
        nama_id = get_info_tanaman(h['label'])['nama_id']
        label_counts[nama_id] = label_counts.get(nama_id, 0) + 1

    labels = list(label_counts.keys())
    values = list(label_counts.values())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        'Distribusi Hasil Prediksi Rekomendasi Tanaman',
        fontsize=14, fontweight='bold'
    )

    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            startangle=90, pctdistance=0.85)
    ax1.set_title('Proporsi Tanaman (%)', fontsize=12, fontweight='bold')

    warna_bar = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    bars = ax2.barh(labels, values, color=warna_bar, edgecolor='white')
    for bar, val in zip(bars, values):
        ax2.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(val), va='center', fontsize=9
        )
    ax2.set_title('Jumlah per Tanaman', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Jumlah Data')
    ax2.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()

    # Pastikan folder ada sebelum simpan
    folder_prediction = os.path.join('static', 'img', 'prediction')
    os.makedirs(folder_prediction, exist_ok=True)

    nama_file   = 'bulk_' + uuid.uuid4().hex[:8] + '.png'
    path_simpan = os.path.join(folder_prediction, nama_file)
    plt.savefig(path_simpan, dpi=150, bbox_inches='tight')
    plt.close()

    return nama_file

# ============================================================
# ROUTING — HALAMAN UTAMA
# ============================================================

@app.route('/')
def index():
    grafik_training = {
        'confusion_matrix': os.path.join('static', 'img', 'training', 'confusion_matrix.png'),
        'elbow_method'    : os.path.join('static', 'img', 'training', 'elbow_method.png'),
        'akurasi_per_k'   : os.path.join('static', 'img', 'training', 'akurasi_per_k.png'),
        'heatmap_korelasi': os.path.join('static', 'img', 'training', 'heatmap_korelasi.png'),
        'distribusi_fitur': os.path.join('static', 'img', 'training', 'distribusi_fitur.png'),
        'distribusi_label': os.path.join('static', 'img', 'training', 'distribusi_label.png'),
    }

    grafik_tersedia = {
        k: v for k, v in grafik_training.items()
        if os.path.exists(v)
    }

    return render_template('index.html', grafik_training=grafik_tersedia)

# ============================================================
# ROUTING — MODE AHLI
# ============================================================

@app.route('/form-teknis')
def form_teknis():
    return render_template(
        'form_teknis.html',
        fitur_label  = FITUR_LABEL,
        fitur_range  = FITUR_RANGE,
        nilai_default= NILAI_DEFAULT,
    )


@app.route('/prediksi-teknis', methods=['POST'])
def prediksi_teknis():
    try:
        nilai_input = {}
        for fitur in FITUR_KOLOM:
            nilai = float(request.form.get(fitur, 0))
            nilai = max(FITUR_RANGE[fitur]['min'],
                        min(FITUR_RANGE[fitur]['max'], nilai))
            nilai_input[fitur] = nilai

        hasil        = prediksi_satu(nilai_input)
        info         = get_info_tanaman(hasil['label'])
        grafik_radar = generate_grafik_radar(nilai_input, hasil['label'])

        return render_template(
            'result.html',
            nilai_input  = nilai_input,
            fitur_label  = FITUR_LABEL,
            hasil        = hasil,
            info         = info,
            grafik_radar = grafik_radar,
        )

    except Exception as e:
        return render_template(
            'form_teknis.html',
            fitur_label  = FITUR_LABEL,
            fitur_range  = FITUR_RANGE,
            nilai_default= NILAI_DEFAULT,
            error        = 'Terjadi kesalahan: ' + str(e)
        )

# ============================================================
# ROUTING — MODE PETANI
# ============================================================

@app.route('/form-petani')
def form_petani():
    return render_template(
        'form_petani.html',
        pertanyaan=PERTANYAAN_PETANI,
    )


@app.route('/prediksi-petani', methods=['POST'])
def prediksi_petani():
    try:
        jawaban = {}
        for p in PERTANYAAN_PETANI:
            jawaban[p['id']] = request.form.get(p['id'], '')

        nilai_input  = konversi_jawaban_petani(jawaban)
        hasil        = prediksi_satu(nilai_input)
        info         = get_info_tanaman(hasil['label'])
        grafik_radar = generate_grafik_radar(nilai_input, hasil['label'])

        return render_template(
            'result_petani.html',
            jawaban      = jawaban,
            pertanyaan   = PERTANYAAN_PETANI,
            nilai_input  = nilai_input,
            fitur_label  = FITUR_LABEL,
            hasil        = hasil,
            info         = info,
            grafik_radar = grafik_radar,
        )

    except Exception as e:
        return render_template(
            'form_petani.html',
            pertanyaan = PERTANYAAN_PETANI,
            error      = 'Terjadi kesalahan: ' + str(e)
        )

# ============================================================
# ROUTING — UPLOAD CSV
# ============================================================

@app.route('/prediksi-bulk', methods=['POST'])
def prediksi_bulk():
    try:
        if 'file_csv' not in request.files:
            raise ValueError('Tidak ada file yang dipilih.')

        file = request.files['file_csv']

        if file.filename == '':
            raise ValueError('Tidak ada file yang dipilih.')

        if not allowed_file(file.filename):
            raise ValueError('Format file harus CSV.')

        # Pastikan folder uploads ada
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        filename = secure_filename(uuid.uuid4().hex[:8] + '_' + file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df_upload   = pd.read_csv(filepath)
        kolom_wajib = set(FITUR_KOLOM)
        kolom_ada   = set(df_upload.columns)

        if not kolom_wajib.issubset(kolom_ada):
            kolom_kurang = kolom_wajib - kolom_ada
            raise ValueError(
                'Kolom berikut tidak ditemukan: ' + ', '.join(kolom_kurang)
            )

        hasil_list = []
        for idx, row in df_upload.iterrows():
            nilai_dict = {f: float(row[f]) for f in FITUR_KOLOM}
            hasil      = prediksi_satu(nilai_dict)
            info       = get_info_tanaman(hasil['label'])
            hasil_list.append({
                'no'         : idx + 1,
                'input'      : nilai_dict,
                'label'      : hasil['label'],
                'nama_id'    : info['nama_id'],
                'kepercayaan': hasil['kepercayaan'],
            })

        grafik_bulk = generate_grafik_bulk(hasil_list)

        os.remove(filepath)

        return render_template(
            'result_bulk.html',
            hasil_list  = hasil_list,
            total       = len(hasil_list),
            fitur_label = FITUR_LABEL,
            grafik_bulk = grafik_bulk,
        )

    except Exception as e:
        return render_template(
            'form_teknis.html',
            fitur_label  = FITUR_LABEL,
            fitur_range  = FITUR_RANGE,
            nilai_default= NILAI_DEFAULT,
            error        = 'Terjadi kesalahan: ' + str(e)
        )

# ============================================================
# ROUTING — DOWNLOAD
# ============================================================

@app.route('/download-template-csv')
def download_template_csv():
    template_path = os.path.join('dataset', 'contoh_input.csv')

    os.makedirs('dataset', exist_ok=True)

    if not os.path.exists(template_path):
        df_template = pd.DataFrame([
            {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.87,
             'humidity': 82.00, 'ph': 6.50, 'rainfall': 202.93},
            {'N': 85, 'P': 58, 'K': 41, 'temperature': 21.77,
             'humidity': 80.31, 'ph': 7.03, 'rainfall': 226.65},
            {'N': 60, 'P': 55, 'K': 44, 'temperature': 23.00,
             'humidity': 82.32, 'ph': 7.84, 'rainfall': 263.96},
        ])
        df_template.to_csv(template_path, index=False)

    return send_file(
        template_path,
        mimetype     = 'text/csv',
        as_attachment= True,
        download_name= 'template_input_knn.csv'
    )


@app.route('/download-hasil-csv', methods=['POST'])
def download_hasil_csv():
    try:
        data_json = request.form.get('data_hasil', '[]')
        data      = json.loads(data_json)

        rows = []
        for item in data:
            row = item['input'].copy()
            row['Rekomendasi Tanaman'] = item['nama_id']
            row['Kepercayaan (%)']     = item['kepercayaan']
            rows.append(row)

        df_hasil = pd.DataFrame(rows)

        os.makedirs('uploads', exist_ok=True)
        temp_path = os.path.join('uploads', 'hasil_' + uuid.uuid4().hex[:8] + '.csv')
        df_hasil.to_csv(temp_path, index=False)

        response = send_file(
            temp_path,
            mimetype     = 'text/csv',
            as_attachment= True,
            download_name= 'hasil_prediksi_knn.csv'
        )

        @response.call_on_close
        def hapus_file():
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return response

    except Exception as e:
        return 'Error: ' + str(e), 500


@app.route('/download-hasil-excel', methods=['POST'])
def download_hasil_excel():
    try:
        data_json = request.form.get('data_hasil', '[]')
        data      = json.loads(data_json)

        rows = []
        for item in data:
            row = item['input'].copy()
            row['Rekomendasi Tanaman'] = item['nama_id']
            row['Kepercayaan (%)']     = item['kepercayaan']
            rows.append(row)

        df_hasil = pd.DataFrame(rows)

        os.makedirs('uploads', exist_ok=True)
        temp_path = os.path.join('uploads', 'hasil_' + uuid.uuid4().hex[:8] + '.xlsx')

        with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
            df_hasil.to_excel(
                writer,
                sheet_name='Hasil Prediksi KNN',
                index=False
            )

        response = send_file(
            temp_path,
            mimetype=(
                'application/vnd.openxmlformats-officedocument'
                '.spreadsheetml.sheet'
            ),
            as_attachment= True,
            download_name= 'hasil_prediksi_knn.xlsx'
        )

        @response.call_on_close
        def hapus_file():
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return response

    except Exception as e:
        return 'Error: ' + str(e), 500

# ============================================================
# ROUTING — ABOUT
# ============================================================

@app.route('/about')
def about():
    return render_template(
        'about.html',
        semua_tanaman=get_semua_tanaman()
    )

# ============================================================
# ROUTING — API
# ============================================================

@app.route('/api/prediksi', methods=['POST'])
def api_prediksi():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Data JSON tidak ditemukan'}), 400

        for fitur in FITUR_KOLOM:
            if fitur not in data:
                return jsonify({'error': 'Kolom ' + fitur + ' tidak ditemukan'}), 400

        hasil = prediksi_satu(data)
        info  = get_info_tanaman(hasil['label'])

        return jsonify({
            'status'     : 'success',
            'prediksi'   : hasil['label'],
            'nama_id'    : info['nama_id'],
            'kepercayaan': hasil['kepercayaan'],
            'top3'       : hasil['top3'],
            'deskripsi'  : info['deskripsi'],
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# JALANKAN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)