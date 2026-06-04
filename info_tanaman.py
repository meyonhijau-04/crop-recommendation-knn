# ============================================================
# info_tanaman.py
# Berisi database informasi lengkap untuk setiap tanaman
# yang ada dalam dataset crop_recommendation.csv
# Digunakan oleh app.py untuk menampilkan info di halaman hasil
# ============================================================

# ============================================================
# FORMAT DATA TIAP TANAMAN:
# 'nama_en'        : nama dalam bahasa Inggris (sesuai label dataset)
# 'nama_id'        : nama dalam bahasa Indonesia
# 'deskripsi'      : penjelasan singkat tanaman
# 'waktu_tanam'    : musim atau bulan terbaik untuk menanam
# 'waktu_panen'    : estimasi durasi hingga panen
# 'kebutuhan_air'  : Rendah / Sedang / Tinggi
# 'suhu_ideal'     : rentang suhu terbaik (Celsius)
# 'tips'           : list tips singkat untuk petani
# 'warna_card'     : warna tema card di web (hex)
# ============================================================

INFO_TANAMAN = {

    'rice': {
        'nama_en'      : 'rice',
        'nama_id'      : 'Padi',
        'deskripsi'    : 'Padi adalah tanaman pangan utama Indonesia. '
                         'Tumbuh optimal di lahan basah dengan curah hujan tinggi '
                         'dan suhu hangat.',
        'waktu_tanam'  : 'Musim hujan (Oktober - November) atau musim kemarau '
                         'dengan irigasi cukup (April - Mei)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Tinggi',
        'suhu_ideal'   : '20 - 27 derajat Celsius',
        'tips'         : [
            'Pastikan lahan selalu tergenang air pada awal pertumbuhan',
            'Gunakan pupuk nitrogen (urea) secukupnya',
            'Jaga kebersihan lahan dari gulma',
            'Perhatikan hama wereng dan tikus',
        ],
        'warna_card'   : '#27AE60',
    },

    'maize': {
        'nama_en'      : 'maize',
        'nama_id'      : 'Jagung',
        'deskripsi'    : 'Jagung adalah tanaman serealia yang adaptif di berbagai '
                         'kondisi lahan. Cocok untuk daerah dengan curah hujan sedang.',
        'waktu_tanam'  : 'Awal musim hujan (Oktober - November)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '21 - 30 derajat Celsius',
        'tips'         : [
            'Tanam dengan jarak 70 x 25 cm untuk hasil optimal',
            'Pemupukan nitrogen sangat penting pada fase vegetatif',
            'Hindari genangan air yang berlebihan',
            'Lakukan penyiangan gulma pada 2-4 minggu pertama',
        ],
        'warna_card'   : '#F39C12',
    },

    'chickpea': {
        'nama_en'      : 'chickpea',
        'nama_id'      : 'Kacang Arab',
        'deskripsi'    : 'Kacang arab adalah tanaman legum kaya protein. '
                         'Tahan terhadap kondisi kering dan cocok untuk '
                         'lahan dengan pH netral.',
        'waktu_tanam'  : 'Musim kemarau (Juni - Agustus)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Rendah',
        'suhu_ideal'   : '18 - 26 derajat Celsius',
        'tips'         : [
            'Tidak memerlukan banyak pupuk nitrogen karena dapat mengikat N sendiri',
            'Pastikan drainase lahan baik, tidak boleh tergenang',
            'Cocok ditanam setelah padi sebagai rotasi tanaman',
        ],
        'warna_card'   : '#E67E22',
    },

    'kidneybeans': {
        'nama_en'      : 'kidneybeans',
        'nama_id'      : 'Kacang Merah',
        'deskripsi'    : 'Kacang merah adalah sumber protein nabati yang baik. '
                         'Tumbuh baik di daerah sejuk dengan tanah subur.',
        'waktu_tanam'  : 'Awal musim hujan (Oktober - November)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '18 - 24 derajat Celsius',
        'tips'         : [
            'Tanah harus gembur dan kaya bahan organik',
            'Hindari tanah yang terlalu asam, pH ideal 6.0 - 7.0',
            'Siram secara teratur terutama saat pembungaan',
        ],
        'warna_card'   : '#C0392B',
    },

    'pigeonpeas': {
        'nama_en'      : 'pigeonpeas',
        'nama_id'      : 'Kacang Gude',
        'deskripsi'    : 'Kacang gude adalah tanaman legum tahan kering yang '
                         'banyak dibudidayakan di daerah tropis.',
        'waktu_tanam'  : 'Awal musim hujan (Oktober - November)',
        'waktu_panen'  : '5 - 6 bulan setelah tanam',
        'kebutuhan_air': 'Rendah',
        'suhu_ideal'   : '18 - 29 derajat Celsius',
        'tips'         : [
            'Sangat tahan terhadap kekeringan setelah tumbuh',
            'Tidak perlu banyak pupuk karena bisa mengikat nitrogen',
            'Cocok untuk lahan marginal atau kering',
        ],
        'warna_card'   : '#8E44AD',
    },

    'mothbeans': {
        'nama_en'      : 'mothbeans',
        'nama_id'      : 'Kacang Moth',
        'deskripsi'    : 'Kacang moth adalah tanaman legum yang sangat tahan '
                         'terhadap kondisi panas dan kering.',
        'waktu_tanam'  : 'Musim kemarau (Juni - Agustus)',
        'waktu_panen'  : '2 - 3 bulan setelah tanam',
        'kebutuhan_air': 'Rendah',
        'suhu_ideal'   : '24 - 35 derajat Celsius',
        'tips'         : [
            'Sangat cocok untuk daerah panas dan kering',
            'Tidak memerlukan banyak perawatan',
            'Baik sebagai tanaman penutup tanah',
        ],
        'warna_card'   : '#D35400',
    },

    'mungbean': {
        'nama_en'      : 'mungbean',
        'nama_id'      : 'Kacang Hijau',
        'deskripsi'    : 'Kacang hijau adalah tanaman pangan populer di Indonesia '
                         'dengan umur tanam pendek dan adaptif.',
        'waktu_tanam'  : 'Akhir musim hujan (Februari - Maret)',
        'waktu_panen'  : '2 - 3 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '25 - 35 derajat Celsius',
        'tips'         : [
            'Cocok sebagai tanaman sela atau rotasi setelah padi',
            'Tidak tahan genangan air, pastikan drainase baik',
            'Panen dilakukan bertahap saat polong mulai menghitam',
        ],
        'warna_card'   : '#27AE60',
    },

    'blackgram': {
        'nama_en'      : 'blackgram',
        'nama_id'      : 'Kacang Hitam',
        'deskripsi'    : 'Kacang hitam adalah tanaman legum dengan kandungan '
                         'protein tinggi, adaptif di lahan tropis.',
        'waktu_tanam'  : 'Akhir musim hujan (Februari - Maret)',
        'waktu_panen'  : '2 - 3 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '25 - 35 derajat Celsius',
        'tips'         : [
            'Cocok di tanah lempung berpasir',
            'Hindari lahan yang terlalu asam',
            'Lakukan inokulasi benih dengan bakteri rhizobium',
        ],
        'warna_card'   : '#2C3E50',
    },

    'lentil': {
        'nama_en'      : 'lentil',
        'nama_id'      : 'Lentil',
        'deskripsi'    : 'Lentil adalah tanaman legum kaya protein dan serat '
                         'yang cocok di daerah sejuk dan kering.',
        'waktu_tanam'  : 'Musim dingin atau akhir tahun (November - Desember)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Rendah',
        'suhu_ideal'   : '18 - 24 derajat Celsius',
        'tips'         : [
            'Tidak tahan terhadap suhu tinggi dan kelembapan berlebihan',
            'Tanah harus memiliki drainase yang sangat baik',
            'Cocok sebagai rotasi tanaman dengan serealia',
        ],
        'warna_card'   : '#795548',
    },

    'pomegranate': {
        'nama_en'      : 'pomegranate',
        'nama_id'      : 'Delima',
        'deskripsi'    : 'Delima adalah tanaman buah tahan kering dengan nilai '
                         'ekonomi tinggi. Cocok di daerah panas dan kering.',
        'waktu_tanam'  : 'Musim kemarau (Juni - Agustus)',
        'waktu_panen'  : '5 - 7 bulan setelah tanam (buah pertama 2-3 tahun)',
        'kebutuhan_air': 'Rendah',
        'suhu_ideal'   : '25 - 35 derajat Celsius',
        'tips'         : [
            'Sangat tahan kekeringan setelah pohon dewasa',
            'Pemangkasan rutin meningkatkan hasil buah',
            'pH tanah ideal 5.5 - 7.2',
        ],
        'warna_card'   : '#E74C3C',
    },

    'banana': {
        'nama_en'      : 'banana',
        'nama_id'      : 'Pisang',
        'deskripsi'    : 'Pisang adalah tanaman buah tropis yang sangat populer '
                         'di Indonesia dengan pertumbuhan cepat.',
        'waktu_tanam'  : 'Sepanjang tahun, terbaik awal musim hujan',
        'waktu_panen'  : '9 - 12 bulan setelah tanam',
        'kebutuhan_air': 'Tinggi',
        'suhu_ideal'   : '26 - 30 derajat Celsius',
        'tips'         : [
            'Butuh banyak air tetapi tidak boleh tergenang',
            'Pemupukan kalium sangat penting untuk kualitas buah',
            'Potong daun kering secara rutin',
            'Satu pohon hanya dibiarkan 1-2 anakan produktif',
        ],
        'warna_card'   : '#F1C40F',
    },

    'mango': {
        'nama_en'      : 'mango',
        'nama_id'      : 'Mangga',
        'deskripsi'    : 'Mangga adalah buah tropis favorit Indonesia dengan '
                         'nilai ekonomi tinggi dan perawatan relatif mudah.',
        'waktu_tanam'  : 'Awal musim hujan (Oktober - November)',
        'waktu_panen'  : '3 - 5 bulan setelah berbunga (pohon mulai berbuah 3-5 tahun)',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '24 - 30 derajat Celsius',
        'tips'         : [
            'Perlu musim kering untuk merangsang pembungaan',
            'Pemupukan P dan K penting saat fase generatif',
            'Lakukan penjarangan buah untuk ukuran buah lebih besar',
        ],
        'warna_card'   : '#F39C12',
    },

    'grapes': {
        'nama_en'      : 'grapes',
        'nama_id'      : 'Anggur',
        'deskripsi'    : 'Anggur adalah tanaman buah yang membutuhkan perawatan '
                         'intensif namun memiliki nilai ekonomi sangat tinggi.',
        'waktu_tanam'  : 'Musim kemarau (Juni - Agustus)',
        'waktu_panen'  : '3 - 4 bulan setelah pemangkasan produksi',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '15 - 25 derajat Celsius',
        'tips'         : [
            'Memerlukan penyangga atau pergola untuk merambat',
            'Pemangkasan rutin sangat penting untuk produksi buah',
            'Hindari kelembapan berlebihan untuk mencegah jamur',
            'pH tanah ideal 6.0 - 7.0',
        ],
        'warna_card'   : '#8E44AD',
    },

    'watermelon': {
        'nama_en'      : 'watermelon',
        'nama_id'      : 'Semangka',
        'deskripsi'    : 'Semangka adalah tanaman buah musiman dengan masa tanam '
                         'singkat dan permintaan pasar yang tinggi.',
        'waktu_tanam'  : 'Musim kemarau (Mei - Juli)',
        'waktu_panen'  : '2 - 3 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '25 - 30 derajat Celsius',
        'tips'         : [
            'Butuh sinar matahari penuh minimal 8 jam per hari',
            'Kurangi penyiraman menjelang panen agar buah manis',
            'Gunakan mulsa untuk menjaga kelembapan tanah',
        ],
        'warna_card'   : '#E74C3C',
    },

    'muskmelon': {
        'nama_en'      : 'muskmelon',
        'nama_id'      : 'Melon',
        'deskripsi'    : 'Melon adalah tanaman buah bernilai ekonomi tinggi '
                         'yang cocok untuk pertanian komersial.',
        'waktu_tanam'  : 'Musim kemarau (April - Juni)',
        'waktu_panen'  : '2 - 3 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '25 - 30 derajat Celsius',
        'tips'         : [
            'Sistem irigasi tetes sangat dianjurkan',
            'Satu tanaman idealnya hanya 1-2 buah untuk kualitas terbaik',
            'Pemupukan kalium tinggi menjelang panen meningkatkan rasa manis',
        ],
        'warna_card'   : '#F39C12',
    },

    'apple': {
        'nama_en'      : 'apple',
        'nama_id'      : 'Apel',
        'deskripsi'    : 'Apel cocok di daerah sejuk seperti dataran tinggi '
                         'Indonesia. Membutuhkan perawatan intensif.',
        'waktu_tanam'  : 'Awal musim hujan di dataran tinggi',
        'waktu_panen'  : '4 - 6 bulan setelah pemangkasan produksi',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '16 - 24 derajat Celsius',
        'tips'         : [
            'Cocok di ketinggian 700 - 1200 mdpl',
            'Perlu pemangkasan rutin setiap musim',
            'Pemupukan berimbang N, P, K sangat penting',
            'Lakukan penjarangan buah untuk ukuran optimal',
        ],
        'warna_card'   : '#E74C3C',
    },

    'orange': {
        'nama_en'      : 'orange',
        'nama_id'      : 'Jeruk',
        'deskripsi'    : 'Jeruk adalah buah tropis populer dengan permintaan '
                         'pasar yang stabil dan nilai ekonomi tinggi.',
        'waktu_tanam'  : 'Awal musim hujan (Oktober - November)',
        'waktu_panen'  : '6 - 8 bulan setelah berbunga',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '22 - 30 derajat Celsius',
        'tips'         : [
            'pH tanah ideal 5.5 - 6.5',
            'Pemupukan magnesium penting untuk warna buah',
            'Lakukan pengapuran jika tanah terlalu asam',
            'Perhatikan penyakit CVPD yang umum menyerang jeruk',
        ],
        'warna_card'   : '#E67E22',
    },

    'papaya': {
        'nama_en'      : 'papaya',
        'nama_id'      : 'Pepaya',
        'deskripsi'    : 'Pepaya adalah tanaman buah cepat panen dan mudah '
                         'dibudidayakan di seluruh wilayah Indonesia.',
        'waktu_tanam'  : 'Sepanjang tahun',
        'waktu_panen'  : '9 - 12 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '22 - 30 derajat Celsius',
        'tips'         : [
            'Tidak tahan genangan air, buat bedengan yang cukup tinggi',
            'Pemupukan nitrogen tinggi pada fase vegetatif',
            'Satu lubang tanam idealnya 1 pohon betina dan 1 pohon jantan',
        ],
        'warna_card'   : '#E67E22',
    },

    'coconut': {
        'nama_en'      : 'coconut',
        'nama_id'      : 'Kelapa',
        'deskripsi'    : 'Kelapa adalah tanaman perkebunan ikonik Indonesia '
                         'dengan banyak manfaat dan masa produktif panjang.',
        'waktu_tanam'  : 'Awal musim hujan',
        'waktu_panen'  : '11 - 12 bulan untuk buah (pohon mulai berbuah 5-7 tahun)',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '27 - 30 derajat Celsius',
        'tips'         : [
            'Cocok di daerah pantai dengan kelembapan tinggi',
            'Pemupukan kalium meningkatkan produksi buah',
            'Jarak tanam ideal 9 x 9 meter',
        ],
        'warna_card'   : '#27AE60',
    },

    'cotton': {
        'nama_en'      : 'cotton',
        'nama_id'      : 'Kapas',
        'deskripsi'    : 'Kapas adalah tanaman industri penting untuk bahan '
                         'baku tekstil dengan nilai ekonomi tinggi.',
        'waktu_tanam'  : 'Awal musim kemarau (April - Mei)',
        'waktu_panen'  : '5 - 6 bulan setelah tanam',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '21 - 30 derajat Celsius',
        'tips'         : [
            'Butuh sinar matahari penuh dan drainase baik',
            'Pemupukan nitrogen berlebihan mengurangi kualitas serat',
            'Perhatikan hama ulat bollworm yang sering menyerang',
        ],
        'warna_card'   : '#BDC3C7',
    },

    'jute': {
        'nama_en'      : 'jute',
        'nama_id'      : 'Jute (Rami)',
        'deskripsi'    : 'Jute adalah tanaman serat alam yang digunakan untuk '
                         'karung, tali, dan bahan industri lainnya.',
        'waktu_tanam'  : 'Awal musim hujan (Maret - April)',
        'waktu_panen'  : '3 - 4 bulan setelah tanam',
        'kebutuhan_air': 'Tinggi',
        'suhu_ideal'   : '24 - 35 derajat Celsius',
        'tips'         : [
            'Membutuhkan curah hujan tinggi selama pertumbuhan',
            'Tanah alluvial lembap sangat cocok',
            'Pemanenan dilakukan saat tanaman mulai berbunga',
        ],
        'warna_card'   : '#795548',
    },

    'coffee': {
        'nama_en'      : 'coffee',
        'nama_id'      : 'Kopi',
        'deskripsi'    : 'Kopi adalah komoditas perkebunan unggulan Indonesia '
                         'dengan nilai ekspor tinggi dan permintaan global besar.',
        'waktu_tanam'  : 'Awal musim hujan di dataran tinggi',
        'waktu_panen'  : '6 - 8 bulan setelah berbunga (pohon mulai berbuah 3-4 tahun)',
        'kebutuhan_air': 'Sedang',
        'suhu_ideal'   : '18 - 26 derajat Celsius',
        'tips'         : [
            'Cocok di ketinggian 500 - 1500 mdpl',
            'Butuh pohon naungan untuk kualitas biji terbaik',
            'pH tanah ideal 5.5 - 6.5',
            'Pemangkasan rutin meningkatkan produksi biji',
        ],
        'warna_card'   : '#4A235A',
    },

}

# ============================================================
# FUNGSI HELPER
# ============================================================

def get_info_tanaman(nama_en: str) -> dict:
    """
    Mengambil informasi tanaman berdasarkan nama label dataset.

    Parameter:
        nama_en (str): Nama tanaman dalam bahasa Inggris
                       sesuai label dataset (contoh: 'rice')

    Return:
        dict: Info lengkap tanaman, atau dict default jika tidak ditemukan
    """
    return INFO_TANAMAN.get(nama_en, {
        'nama_en'      : nama_en,
        'nama_id'      : nama_en.capitalize(),
        'deskripsi'    : 'Informasi tanaman belum tersedia.',
        'waktu_tanam'  : '-',
        'waktu_panen'  : '-',
        'kebutuhan_air': '-',
        'suhu_ideal'   : '-',
        'tips'         : [],
        'warna_card'   : '#2E86AB',
    })


def get_semua_tanaman() -> list:
    """
    Mengambil daftar semua tanaman beserta nama Indonesia-nya.
    Digunakan untuk halaman about atau referensi.

    Return:
        list: List of dict berisi nama_en dan nama_id
    """
    return [
        {'nama_en': k, 'nama_id': v['nama_id']}
        for k, v in INFO_TANAMAN.items()
    ]