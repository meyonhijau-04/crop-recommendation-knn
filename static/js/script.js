/* ============================================================
   script.js
   ============================================================ */


/* ============================================================
   DARK / LIGHT MODE
   ============================================================ */

const KUNCI_TEMA = 'tema-aplikasi';

function getTema() {
    return localStorage.getItem(KUNCI_TEMA) || 'light';
}

function terapkanTema(tema) {
    document.documentElement.setAttribute('data-tema', tema);
    localStorage.setItem(KUNCI_TEMA, tema);

    const tombol = document.getElementById('tombol-tema');
    if (tombol) {
        if (tema === 'dark') {
            tombol.innerHTML = '<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707z"/></svg> Terang';
        } else {
            tombol.innerHTML = '<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/></svg> Gelap';
        }
    }
}

function toggleTema() {
    const temaSaat = getTema();
    terapkanTema(temaSaat === 'dark' ? 'light' : 'dark');
}


/* ============================================================
   SLIDER RANGE
   ============================================================ */

function initSlider() {
    const semuaSlider = document.querySelectorAll('.form-range-kustom');

    semuaSlider.forEach(function (slider) {
        const idNilai = slider.getAttribute('data-target-nilai');
        const elNilai = document.getElementById(idNilai);

        if (!elNilai) return;

        elNilai.textContent = parseFloat(slider.value).toFixed(
            parseFloat(slider.step) < 1 ? 2 : 0
        );

        slider.addEventListener('input', function () {
            elNilai.textContent = parseFloat(this.value).toFixed(
                parseFloat(this.step) < 1 ? 2 : 0
            );

            const idInput = this.getAttribute('data-target-input');
            if (idInput) {
                const elInput = document.getElementById(idInput);
                if (elInput) elInput.value = this.value;
            }
        });
    });

    const semuaInput = document.querySelectorAll('.input-sinkron-slider');

    semuaInput.forEach(function (input) {
        input.addEventListener('input', function () {
            const idSlider = this.getAttribute('data-target-slider');
            const idNilai  = this.getAttribute('data-target-nilai');

            if (idSlider) {
                const elSlider = document.getElementById(idSlider);
                if (elSlider) {
                    const min = parseFloat(elSlider.min);
                    const max = parseFloat(elSlider.max);
                    const val = Math.min(max, Math.max(min, parseFloat(this.value) || min));
                    elSlider.value = val;
                }
            }

            if (idNilai) {
                const elNilai = document.getElementById(idNilai);
                if (elNilai) elNilai.textContent = this.value;
            }
        });
    });
}


/* ============================================================
   ISI CONTOH DATA
   ============================================================ */

function isiContohData() {
    const contoh = {
        'N'          : 90,
        'P'          : 42,
        'K'          : 43,
        'temperature': 20.87,
        'humidity'   : 82.00,
        'ph'         : 6.50,
        'rainfall'   : 202.93,
    };

    Object.entries(contoh).forEach(function ([fitur, nilai]) {
        const elInput  = document.getElementById('input-'  + fitur);
        const elSlider = document.getElementById('slider-' + fitur);
        const elNilai  = document.getElementById('nilai-'  + fitur);

        if (elInput)  elInput.value  = nilai;
        if (elSlider) elSlider.value = nilai;
        if (elNilai)  elNilai.textContent = parseFloat(nilai).toFixed(nilai % 1 !== 0 ? 2 : 0);
    });

    tampilkanNotifikasi('Data contoh berhasil diisi.', 'sukses');
}


/* ============================================================
   RESET FORM
   ============================================================ */

function resetForm() {
    const form = document.getElementById('form-teknis');
    if (form) {
        form.reset();
        initSlider();
        tampilkanNotifikasi('Form berhasil dikosongkan.', 'info');
    }
}


/* ============================================================
   UPLOAD CSV — DRAG AND DROP
   ============================================================ */

function initUploadCSV() {
    const areaUpload = document.getElementById('area-upload-csv');
    const inputFile  = document.getElementById('input-file-csv');
    const namaFile   = document.getElementById('nama-file-dipilih');

    if (!areaUpload || !inputFile) return;

    areaUpload.addEventListener('click', function () {
        inputFile.click();
    });

    inputFile.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            tampilkanNamaFile(this.files[0].name);
        }
    });

    areaUpload.addEventListener('dragover', function (e) {
        e.preventDefault();
        this.classList.add('drag-over');
    });

    areaUpload.addEventListener('dragleave', function () {
        this.classList.remove('drag-over');
    });

    areaUpload.addEventListener('drop', function (e) {
        e.preventDefault();
        this.classList.remove('drag-over');

        const file = e.dataTransfer.files[0];
        if (!file) return;

        if (!file.name.toLowerCase().endsWith('.csv')) {
            tampilkanNotifikasi('Hanya file CSV yang diperbolehkan.', 'error');
            return;
        }

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        inputFile.files = dataTransfer.files;

        tampilkanNamaFile(file.name);
    });

    function tampilkanNamaFile(nama) {
        if (namaFile) {
            namaFile.textContent = 'File dipilih: ' + nama;
            namaFile.style.display = 'block';
        }
    }
}


/* ============================================================
   VALIDASI FORM
   ============================================================ */

function validasiFormTeknis() {
    const fiturList = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'];
    let valid = true;
    let pesanError = [];

    fiturList.forEach(function (fitur) {
        const el = document.getElementById('input-' + fitur);
        if (!el) return;

        const nilai = parseFloat(el.value);
        const min   = parseFloat(el.min);
        const max   = parseFloat(el.max);

        if (isNaN(nilai)) {
            pesanError.push(fitur + ' harus diisi dengan angka.');
            valid = false;
        } else if (nilai < min || nilai > max) {
            pesanError.push(fitur + ' harus antara ' + min + ' dan ' + max + '.');
            valid = false;
        }
    });

    if (!valid) tampilkanNotifikasi(pesanError.join(' '), 'error');

    return valid;
}

function validasiFormPetani() {
    const semuaGrup = document.querySelectorAll('.grup-pertanyaan');
    let valid = true;

    semuaGrup.forEach(function (grup) {
        const dipilih = grup.querySelector('input[type="radio"]:checked');
        if (!dipilih) {
            grup.classList.add('pertanyaan-belum-dijawab');
            valid = false;
        } else {
            grup.classList.remove('pertanyaan-belum-dijawab');
        }
    });

    if (!valid) {
        tampilkanNotifikasi('Harap jawab semua pertanyaan sebelum melanjutkan.', 'error');
        const belumDijawab = document.querySelector('.pertanyaan-belum-dijawab');
        if (belumDijawab) {
            belumDijawab.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    return valid;
}

function validasiFormBulk() {
    const inputFile = document.getElementById('input-file-csv');

    if (!inputFile || !inputFile.files || inputFile.files.length === 0) {
        tampilkanNotifikasi('Pilih file CSV terlebih dahulu.', 'error');
        return false;
    }

    if (!inputFile.files[0].name.toLowerCase().endsWith('.csv')) {
        tampilkanNotifikasi('Hanya file CSV yang diperbolehkan.', 'error');
        return false;
    }

    return true;
}


/* ============================================================
   LOADING OVERLAY
   ============================================================ */

function tampilkanLoading(pesan) {
    pesan = pesan || 'Sedang memproses data...';
    const overlay = document.getElementById('overlay-loading');
    const teks    = document.getElementById('loading-teks');
    if (overlay) overlay.classList.add('aktif');
    if (teks)    teks.textContent = pesan;
}

function sembunyikanLoading() {
    const overlay = document.getElementById('overlay-loading');
    if (overlay) overlay.classList.remove('aktif');
}


/* ============================================================
   NOTIFIKASI TOAST
   ============================================================ */

function tampilkanNotifikasi(pesan, tipe) {
    tipe = tipe || 'info';

    const existing = document.getElementById('notifikasi-global');
    if (existing) existing.remove();

    const el = document.createElement('div');
    el.id        = 'notifikasi-global';
    el.className = 'alert-kustom alert-' + tipe;
    el.textContent = pesan;
    el.style.cssText = [
        'position: fixed',
        'top: 80px',
        'right: 20px',
        'z-index: 9998',
        'max-width: 360px',
        'animation: fadeIn 0.3s ease',
        'box-shadow: 0 4px 16px rgba(0,0,0,0.15)',
    ].join(';');

    document.body.appendChild(el);

    setTimeout(function () {
        el.style.opacity    = '0';
        el.style.transition = 'opacity 0.3s ease';
        setTimeout(function () { el.remove(); }, 300);
    }, 3500);
}


/* ============================================================
   ANIMASI PROGRESS BAR
   ============================================================ */

function animasiProgressBar() {
    document.querySelectorAll('.progress-bar-kepercayaan').forEach(function (bar) {
        const target = bar.getAttribute('data-nilai') || '0';
        bar.style.width = '0%';
        setTimeout(function () { bar.style.width = target + '%'; }, 300);
    });

    document.querySelectorAll('.alternatif-bar-fill').forEach(function (bar) {
        const target = bar.getAttribute('data-nilai') || '0';
        bar.style.width = '0%';
        setTimeout(function () { bar.style.width = target + '%'; }, 500);
    });
}


/* ============================================================
   TAB SWITCHING
   ============================================================ */

function initTab() {
    const tombolTab = document.querySelectorAll('.tombol-tab');
    const kontenTab = document.querySelectorAll('.konten-tab');

    if (tombolTab.length === 0) return;

    tombolTab.forEach(function (tombol) {
        tombol.addEventListener('click', function () {
            const target = this.getAttribute('data-tab');

            tombolTab.forEach(function (t) { t.classList.remove('aktif'); });
            kontenTab.forEach(function (k) {
                k.classList.remove('aktif');
                k.style.display = 'none';
            });

            this.classList.add('aktif');
            const elTarget = document.getElementById('tab-' + target);
            if (elTarget) {
                elTarget.classList.add('aktif');
                elTarget.style.display = 'block';
            }
        });
    });

    tombolTab[0].click();
}


/* ============================================================
   SCROLL TO TOP
   ============================================================ */

function initScrollToTop() {
    const tombol = document.getElementById('tombol-scroll-top');
    if (!tombol) return;

    window.addEventListener('scroll', function () {
        tombol.style.display = window.scrollY > 300 ? 'flex' : 'none';
    });

    tombol.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}


/* ============================================================
   INISIALISASI
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    terapkanTema(getTema());

    initSlider();
    initUploadCSV();
    initTab();
    initScrollToTop();
    animasiProgressBar();

    const tombolTema = document.getElementById('tombol-tema');
    if (tombolTema) tombolTema.addEventListener('click', toggleTema);

    const tombolContoh = document.getElementById('tombol-contoh');
    if (tombolContoh) tombolContoh.addEventListener('click', isiContohData);

    const tombolReset = document.getElementById('tombol-reset');
    if (tombolReset) tombolReset.addEventListener('click', resetForm);

    const formTeknis = document.getElementById('form-teknis');
    if (formTeknis) {
        formTeknis.addEventListener('submit', function (e) {
            if (!validasiFormTeknis()) { e.preventDefault(); return; }
            tampilkanLoading('Sedang memproses prediksi...');
        });
    }

    const formPetani = document.getElementById('form-petani');
    if (formPetani) {
        formPetani.addEventListener('submit', function (e) {
            if (!validasiFormPetani()) { e.preventDefault(); return; }
            tampilkanLoading('Sedang menganalisis kondisi lahan...');
        });
    }

    const formBulk = document.getElementById('form-bulk');
    if (formBulk) {
        formBulk.addEventListener('submit', function (e) {
            if (!validasiFormBulk()) { e.preventDefault(); return; }
            tampilkanLoading('Sedang memproses semua data CSV...');
        });
    }

    /* Aktifkan tab bulk jika URL mengandung ?tab=bulk */
    const params = new URLSearchParams(window.location.search);
    if (params.get('tab') === 'bulk') {
        const tombolBulk = document.querySelector('[data-tab="bulk"]');
        if (tombolBulk) tombolBulk.click();
    }

});


/* ============================================================
   CSS ANIMASI TAMBAHAN
   ============================================================ */

const styleAnimasi = document.createElement('style');
styleAnimasi.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-8px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    .pertanyaan-belum-dijawab {
        border        : 1px solid #E74C3C !important;
        border-radius : 12px;
        padding       : 0.5rem;
        animation     : goyangKecil 0.3s ease;
    }

    @keyframes goyangKecil {
        0%   { transform: translateX(0);    }
        25%  { transform: translateX(-5px); }
        75%  { transform: translateX(5px);  }
        100% { transform: translateX(0);    }
    }

    .tombol-tab {
        background   : transparent;
        border       : 1px solid var(--border-warna);
        border-radius: 8px;
        padding      : 0.5rem 1.2rem;
        font-size    : 0.875rem;
        font-weight  : 600;
        color        : var(--teks-sekunder);
        cursor       : pointer;
        transition   : all 0.2s ease;
    }

    .tombol-tab.aktif,
    .tombol-tab:hover {
        background-color : var(--warna-primer);
        border-color     : var(--warna-primer);
        color            : #ffffff;
    }

    #tombol-scroll-top {
        position         : fixed;
        bottom           : 24px;
        right            : 24px;
        width            : 40px;
        height           : 40px;
        background-color : var(--warna-primer);
        border           : none;
        border-radius    : 50%;
        color            : #ffffff;
        cursor           : pointer;
        display          : none;
        align-items      : center;
        justify-content  : center;
        z-index          : 999;
        box-shadow       : 0 4px 12px rgba(46,134,171,0.4);
        transition       : all 0.2s ease;
    }

    #tombol-scroll-top:hover {
        background-color : var(--warna-primer-gelap);
        transform        : translateY(-2px);
    }
`;
document.head.appendChild(styleAnimasi);