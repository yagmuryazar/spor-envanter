import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# GİRİŞ ŞİFRESİ VE OTURUM KONTROLÜ
# ==========================================
DOGRU_SIFRE = "Sks1907"  # Belirlediğin güncel şifre

st.set_page_config(
    page_title="FBÜ SKS | Spor Malzemeleri ve Zimmet Portalı", 
    page_icon="🏛️", 
    layout="wide"
)

# Editorial Bej & Vişne CSS Stilleri
st.markdown("""
<style>
    .stApp {
        background-color: #F9F6F0 !important;
        color: #2D2424 !important;
    }
    
    h1, h2, h3, .serif-text {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #630C16 !important;
        font-weight: 600 !important;
    }

    .editorial-header {
        border-bottom: 1.5px solid #E6DCD2;
        padding-bottom: 24px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    .editorial-title {
        font-size: 2.3rem;
        letter-spacing: -0.02em;
        margin: 0;
        color: #630C16;
        font-family: 'Playfair Display', Georgia, serif;
    }
    .editorial-tag {
        background-color: #630C16;
        color: #FAF6F0;
        padding: 6px 18px;
        border-radius: 9999px;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 600;
        display: inline-block;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #EADBCE;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 4px 15px rgba(99, 12, 22, 0.03);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8C7872;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #630C16;
        line-height: 1;
    }

    div.stButton > button[kind="primary"] {
        background-color: #630C16 !important;
        color: #F9F6F0 !important;
        border: 1px solid #630C16 !important;
        border-radius: 9999px !important;
        padding: 8px 26px !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 4px 12px rgba(99, 12, 22, 0.15) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #4A0810 !important;
        border-color: #4A0810 !important;
        transform: translateY(-1px);
    }

    div.stButton > button:not([kind="primary"]) {
        background-color: transparent !important;
        color: #630C16 !important;
        border: 1px solid #C8B6A6 !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
    }
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #F1ECE4 !important;
        border-color: #630C16 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid #E6DCD2;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid #E0D3C5;
        border-radius: 9999px;
        padding: 6px 20px;
        color: #6A5B57;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #630C16 !important;
        border: 1px solid #630C16 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    .stExpander {
        background-color: #FFFFFF !important;
        border: 1px solid #E6DCD2 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Şifre Doğrulama Mantığı
if "giris_yetkisi" not in st.session_state:
    st.session_state.giris_yetkisi = False

def sifre_kontrol():
    if st.session_state.parola_input == DOGRU_SIFRE:
        st.session_state.giris_yetkisi = True
    else:
        st.error("Hatalı parola! Lütfen tekrar deneyin.")

# Kullanıcı giriş yapmadıysa resmi kurumsal giriş kutusu görünür
if not st.session_state.giris_yetkisi:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("""
            <div style="background: #FFFFFF; border: 1.5px solid #E6DCD2; border-radius: 18px; padding: 32px 28px; text-align: center; box-shadow: 0 10px 25px rgba(99, 12, 22, 0.04);">
                <span style="font-size: 2.2rem;">🏛️</span>
                <h2 style="font-family: 'Playfair Display', Georgia, serif; color: #630C16; margin: 10px 0 4px 0;">Fenerbahçe Üniversitesi</h2>
                <h4 style="color: #630C16; margin: 0 0 10px 0; font-weight: 500; font-size: 1.05rem;">Sağlık, Kültür ve Spor Daire Başkanlığı</h4>
                <p style="color: #8C7872; font-size: 0.88rem; margin-bottom: 22px;">Spor Malzemeleri ve Zimmet Takip Portalı</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.text_input("Giriş Parolası:", type="password", key="parola_input", on_change=sifre_kontrol, placeholder="Parolanızı yazın...")
        if st.button("Giriş Yap", type="primary", use_container_width=True):
            sifre_kontrol()
    st.stop()  # Parola doğrulanana kadar aşağıdaki kodları asla çalıştırmaz

# ==========================================
# VERİTABANI BAĞLANTISI VE TABLO KURULUMU
# ==========================================
conn = sqlite3.connect("spor_takim_stok.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS envanter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_adi TEXT,
    beden TEXT,
    toplam_adet INTEGER,
    depoda INTEGER,
    temizlemede INTEGER DEFAULT 0,
    zimmette INTEGER DEFAULT 0
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS temizleme_kayitlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_id INTEGER,
    urun_adi TEXT,
    beden TEXT,
    adet INTEGER,
    gidis_tarihi TEXT,
    durum TEXT,
    notlar TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS zimmet_kayitlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_id INTEGER,
    urun_adi TEXT,
    beden TEXT,
    sporcu_adi TEXT,
    forma_no TEXT,
    adet INTEGER,
    verilis_tarihi TEXT,
    durum TEXT,
    notlar TEXT
)
""")
conn.commit()

# ==========================================
# PANEL BAŞLIĞI VE ÇIKIŞ BUTONU
# ==========================================
header_col1, header_col2 = st.columns([5, 1])
with header_col1:
    st.markdown("""
    <div class="editorial-header">
        <div>
            <h1 class="editorial-title">Spor Malzemeleri ve Zimmet Portalı</h1>
            <p style="margin: 4px 0 0 0; color: #8A7670; font-size: 0.95rem;">Fenerbahçe Üniversitesi Sağlık, Kültür ve Spor Daire Başkanlığı • Spor Birimi</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    st.write("")
    if st.button("Güvenli Çıkış", key="btn_cikis"):
        st.session_state.giris_yetkisi = False
        st.rerun()

# ==========================================
# CANLI METRİK KARTLARI
# ==========================================
stats_df = pd.read_sql("SELECT IFNULL(SUM(toplam_adet),0) as toplam, IFNULL(SUM(depoda),0) as depo, IFNULL(SUM(zimmette),0) as zimmet, IFNULL(SUM(temizlemede),0) as temizleme FROM envanter", conn)
t_toplam = int(stats_df['toplam'].values[0]) if not stats_df.empty else 0
t_depo = int(stats_df['depo'].values[0]) if not stats_df.empty else 0
t_zimmet = int(stats_df['zimmet'].values[0]) if not stats_df.empty else 0
t_temizleme = int(stats_df['temizleme'].values[0]) if not stats_df.empty else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Toplam Koleksiyon</div>
        <div class="metric-value">{t_toplam} <span style="font-size: 0.9rem; font-family: sans-serif; color: #8A7670; font-weight: 500;">Adet</span></div>
    </div>
    """, unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Hazır / Depoda</div>
        <div class="metric-value" style="color: #2F6F4E;">{t_depo} <span style="font-size: 0.9rem; font-family: sans-serif; color: #8A7670; font-weight: 500;">Adet</span></div>
    </div>
    """, unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sporcuda Zimmetli</div>
        <div class="metric-value" style="color: #A34E36;">{t_zimmet} <span style="font-size: 0.9rem; font-family: sans-serif; color: #8A7670; font-weight: 500;">Adet</span></div>
    </div>
    """, unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Kuru Temizlemede</div>
        <div class="metric-value" style="color: #630C16;">{t_temizleme} <span style="font-size: 0.9rem; font-family: sans-serif; color: #8A7670; font-weight: 500;">Adet</span></div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Sekmeler
tab1, tab2, tab3, tab4 = st.tabs([
    "Envanter Özeti", 
    "Sporcu Zimmet", 
    "Kuru Temizleme", 
    "Koleksiyon Yönetimi"
])

BEDEN_SIRASI = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL"]

# ==========================================
# TAB 1: GENEL STOK
# ==========================================
with tab1:
    st.subheader("Ürün & Beden Stok Matrisi")
    envanter_df = pd.read_sql("SELECT * FROM envanter", conn)

    if not envanter_df.empty:
        pivot_depo = pd.pivot_table(
            envanter_df, 
            values='depoda', 
            index=['urun_adi'], 
            columns=['beden'], 
            aggfunc='sum', 
            fill_value=0
        )
        
        mevcut_bedenler = [b for b in BEDEN_SIRASI if b in pivot_depo.columns]
        diger_bedenler = [b for b in pivot_depo.columns if b not in BEDEN_SIRASI]
        pivot_depo = pivot_depo[mevcut_bedenler + diger_bedenler]
        
        ozet_genel = envanter_df.groupby('urun_adi').agg({
            'depoda': 'sum',
            'zimmette': 'sum',
            'temizlemede': 'sum',
            'toplam_adet': 'sum'
        }).rename(columns={
            'depoda': 'Depoda Hazır',
            'zimmette': 'Zimmetli',
            'temizlemede': 'Temizlemede',
            'toplam_adet': 'Genel Toplam'
        })

        birlestirilmis_tablo = pivot_depo.merge(ozet_genel, left_index=True, right_index=True)
        st.dataframe(birlestirilmis_tablo, use_container_width=True)
        st.caption("ℹ️ Tablodaki beden sütunları **Depoda Kullanıma Hazır** stok miktarını gösterir.")

        st.divider()
        st.subheader("Parça Kırılımları")
        for urun in envanter_df['urun_adi'].unique():
            urun_filtre = envanter_df[envanter_df['urun_adi'] == urun]
            toplam_sayi = urun_filtre['toplam_adet'].sum()
            depo_sayi = urun_filtre['depoda'].sum()
            
            with st.expander(f"{urun}  —  [Hazır: {depo_sayi} | Toplam: {toplam_sayi} Adet]"):
                detay_df = urun_filtre[['beden', 'depoda', 'zimmette', 'temizlemede', 'toplam_adet']].rename(columns={
                    'beden': 'Beden',
                    'depoda': 'Depoda Hazır',
                    'zimmette': 'Sporcuda (Zimmet)',
                    'temizlemede': 'Kuru Temizlemede',
                    'toplam_adet': 'Toplam Adet'
                })
                st.dataframe(detay_df, use_container_width=True, hide_index=True)
    else:
        st.info("Koleksiyonda henüz tanımlı ürün bulunmuyor.")

    st.divider()
    st.subheader("Aktif Sporcu Zimmetleri")
    aktif_zimmet_df = pd.read_sql("""
        SELECT 
            sporcu_adi as [Sporcu],
            forma_no as [Forma No],
            urun_adi as [Ürün],
            beden as [Beden],
            adet as [Adet],
            verilis_tarihi as [Veriliş Tarihi],
            notlar as [Açıklama]
        FROM zimmet_kayitlari 
        WHERE durum = 'Zimmetli'
        ORDER BY sporcu_adi ASC
    """, conn)
    
    if not aktif_zimmet_df.empty:
        st.dataframe(aktif_zimmet_df, use_container_width=True)
    else:
        st.info("Şu anda zimmette bir ürün bulunmuyor.")

# ==========================================
# TAB 2: SPORCU ZİMMET
# ==========================================
with tab2:
    z_col1, z_col2 = st.columns(2)

    with z_col1:
        st.subheader("Sporcuya Teslim Et (Zimmetle)")
        hazir_urunler = pd.read_sql("SELECT id, urun_adi, beden, depoda FROM envanter WHERE depoda > 0", conn)

        if not hazir_urunler.empty:
            secenekler_z = {
                f"{r['urun_adi']} [{r['beden']}] — (Hazır: {r['depoda']} adet)": r['id'] 
                for _, r in hazir_urunler.iterrows()
            }
            secilen_z_label = st.selectbox("Teslim Edilecek Parça:", list(secenekler_z.keys()), key="zimmet_secim")
            secilen_z_id = secenekler_z[secilen_z_label]
            max_adet_z = int(hazir_urunler[hazir_urunler['id'] == secilen_z_id]['depoda'].values[0])

            sporcu_ad = st.text_input("Sporcu Adı Soyadı:")
            forma_no = st.text_input("Forma No (Varsa):", placeholder="Örn: 10")
            adet_z = st.number_input("Adet:", min_value=1, max_value=max_adet_z, step=1, key="zimmet_adet")
            not_z = st.text_input("Açıklama / Not:", placeholder="Örn: Sezonluk müsabaka kiti", key="zimmet_not")

            if st.button("Sporcuya Zimmetle", type="primary", use_container_width=True):
                if sporcu_ad.strip():
                    c.execute("UPDATE envanter SET depoda = depoda - ?, zimmette = zimmette + ? WHERE id = ?", (adet_z, adet_z, secilen_z_id))
                    secili_item = hazir_urunler[hazir_urunler['id'] == secilen_z_id].iloc[0]
                    c.execute("""
                        INSERT INTO zimmet_kayitlari (urun_id, urun_adi, beden, sporcu_adi, forma_no, adet, verilis_tarihi, durum, notlar)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'Zimmetli', ?)
                    """, (secilen_z_id, secili_item['urun_adi'], secili_item['beden'], sporcu_ad.strip(), forma_no.strip(), adet_z, str(date.today()), not_z))
                    conn.commit()
                    st.success(f"{sporcu_ad} adlı sporcuya zimmetlendi.")
                    st.rerun()
                else:
                    st.warning("Lütfen sporcu adını yazın.")
        else:
            st.info("Depoda zimmetlenebilecek boşta malzeme yok.")

    with z_col2:
        st.subheader("Sporcudan İade Al")
        bekleyen_zimmetler = pd.read_sql("SELECT * FROM zimmet_kayitlari WHERE durum = 'Zimmetli'", conn)

        if not bekleyen_zimmetler.empty:
            for _, row in bekleyen_zimmetler.iterrows():
                f_no = f" [No: {row['forma_no']}]" if row['forma_no'] else ""
                with st.expander(f"{row['sporcu_adi']}{f_no} — {row['urun_adi']} [{row['beden']}] x{row['adet']}"):
                    st.caption(f"Tarih: {row['verilis_tarihi']} | Not: {row['notlar'] or '-'}")
                    sub_c1, sub_c2 = st.columns(2)
                    with sub_c1:
                        if st.button("Depoya Al (Temiz)", key=f"iade_depo_{row['id']}", use_container_width=True):
                            c.execute("UPDATE envanter SET depoda = depoda + ?, zimmette = zimmette - ? WHERE id = ?", (row['adet'], row['adet'], row['urun_id']))
                            c.execute("UPDATE zimmet_kayitlari SET durum = 'Teslim Alındı' WHERE id = ?", (row['id'],))
                            conn.commit()
                            st.success("Depoya alındı.")
                            st.rerun()
                    with sub_c2:
                        if st.button("Kuru Temizlemeye Sevk Et", key=f"iade_kuru_{row['id']}", use_container_width=True):
                            c.execute("UPDATE envanter SET zimmette = zimmette - ?, temizlemede = temizlemede + ? WHERE id = ?", (row['adet'], row['adet'], row['urun_id']))
                            c.execute("UPDATE zimmet_kayitlari SET durum = 'Kuru Temizlemeye Sevk Edildi' WHERE id = ?", (row['id'],))
                            c.execute("""
                                INSERT INTO temizleme_kayitlari (urun_id, urun_adi, beden, adet, gidis_tarihi, durum, notlar)
                                VALUES (?, ?, ?, ?, ?, 'Temizlemede', ?)
                            """, (row['urun_id'], row['urun_adi'], row['beden'], row['adet'], str(date.today()), f"{row['sporcu_adi']} iadesi"))
                            conn.commit()
                            st.success("Kuru temizlemeye sevk edildi.")
                            st.rerun()
        else:
            st.info("İade bekleyen zimmet bulunmuyor.")

# ==========================================
# TAB 3: KURU TEMİZLEME
# ==========================================
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Kuru Temizlemeye Gönder")
        urunler = pd.read_sql("SELECT id, urun_adi, beden, depoda FROM envanter WHERE depoda > 0", conn)
        
        if not urunler.empty:
            secenekler = {f"{row['urun_adi']} [{row['beden']}] — Depo: {row['depoda']}": row['id'] for _, row in urunler.iterrows()}
            secilen = st.selectbox("Gönderilecek Malzeme:", list(secenekler.keys()), key="temizleme_urun_secimi")
            secilen_id = secenekler[secilen]
            max_adet = int(urunler[urunler['id'] == secilen_id]['depoda'].values[0])
            
            adet = st.number_input("Adet:", min_value=1, max_value=max_adet, step=1, key="kt_adet")
            not_bilgisi = st.text_input("Kuru Temizleme Firması / Açıklama:", key="kt_not")
            
            if st.button("Temizlemeye Gönder", type="primary", use_container_width=True):
                c.execute("UPDATE envanter SET depoda = depoda - ?, temizlemede = temizlemede + ? WHERE id = ?", (adet, adet, secilen_id))
                secilen_row = urunler[urunler['id'] == secilen_id].iloc[0]
                c.execute("""
                INSERT INTO temizleme_kayitlari (urun_id, urun_adi, beden, adet, gidis_tarihi, durum, notlar)
                VALUES (?, ?, ?, ?, ?, 'Temizlemede', ?)
                """, (secilen_id, secilen_row['urun_adi'], secilen_row['beden'], adet, str(date.today()), not_bilgisi))
                conn.commit()
                st.success("Kuru temizlemeye gönderildi.")
                st.rerun()
        else:
            st.info("Depoda ürün kalmadı.")

    with col2:
        st.subheader("Temizlemeden Geri Teslim Al")
        aktif_temizleme = pd.read_sql("SELECT * FROM temizleme_kayitlari WHERE durum = 'Temizlemede'", conn)
        
        if not aktif_temizleme.empty:
            for _, row in aktif_temizleme.iterrows():
                with st.expander(f"{row['urun_adi']} [{row['beden']}] — {row['adet']} Adet"):
                    st.caption(f"Gönderim: {row['gidis_tarihi']} | Not: {row['notlar'] or '-'}")
                    if st.button(f"Temizlendi, Stoğa Al (#{row['id']})", key=f"btn_kt_{row['id']}"):
                        c.execute("UPDATE envanter SET depoda = depoda + ?, temizlemede = temizlemede - ? WHERE id = ?", (row['adet'], row['adet'], row['urun_id']))
                        c.execute("UPDATE temizleme_kayitlari SET durum = 'Teslim Alındı' WHERE id = ?", (row['id'],))
                        conn.commit()
                        st.success("Ürün depoya alındı.")
                        st.rerun()
        else:
            st.info("Temizlemede işlem gören ürün yok.")

# ==========================================
# TAB 4: KOLEKSİYON YÖNETİMİ
# ==========================================
with tab4:
    col_ekle, col_sil = st.columns(2)

    with col_ekle:
        st.subheader("Yeni Koleksiyon Ekle")
        st.caption("Tek seferde tüm beden adetlerini tanımlayabilirsiniz.")
        
        urun_adi_input = st.text_input("Parça Başlığı (örn: Maç Forması, Antrenman Sweat, Eşofman Altı):")
        
        st.write("**Beden Adetleri:**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            adet_xs = st.number_input("XS:", min_value=0, step=1, value=0)
            adet_s  = st.number_input("S:", min_value=0, step=1, value=0)
        with c2:
            adet_m  = st.number_input("M:", min_value=0, step=1, value=0)
            adet_l  = st.number_input("L:", min_value=0, step=1, value=0)
        with c3:
            adet_xl = st.number_input("XL:", min_value=0, step=1, value=0)
            adet_2xl = st.number_input("2XL:", min_value=0, step=1, value=0)
        with c4:
            adet_3xl = st.number_input("3XL:", min_value=0, step=1, value=0)
            adet_4xl = st.number_input("4XL:", min_value=0, step=1, value=0)

        if st.button("Koleksiyonu Kaydet", type="primary", use_container_width=True):
            if urun_adi_input.strip():
                bedenler = {
                    "XS": adet_xs, "S": adet_s, "M": adet_m, 
                    "L": adet_l, "XL": adet_xl, "2XL": adet_2xl,
                    "3XL": adet_3xl, "4XL": adet_4xl
                }
                eklenen_var_mi = False
                for b_ad, b_adet in bedenler.items():
                    if b_adet > 0:
                        c.execute("""
                            INSERT INTO envanter (urun_adi, beden, toplam_adet, depoda, temizlemede, zimmette) 
                            VALUES (?, ?, ?, ?, 0, 0)
                        """, (urun_adi_input.strip(), b_ad, b_adet, b_adet))
                        eklenen_var_mi = True
                
                if eklenen_var_mi:
                    conn.commit()
                    st.success(f"'{urun_adi_input}' başarıyla eklendi!")
                    st.rerun()
                else:
                    st.warning("Lütfen en az bir beden için 1 veya daha fazla adet girin.")
            else:
                st.warning("Lütfen parça başlığını girin.")

    with col_sil:
        st.subheader("Koleksiyondan Çıkar")
        mevcut_urunler = pd.read_sql("SELECT DISTINCT urun_adi FROM envanter", conn)

        if not mevcut_urunler.empty:
            sil_urun = st.selectbox("Silinecek Parça:", mevcut_urunler['urun_adi'].tolist())
            
            st.warning(f"**{sil_urun}** adlı parça tüm bedenleriyle birlikte silinecektir.")
            if st.button(f"'{sil_urun}' Parçasını Sil", type="primary", use_container_width=True):
                c.execute("SELECT id FROM envanter WHERE urun_adi = ?", (sil_urun,))
                ids = [str(r[0]) for r in c.fetchall()]
                if ids:
                    id_listesi = ",".join(ids)
                    c.execute(f"DELETE FROM zimmet_kayitlari WHERE urun_id IN ({id_listesi})")
                    c.execute(f"DELETE FROM temizleme_kayitlari WHERE urun_id IN ({id_listesi})")
                c.execute("DELETE FROM envanter WHERE urun_adi = ?", (sil_urun,))
                conn.commit()

                for k in list(st.session_state.keys()):
                    del st.session_state[k]

                st.toast("Parça başarıyla kaldırıldı.")
                st.rerun()
        else:
            st.info("Kayıtlı ürün bulunmuyor.")

# ==========================================
# SAYFA ALTI İMZA
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="
        border-top: 1.5px solid #E6DCD2; 
        margin-top: 60px; 
        padding-top: 25px; 
        padding-bottom: 25px; 
        text-align: center;
    ">
        <p style="margin: 0; color: #630C16; font-size: 0.95rem; font-family: 'Playfair Display', Georgia, serif; letter-spacing: 0.04em;">
            Designed & Developed by <b>Yağmur Ece Yazar</b>
        </p>
        <p style="margin: 4px 0 0 0; color: #8A7670; font-size: 0.78rem; letter-spacing: 0.05em; text-transform: uppercase;">
            FBÜ Sağlık, Kültür ve Spor Daire Başkanlığı © 2026
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
