import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Dashboard Jadwal Vendor", layout="wide")

# --- CUSTOM CSS UNTUK TEMA COKLAT KOPI & LATAR KREM (UPDATED) ---
st.markdown("""
    <style>
        /* 1. Mengubah warna latar belakang halaman utama menjadi krem lembut */
        .stApp {
            background-color: #FDFBF7 !important;
        }
        
        /* 2. Mengubah warna latar belakang sidebar */
        [data-testid="stSidebar"] {
            background-color: #4A3B32 !important;
        }
        
        /* 3. FORCE TOTAL WARNA FONT SIDEBAR agar menyala terang */
        [data-testid="stSidebar"] *, 
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span {
            color: #F5F5DC !important;
        }
        
        /* 4. Menjaga agar tombol hapus di sidebar teksnya tetap putih/terang */
        [data-testid="stSidebar"] button * {
            color: #ffffff !important;
        }
        
        /* 5. Mengubah warna tombol utama (Primary Button) */
        div.stButton > button:first-child {
            background-color: #5C4033;
            color: white;
            border-radius: 5px;
            border: none;
        }
        div.stButton > button:first-child:hover {
            background-color: #3B2F2F;
            color: #D2B48C;
        }
        
        /* 6. Mengubah border form dan warna latar dalamnya agar kontras di atas krem */
        div[data-testid="stForm"] {
            border: 2px solid #8B5A2B;
            border-radius: 10px;
            background-color: #FFFFFF;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# File database sederhana berbasis CSV
DATABASE_FILE = "jadwal_vendor.csv"

# Fungsi untuk membaca data dari CSV
def load_data():
    try:
        df = pd.read_csv(DATABASE_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.strftime('%d/%m/%Y')
        return df
    except:
        return pd.DataFrame(columns=["Tanggal", "Vendor", "Pekerjaan", "Area", "Kebutuhan_Personil", "PIC"])

# Fungsi untuk menyimpan data ke CSV
def save_data(df):
    df.to_csv(DATABASE_FILE, index=False)

# Memuat data aktif
df_jadwal = load_data()

# --- DAFTAR AREA STANDAR ---
LIST_AREA = [
    "ALL", "ALL AREA", "ALL PLANT", "UNIVERSAL",
    "DEK BALKON", "DEK BARU", "DEK HITAM", "DEK KUNING", "DEK SELATAN",
    "GBJ", "SURAMADU", 
    "PRO 1", "PRO 2", "PRO 1 & 2", "UPBM PRO 1", "UPBM PRO 2", "UPBM1",
    "LINE A", "LINE A1", "LINE A2", 
    "LINE B", "LINE B6", 
    "LINE C", "LINE C2", 
    "LINE D", "LINE E", 
    "GSI LINE F", "LINE F", "LINE F1", "LINE F3", "LINE F5", 
    "LINE G", "LINE H", "LINE I", "LINE I4", "LINE J",
    "LINE MANUAL", "LINE REGULER", "LINE UNIVERSAL",
    "LINE A, B, C, D & REGULER", "LINE AB REG", "LINE C & D", "LINE CD",
    "MADHAND", "(BLANK)",
    "LAINNYA (Isi Manual)"
]

# --- DAFTAR PIC STANDAR ---
LIST_PIC = [
    "ABDUL", "AKHMAD", "AMANDA", "ANDIK", "ANDRA", "ANDREW", "ANGGA", 
    "ARI", "ARI ISWORO", "ARIFIN", "ARRYAN", "AZRIEL", "BAMBANG", 
    "CHANAFI", "DIAS", "DWI RIZKI", "EGAR", "EKO", "FADLY", "FAJAR", 
    "FANDI", "FARID", "FERDIAN", "FERDIANSYAH", "GUFRON", "HARDA", 
    "HENGKY", "IAN", "IBNU", "ILHAM", "IMAM", "IRCHAM", "JIMMY", 
    "KHOIRUL ANAM", "MAKSUM", "MUHAJIR", "ORI", "PRAS", "PRIHADIANTO", 
    "PRODUKSI", "RAHMAT", "REDY", "RENDI", "RIZKY AFFANDI W.", 
    "SANCA", "SATRIO", "SLAMET", "SUPARDIYANTO", "SUPRIYADI", "SYAFI'I", 
    "TEGUH", "TRI SUTRISNO", "TRI SUTRISNO WAHYUDI", "TRISBIYANTO", 
    "VIANTO", "YULI",
    "FADLY & ANDRE", "IBNU, SYAFII & MAKSUM", "MUSTOFA & TRISBIYANTO", 
    "RAHMAT & IRCHAM", "VIANTO & YULI", "-",
    "LAINNYA (Isi Manual)"
]

# --- NAVIGASI SIDEBAR ---
st.sidebar.markdown("<h2 style='color: #F5F5DC;'>☕ MENU UTAMA</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Pilih Tampilan:", ["Input Form Jadwal", "Dashboard Tampilan Vendor"])

# --- FITUR GLOBAL: CLEAR DATA ALL DATABASE (SIDEBAR) ---
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Reset Database")
confirm_clear = st.sidebar.checkbox("Saya yakin ingin menghapus SEMUA data")
if st.sidebar.button("🗑️ Kosongkan Semua Data", type="primary"):
    if confirm_clear:
        df_kosong = pd.DataFrame(columns=["Tanggal", "Vendor", "Pekerjaan", "Area", "Kebutuhan_Personil", "PIC"])
        save_data(df_kosong)
        st.sidebar.success("Database berhasil dikosongkan!")
        st.experimental_rerun()
    else:
        st.sidebar.warning("Silakan centang kotak konfirmasi terlebih dahulu!")


# --- MENU 1: INPUT FORM JADWAL ---
if menu == "Input Form Jadwal":
    st.markdown("<h1 style='color: #4A3B32;'>📝 Form Input Penjadwalan Vendor</h1>", unsafe_allow_html=True)
    st.write("Gunakan form di bawah ini untuk menambahkan jadwal baru.")
    
    with st.form(key="form_input", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            tgl_input = st.date_input("Tanggal Pekerjaan", datetime.now())
            vendor_input = st.selectbox("Pilih Vendor", ["Tetuko", "Nata Mulya Abadi", "Tommy", "PRINTECH", "LAINNYA (Isi Manual)"])
            pekerjaan_input = st.text_area("Deskripsi Pekerjaan / Temuan PM")
            
        with col2:
            area_select = st.selectbox("Pilih Area Kerja", LIST_AREA)
            if area_select == "LAINNYA (Isi Manual)":
                area_input = st.text_input("Ketik Nama Area Baru:", placeholder="Contoh: LINE K")
            else:
                area_input = area_select
                
            personil_input = st.number_input("Kebutuhan Personil / Man Power", min_value=1, value=2, step=1)
            
            pic_select = st.selectbox("Pilih PIC", LIST_PIC)
            if pic_select == "LAINNYA (Isi Manual)":
                pic_input = st.text_input("Ketik Nama PIC Baru:", placeholder="Contoh: BUDI SUTEDJO")
            else:
                pic_input = pic_select
            
        submit_button = st.form_submit_button(label="Simpan Jadwal")
        
    if submit_button:
        if pekerjaan_input.strip() == "":
            st.error("Gagal Menyimpan! Kolom 'Pekerjaan' wajib diisi.")
        elif area_select == "LAINNYA (Isi Manual)" and area_input.strip() == "":
            st.error("Gagal Menyimpan! Silakan isi nama area baru pada kolom teks.")
        elif pic_select == "LAINNYA (Isi Manual)" and pic_input.strip() == "":
            st.error("Gagal Menyimpan! Silakan isi nama PIC baru pada kolom teks.")
        else:
            tgl_formatted = tgl_input.strftime('%d/%m/%Y')
            
            new_data = {
                "Tanggal": tgl_formatted,
                "Vendor": vendor_input,
                "Pekerjaan": pekerjaan_input,
                "Area": area_input.strip().upper(),
                "Kebutuhan_Personil": int(personil_input),
                "PIC": pic_input.strip().upper()
            }
            
            df_jadwal = pd.concat([df_jadwal, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df_jadwal)
            st.success(f"Berhasil menambahkan jadwal untuk vendor {vendor_input}!")
            st.experimental_rerun()
            
    st.markdown("<h3 style='color: #4A3B32;'>📋 Semua Data Jadwal Tersimpan</h3>", unsafe_allow_html=True)
    st.dataframe(df_jadwal, use_container_width=True)
    
    csv_data = df_jadwal.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Database ke CSV (Bisa dibuka di Excel)",
        data=csv_data,
        file_name=f"database_jadwal_all_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# --- MENU 2: DASHBOARD TAMPILAN PER VENDOR ---
elif menu == "Dashboard Tampilan Vendor":
    st.markdown("<h1 style='color: #4A3B32;'>🏪 Dashboard Penjadwalan Vendor</h1>", unsafe_allow_html=True)
    
    vendor_terpilih = st.selectbox("Pilih Vendor yang Ingin Dilihat:", ["Tetuko", "Nata Mulya Abadi", "Tommy", "PRINTECH","LAINNYA (Isi Manual)"])
    
    st.markdown(f"<h2 style='text-align: center; background-color: #3B2F2F; color: #D2B48C; padding: 12px; border-radius: 5px; font-family: sans-serif; letter-spacing: 2px;'>SCHEDULE {vendor_terpilih.upper()}</h2>", unsafe_allow_html=True)
    
    col_tgl, _ = st.columns([1, 2])
    with col_tgl:
        tgl_filter = st.date_input("MASUKKAN TANGGAL :", datetime.now())
        tgl_filter_str = tgl_filter.strftime('%d/%m/%Y')
        
    df_jadwal['Original_Index'] = df_jadwal.index
    data_filtered = df_jadwal[(df_jadwal['Vendor'] == vendor_terpilih) & (df_jadwal['Tanggal'] == tgl_filter_str)]
    
    if not data_filtered.empty:
        tabel_tampil = data_filtered[["Pekerjaan", "Area", "PIC", "Kebutuhan_Personil", "Original_Index"]].copy()
        tabel_tampil.columns = ["PEKERJAAN", "AREA", "PIC", "MAN POWER", "Original_Index"]
        tabel_tampil.insert(0, 'NO', range(1, 1 + len(tabel_tampil)))
        
        st.dataframe(tabel_tampil.set_index('NO').drop(columns=["Original_Index"]), use_container_width=True)
        
        col_dl1, col_dl2 = st.columns([1, 2])
        with col_dl1:
            no_hapus = st.selectbox("Pilih NO baris yang ingin dihapus:", tabel_tampil['NO'].tolist())
            if st.button("❌ Hapus Baris Terpilih"):
                idx_asli = tabel_tampil[tabel_tampil['NO'] == no_hapus]['Original_Index'].values[0]
                df_jadwal = df_jadwal.drop(index=idx_asli).drop(columns=["Original_Index"], errors='ignore')
                save_data(df_jadwal)
                st.success(f"Baris Nomor {no_hapus} berhasil dihapus!")
                st.experimental_rerun()
        
        st.markdown(" ")
        csv_filter = tabel_tampil.drop(columns=["NO", "Original_Index"]).to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download Jadwal {vendor_terpilih} Tanggal {tgl_filter_str}",
            data=csv_filter,
            file_name=f"Jadwal_{vendor_terpilih}_{tgl_filter_str.replace('/', '-')}.csv",
            mime="text/csv"
        )
    else:
        st.info(f"Tidak ada jadwal untuk {vendor_terpilih} pada tanggal {tgl_filter_str}. (Hari Libur / Kosong)")
        
    st.markdown("---")
    st.markdown(f"<h3 style='color: #4A3B32;'>➕ Tambah Jadwal Cepat untuk {vendor_terpilih}</h3>", unsafe_allow_html=True)
    with st.expander("Klik di sini untuk mengisi hari libur / jadwal kosong minggu ini"):
        with st.form(key="quick_add", clear_on_submit=False):
            tgl_q = st.date_input("Tanggal", tgl_filter)
            pekerjaan_q = st.text_input("Pekerjaan", placeholder="Contoh: SH1: FOLLOW UP TEMUAN PM...")
            
            area_select_q = st.selectbox("Area", LIST_AREA, key="q_area")
            if area_select_q == "LAINNYA (Isi Manual)":
                area_q = st.text_input("Ketik Nama Area Baru (Form Cepat):")
            else:
                area_q = area_select_q
                
            pic_select_q = st.selectbox("PIC", LIST_PIC, key="q_pic")
            if pic_select_q == "LAINNYA (Isi Manual)":
                pic_q = st.text_input("Ketik Nama PIC Baru (Form Cepat):")
            else:
                pic_q = pic_select_q
                
            mp_q = st.number_input("Man Power", min_value=1, value=2)
            
            btn_q = st.form_submit_button("Simpan Ke Jadwal")
            
            if btn_q:
                if 'Original_Index' in df_jadwal.columns:
                    df_jadwal = df_jadwal.drop(columns=["Original_Index"])
                    
                if pekerjaan_q.strip() == "":
                    st.error("Kolom pekerjaan harus diisi.")
                elif area_select_q == "LAINNYA (Isi Manual)" and area_q.strip() == "":
                    st.error("Silakan isi nama area baru pada kolom teks.")
                elif pic_select_q == "LAINNYA (Isi Manual)" and pic_q.strip() == "":
                    st.error("Silakan isi nama PIC baru pada kolom teks.")
                else:
                    new_row = {
                        "Tanggal": tgl_q.strftime('%d/%m/%Y'),
                        "Vendor": vendor_terpilih,
                        "Pekerjaan": pekerjaan_q,
                        "Area": area_q.strip().upper(),
                        "Kebutuhan_Personil": int(mp_q),
                        "PIC": pic_q.strip().upper()
                    }
                    df_jadwal = pd.concat([df_jadwal, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df_jadwal)
                    st.success("Jadwal Berhasil Ditambahkan!")
                    st.rerun()
                    
