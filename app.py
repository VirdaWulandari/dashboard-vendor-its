import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Dashboard Jadwal Vendor", layout="wide")

# --- CUSTOM CSS UNTUK TEMA COKLAT KOPI & LATAR KREM ---
st.markdown("""
    <style>
        .stApp {
            background-color: #FDFBF7 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #4A3B32 !important;
        }
        [data-testid="stSidebar"] *, 
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span {
            color: #F5F5DC !important;
        }
        [data-testid="stSidebar"] button * {
            color: #ffffff !important;
        }
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
        div[data-baseweb="base-input"],
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] {
            background-color: #EAD8C3 !important;
            border: 1px solid #8B5A2B !important;
            border-radius: 5px !important;
        }
        input, textarea, div[data-baseweb="select"] {
            color: #3B2F2F !important; 
        }
        [data-testid="stDownloadButton"] button {
            background-color: #EAD8C3 !important;
            color: #3B2F2F !important;
            border: 1px solid #8B5A2B !important;
            border-radius: 5px !important;
            font-weight: bold;
        }
        [data-testid="stDownloadButton"] button:hover {
            background-color: #D2B48C !important;
            border-color: #5C4033 !important;
        }
    </style>
""", unsafe_allow_html=True)

# File database sederhana berbasis CSV
DATABASE_FILE = "jadwal_vendor.csv"

# --- FUNGSI LOAD DATA (SUDAH DIPERBAIKI TOTAL) ---
def load_data():
    try:
        df = pd.read_csv(DATABASE_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
        
        df['Vendor'] = df['Vendor'].astype(str).str.strip().str.upper()
        df['Area'] = df['Area'].astype(str).str.strip().str.upper()
        df['PIC'] = df['PIC'].astype(str).str.strip().str.upper()
        return df
    except:
        return pd.DataFrame(columns=["Tanggal", "Vendor", "Pekerjaan", "Area", "Kebutuhan_Personil", "PIC"])

# Fungsi untuk menyimpan data ke CSV
def save_data(df):
    df.to_csv(DATABASE_FILE, index=False)

# Memuat data aktif
df_jadwal = load_data()

# --- DAFTAR SELECTION STANDAR ---
LIST_VENDOR = ["Tetuko", "Nata Mulya Abadi", "Tommy", "PRINTECH", "LAINNYA (Isi Manual)"]
LIST_AREA = ["ALL", "ALL AREA", "ALL PLANT", "UNIVERSAL", "DEK BALKON", "DEK BARU", "DEK HITAM", "DEK KUNING", "DEK SELATAN", "GBJ", "SURAMADU", "PRO 1", "PRO 2", "PRO 1 & 2", "UPBM PRO 1", "UPBM PRO 2", "UPBM1", "LINE A", "LINE A1", "LINE A2", "LINE B", "LINE B6", "LINE C", "LINE C2", "LINE D", "LINE E", "GSI LINE F", "LINE F", "LINE F1", "LINE F3", "LINE F5", "LINE G", "LINE H", "LINE I", "LINE I4", "LINE J", "LINE MANUAL", "LINE REGULER", "LINE UNIVERSAL", "LINE A, B, C, D & REGULER", "LINE AB REG", "LINE C & D", "LINE CD", "MADHAND", "(BLANK)", "LAINNYA (Isi Manual)"]
LIST_PIC = ["ABDUL", "AKHMAD", "AMANDA", "ANDIK", "ANDRA", "ANDREW", "ANGGA", "ARI", "ARI ISWORO", "ARIFIN", "ARRYAN", "AZRIEL", "BAMBANG", "CHANAFI", "DIAS", "DWI RIZKI", "EGAR", "EKO", "FADLY", "FAJAR", "FANDI", "FARID", "FERDIAN", "FERDIANSYAH", "GUFRON", "HARDA", "HENGKY", "IAN", "IBNU", "ILHAM", "IMAM", "IRCHAM", "JIMMY", "KHOIRUL ANAM", "MAKSUM", "MUHAJIR", "ORI", "PRAS", "PRIHADIANTO", "PRODUKSI", "RAHMAT", "REDY", "RENDI", "RIZKY AFFANDI W.", "SANCA", "SATRIO", "SLAMET", "SUPARDIYANTO", "SUPRIYADI", "SYAFI'I", "TEGUH", "TRI SUTRISNO", "TRI SUTRISNO WAHYUDI", "TRISBIYANTO", "VIANTO", "YULI", "FADLY & ANDRE", "IBNU, SYAFII & MAKSUM", "MUSTOFA & TRISBIYANTO", "RAHMAT & IRCHAM", "VIANTO & YULI", "-", "LAINNYA (Isi Manual)"]

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
        st.rerun()
    else:
        st.sidebar.warning("Silakan centang kotak konfirmasi terlebih dahulu!")

# --- MENU 1: INPUT FORM JADWAL ---
if menu == "Input Form Jadwal":
    st.markdown("<h1 style='color: #4A3B32;'>📝 Form Input Penjadwalan Vendor</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        tgl_input = st.date_input("Tanggal Pekerjaan", datetime.now())
        vendor_select = st.selectbox("Pilih Vendor", LIST_VENDOR)
        if vendor_select == "LAINNYA (Isi Manual)":
            vendor_input = st.text_input("✍️ Ketik Nama Vendor Baru di Sini:")
        else:
            vendor_input = vendor_select
        pekerjaan_input = st.text_area("Deskripsi Pekerjaan / Temuan PM")
        
    with col2:
        area_select = st.selectbox("Pilih Area Kerja", LIST_AREA)
        if area_select == "LAINNYA (Isi Manual)":
            area_input = st.text_input("✍️ Ketik Nama Area Baru di Sini:")
        else:
            area_input = area_select
        personil_input = st.number_input("Kebutuhan Personil / Man Power", min_value=1, value=2, step=1)
        pic_select = st.selectbox("Pilih PIC", LIST_PIC)
        if pic_select == "LAINNYA (Isi Manual)":
            pic_input = st.text_input("✍️ Ketik Nama PIC Baru di Sini:")
        else:
            pic_input = pic_select

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Simpan Jadwal"):
        if pekerjaan_input.strip() == "":
            st.error("Gagal Menyimpan! Kolom 'Pekerjaan' wajib diisi.")
        elif vendor_select == "LAINNYA (Isi Manual)" and vendor_input.strip() == "":
            st.error("Gagal Menyimpan! Anda memilih LAINNYA, mohon isi nama Vendor baru pada kolom teks.")
        elif area_select == "LAINNYA (Isi Manual)" and area_input.strip() == "":
            st.error("Gagal Menyimpan! Anda memilih LAINNYA, mohon isi nama Area baru pada kolom teks.")
        elif pic_select == "LAINNYA (Isi Manual)" and pic_input.strip() == "":
            st.error("Gagal Menyimpan! Anda memilih LAINNYA, mohon isi nama PIC baru pada kolom teks.")
        else:
            tgl_formatted = tgl_input.strftime('%d/%m/%Y')
            new_data = {
                "Tanggal": tgl_formatted,
                "Vendor": vendor_input.strip().upper(),
                "Pekerjaan": pekerjaan_input,
                "Area": area_input.strip().upper(),
                "Kebutuhan_Personil": int(personil_input),
                "PIC": pic_input.strip().upper()
            }
            df_jadwal = pd.concat([df_jadwal, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df_jadwal)
            st.success(f"Berhasil menambahkan jadwal untuk vendor {vendor_input.upper()}!")
            st.rerun()
            
    st.markdown("<br><h3 style='color: #4A3B32;'>📋 Semua Data Jadwal Tersimpan</h3>", unsafe_allow_html=True)
    styled_df = df_jadwal.style.set_properties(**{'background-color': '#EAD8C3', 'color': '#3B2F2F', 'border-color': '#8B5A2B'})
    st.dataframe(styled_df, use_container_width=True)
    
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
    
    daftar_vendor_aktif = sorted(list(df_jadwal['Vendor'].unique()))
    for v in ["TETUKO", "NATA MULYA ABADI", "TOMMY", "PRINTECH"]:
        if v not in daftar_vendor_aktif:
            daftar_vendor_aktif.append(v)
            
    vendor_terpilih = st.selectbox("Pilih Vendor yang Ingin Dilihat:", daftar_vendor_aktif)
    
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
        
        df_tampil_bersih = tabel_tampil.set_index('NO').drop(columns=["Original_Index"])
        
        df_tampil_bersih.index = df_tampil_bersih.index.astype(str)
        total_mp = df_tampil_bersih["MAN POWER"].sum()
        df_tampil_bersih.loc['TOTAL'] = ["", "", "TOTAL MAN POWER :", total_mp]
        
        styled_tabel_tampil = df_tampil_bersih.style.set_properties(**{'background-color': '#EAD8C3', 'color': '#3B2F2F', 'border-color': '#8B5A2B'})
        st.dataframe(styled_tabel_tampil, use_container_width=True)
        
        col_dl1, col_dl2 = st.columns([1, 2])
        with col_dl1:
            no_hapus = st.selectbox("Pilih NO baris yang ingin dihapus:", tabel_tampil['NO'].tolist())
            if st.button("❌ Hapus Baris Terpilih"):
                idx_asli = tabel_tampil[tabel_tampil['NO'] == no_hapus]['Original_Index'].values[0]
                df_jadwal = df_jadwal.drop(index=idx_asli).drop(columns=["Original_Index"], errors='ignore')
                save_data(df_jadwal)
                st.success(f"Baris Nomor {no_hapus} berhasil dihapus!")
                st.rerun()
        
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
        tgl_q = st.date_input("Tanggal", tgl_filter)
        pekerjaan_q = st.text_input("Pekerjaan", placeholder="Contoh: SH1: FOLLOW UP TEMUAN PM...")
        
        area_select_q = st.selectbox("Area", LIST_AREA, key="q_area")
        if area_select_q == "LAINNYA (Isi Manual)":
            area_q = st.text_input("✍️ Ketik Nama Area Baru (Form Cepat):")
        else:
            area_q = area_select_q
            
        pic_select_q = st.selectbox("PIC", LIST_PIC, key="q_pic")
        if pic_select_q == "LAINNYA (Isi Manual)":
            pic_q = st.text_input("✍️ Ketik Nama PIC Baru (Form Cepat):")
        else:
            pic_q = pic_select_q
            
        mp_q = st.number_input("Man Power", min_value=1, value=2)
        
        if st.button("🚀 Simpan Ke Jadwal"):
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
