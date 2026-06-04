# ============================================================
# konversi_petani.py
# Berisi logika konversi jawaban pertanyaan sederhana petani
# menjadi nilai numerik N, P, K, temperature, humidity, 
# ph, rainfall yang akan dimasukkan ke model KNN
# ============================================================

# ============================================================
# LOGIKA KONVERSI
# Setiap jawaban petani dipetakan ke rentang nilai numerik
# berdasarkan rata-rata statistik dari dataset
# Referensi nilai diambil dari describe() dataset:
# N    : 0   - 140  (mean ~50)
# P    : 5   - 145  (mean ~53)
# K    : 5   - 205  (mean ~48)
# temp : 8   - 43   (mean ~25)
# hum  : 14  - 99   (mean ~71)
# ph   : 3.5 - 9.9  (mean ~6.5)
# rain : 20  - 298  (mean ~103)
# ============================================================

def konversi_jawaban_petani(jawaban: dict) -> dict:
    """
    Fungsi utama untuk mengkonversi jawaban petani
    ke nilai numerik fitur yang dibutuhkan model KNN.

    Parameter:
        jawaban (dict): Dictionary berisi jawaban petani
                        dari form HTML

    Return:
        dict: Dictionary berisi nilai N, P, K, temperature,
              humidity, ph, rainfall
    """

    # Inisialisasi nilai default (nilai tengah/rata-rata dataset)
    N           = 50.0
    P           = 53.0
    K           = 48.0
    temperature = 25.0
    humidity    = 71.0
    ph          = 6.5
    rainfall    = 103.0

    # --------------------------------------------------------
    # PERTANYAAN 1: Warna tanah
    # Warna tanah mencerminkan kandungan bahan organik
    # dan mineral (N, P, K, ph)
    # --------------------------------------------------------
    warna_tanah = jawaban.get('warna_tanah', '')

    if warna_tanah == 'hitam':
        # Tanah hitam/gelap = kaya bahan organik = N,P,K tinggi
        N  += 30
        P  += 20
        K  += 15
        ph  = 6.8

    elif warna_tanah == 'coklat':
        # Tanah coklat = kandungan organik sedang
        N  += 10
        P  += 10
        K  += 10
        ph  = 6.5

    elif warna_tanah == 'merah':
        # Tanah merah = kandungan besi tinggi, N rendah
        N  -= 10
        P  += 5
        K  += 20
        ph  = 5.8

    elif warna_tanah == 'kuning':
        # Tanah kuning/pucat = miskin nutrisi
        N  -= 20
        P  -= 10
        K  -= 10
        ph  = 5.2

    # --------------------------------------------------------
    # PERTANYAAN 2: Tekstur tanah saat digenggam
    # Tekstur mencerminkan kemampuan tanah menyimpan air
    # dan kandungan mineral
    # --------------------------------------------------------
    tekstur_tanah = jawaban.get('tekstur_tanah', '')

    if tekstur_tanah == 'menggumpal_kuat':
        # Tanah liat/lempung = menyimpan air baik,
        # P dan K cenderung tinggi
        P        += 15
        K        += 10
        humidity += 10
        rainfall += 20

    elif tekstur_tanah == 'menggumpal_hancur':
        # Tanah sedang = seimbang
        P        += 5
        K        += 5
        humidity += 0

    elif tekstur_tanah == 'langsung_hancur':
        # Tanah berpasir = tidak menyimpan air,
        # nutrisi mudah hilang
        P        -= 15
        K        -= 10
        humidity -= 15
        rainfall -= 20

    # --------------------------------------------------------
    # PERTANYAAN 3: Kondisi air di lahan
    # Mencerminkan tingkat kelembapan dan curah hujan
    # --------------------------------------------------------
    kondisi_air = jawaban.get('kondisi_air', '')

    if kondisi_air == 'sering_tergenang':
        humidity += 20
        rainfall += 80
        K        += 10

    elif kondisi_air == 'lembap':
        humidity += 5
        rainfall += 20

    elif kondisi_air == 'cepat_kering':
        humidity -= 20
        rainfall -= 40

    # --------------------------------------------------------
    # PERTANYAAN 4: Cuaca / iklim daerah
    # Mencerminkan suhu dan curah hujan wilayah
    # --------------------------------------------------------
    cuaca = jawaban.get('cuaca', '')

    if cuaca == 'hujan_lebat':
        rainfall    += 100
        humidity    += 15
        temperature -= 3

    elif cuaca == 'hujan_sedang':
        rainfall    += 30
        humidity    += 5
        temperature += 0

    elif cuaca == 'kering':
        rainfall    -= 50
        humidity    -= 20
        temperature += 5

    # --------------------------------------------------------
    # PERTANYAAN 5: Lama penggunaan lahan
    # Lahan lama cenderung kekurangan nutrisi tertentu
    # --------------------------------------------------------
    lama_lahan = jawaban.get('lama_lahan', '')

    if lama_lahan == 'baru':
        # Lahan baru = nutrisi masih alami dan seimbang
        N += 10
        P += 5

    elif lama_lahan == '1_3_tahun':
        # Lahan 1-3 tahun = nutrisi mulai berkurang sedikit
        N -= 5
        P -= 5

    elif lama_lahan == 'lebih_3_tahun':
        # Lahan lama = nutrisi sudah banyak terserap
        N -= 20
        P -= 15
        K -= 10

    # --------------------------------------------------------
    # PERTANYAAN 6: Tanaman sebelumnya
    # Tanaman berbeda menyerap nutrisi berbeda dari tanah
    # --------------------------------------------------------
    tanaman_sebelumnya = jawaban.get('tanaman_sebelumnya', '')

    if tanaman_sebelumnya == 'padi':
        # Padi menyerap N tinggi, meningkatkan kelembapan
        N        -= 15
        K        += 5
        humidity += 5

    elif tanaman_sebelumnya == 'jagung':
        # Jagung menyerap N dan K tinggi
        N -= 10
        K -= 10

    elif tanaman_sebelumnya == 'sayuran':
        # Sayuran menyerap P tinggi
        P -= 10
        N -= 5

    elif tanaman_sebelumnya == 'belum_pernah':
        # Lahan baru = semua nutrisi masih baik
        N += 15
        P += 10
        K += 10

    # --------------------------------------------------------
    # PERTANYAAN 7: Suhu terasa di daerah
    # Estimasi suhu berdasarkan persepsi petani
    # --------------------------------------------------------
    suhu_terasa = jawaban.get('suhu_terasa', '')

    if suhu_terasa == 'panas':
        temperature = 32.0

    elif suhu_terasa == 'sedang':
        temperature = 25.0

    elif suhu_terasa == 'dingin':
        temperature = 15.0

    # --------------------------------------------------------
    # CLIPPING NILAI
    # Pastikan semua nilai berada dalam rentang wajar
    # sesuai batas minimum dan maksimum dataset
    # agar tidak menghasilkan prediksi yang tidak masuk akal
    # --------------------------------------------------------
    N           = float(max(0,   min(140, N)))
    P           = float(max(5,   min(145, P)))
    K           = float(max(5,   min(205, K)))
    temperature = float(max(8,   min(43,  temperature)))
    humidity    = float(max(14,  min(99,  humidity)))
    ph          = float(max(3.5, min(9.9, ph)))
    rainfall    = float(max(20,  min(298, rainfall)))

    # Kembalikan hasil konversi sebagai dictionary
    return {
        'N'          : round(N, 2),
        'P'          : round(P, 2),
        'K'          : round(K, 2),
        'temperature': round(temperature, 2),
        'humidity'   : round(humidity, 2),
        'ph'         : round(ph, 2),
        'rainfall'   : round(rainfall, 2)
    }


# ============================================================
# DAFTAR PERTANYAAN UNTUK FORM PETANI
# Digunakan oleh app.py dan form_petani.html
# ============================================================

PERTANYAAN_PETANI = [
    {
        'id'      : 'warna_tanah',
        'teks'    : 'Bagaimana warna tanah di lahan Anda?',
        'pilihan' : [
            {'nilai': 'hitam',  'label': 'Hitam atau Gelap'},
            {'nilai': 'coklat', 'label': 'Coklat'},
            {'nilai': 'merah',  'label': 'Merah atau Oranye'},
            {'nilai': 'kuning', 'label': 'Kuning atau Pucat'},
        ]
    },
    {
        'id'      : 'tekstur_tanah',
        'teks'    : 'Jika tanah digenggam, apa yang terjadi?',
        'pilihan' : [
            {'nilai': 'menggumpal_kuat',   'label': 'Menggumpal kuat dan tidak mudah pecah'},
            {'nilai': 'menggumpal_hancur', 'label': 'Menggumpal lalu mudah hancur'},
            {'nilai': 'langsung_hancur',   'label': 'Langsung hancur seperti pasir'},
        ]
    },
    {
        'id'      : 'kondisi_air',
        'teks'    : 'Bagaimana kondisi air di lahan Anda?',
        'pilihan' : [
            {'nilai': 'sering_tergenang', 'label': 'Sering tergenang air'},
            {'nilai': 'lembap',           'label': 'Lembap tapi tidak tergenang'},
            {'nilai': 'cepat_kering',     'label': 'Cepat kering setelah hujan'},
        ]
    },
    {
        'id'      : 'cuaca',
        'teks'    : 'Bagaimana cuaca di daerah Anda?',
        'pilihan' : [
            {'nilai': 'hujan_lebat', 'label': 'Sering hujan lebat'},
            {'nilai': 'hujan_sedang','label': 'Hujan sedang'},
            {'nilai': 'kering',      'label': 'Jarang hujan atau kering'},
        ]
    },
    {
        'id'      : 'lama_lahan',
        'teks'    : 'Sudah berapa lama lahan ini digunakan untuk bertani?',
        'pilihan' : [
            {'nilai': 'baru',        'label': 'Baru atau belum pernah ditanami'},
            {'nilai': '1_3_tahun',   'label': '1 sampai 3 tahun'},
            {'nilai': 'lebih_3_tahun','label': 'Lebih dari 3 tahun'},
        ]
    },
    {
        'id'      : 'tanaman_sebelumnya',
        'teks'    : 'Tanaman apa yang terakhir ditanam di lahan ini?',
        'pilihan' : [
            {'nilai': 'padi',         'label': 'Padi'},
            {'nilai': 'jagung',       'label': 'Jagung'},
            {'nilai': 'sayuran',      'label': 'Sayuran'},
            {'nilai': 'belum_pernah', 'label': 'Belum pernah ditanami'},
        ]
    },
    {
        'id'      : 'suhu_terasa',
        'teks'    : 'Bagaimana suhu di daerah Anda sehari-hari?',
        'pilihan' : [
            {'nilai': 'panas',  'label': 'Panas (seperti dataran rendah)'},
            {'nilai': 'sedang', 'label': 'Sedang (tidak terlalu panas/dingin)'},
            {'nilai': 'dingin', 'label': 'Dingin (seperti pegunungan)'},
        ]
    },
]