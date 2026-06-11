import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
st.set_page_config(
    page_title="E-Ticaret Dashboard",
    page_icon="📊",
    layout="wide"
)


# Veri yükleme
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

orders = pd.read_csv(os.path.join(BASE_DIR, "data/olist_orders_dataset.csv"))
items = pd.read_csv(os.path.join(BASE_DIR, "data/olist_order_items_dataset.csv"))
products = pd.read_csv(os.path.join(BASE_DIR, "data/olist_products_dataset.csv"))
customers = pd.read_csv(
    os.path.join(BASE_DIR, "data/olist_customers_dataset.csv")
)

geolocation = pd.read_csv(
    os.path.join(BASE_DIR, "data/olist_geolocation_dataset.csv")
)

# Merge
df = pd.merge(orders, items, on="order_id")
df = pd.merge(df, products, on="product_id")
df = pd.merge(df, customers, on="customer_id")

# Kategori isimlerini çevirme
category_translation = {
"beleza_saude": "Sağlık & Güzellik",
"informatica_acessorios": "Teknoloji",
"automotivo": "Otomotiv",
"cama_mesa_banho": "Ev Tekstili",
"moveis_decoracao": "Mobilya & Dekorasyon",
"esporte_lazer": "Spor & Outdoor",
"utilidades_domesticas": "Ev Gereçleri",
"relogios_presentes": "Saat & Hediye",
"cool_stuff": "Teknolojik Ürünler",
"ferramentas_jardim": "Bahçe & Araç Gereç",
"agro_industria_e_comercio": "Tarım ve Ticaret",
"alimentos": "Gıda",
"alimentos_bebidas": "Gıda ve İçecek",
"artes": "Sanat",
"artes_e_artesanato": "El Sanatları",
"artigos_de_festas": "Parti Ürünleri",
"artigos_de_natal": "Yılbaşı Ürünleri",
"audio": "Ses Sistemleri",
"bebes": "Bebek",
"bebidas": "İçecek",
"brinquedos": "Oyuncak",
"casa_conforto": "Ev Konforu",
"casa_conforto_2": "Ev Konforu 2",
"casa_construcao": "Yapı Malzemeleri",
"cds_dvds_musicais": "CD & DVD",
"cine_foto": "Fotoğrafçılık",
"climatizacao": "İklimlendirme",
"consoles_games": "Oyun Konsolları",
"construcao_ferramentas_construcao": "İnşaat Araçları",
"construcao_ferramentas_ferramentas": "El Aletleri",
"construcao_ferramentas_iluminacao": "Aydınlatma",
"construcao_ferramentas_jardim": "Bahçe Aletleri",
"construcao_ferramentas_seguranca": "Güvenlik Sistemleri",
"dvds_blu_ray": "Blu-ray & DVD",
"eletrodomesticos": "Beyaz Eşya",
"eletrodomesticos_2": "Beyaz Eşya 2",
"eletronicos": "Elektronik",
"eletroportateis": "Küçük Ev Aletleri",
"fashion_bolsas_e_acessorios": "Çanta ve Aksesuar",
"fashion_calcados": "Ayakkabı",
"fashion_esporte": "Spor Giyim",
"fashion_roupa_feminina": "Kadın Giyim",
"fashion_roupa_infanto_juvenil": "Çocuk Giyim",
"fashion_roupa_masculina": "Erkek Giyim",
"fashion_underwear_e_moda_praia": "İç Giyim & Plaj",
"flores": "Çiçek",
"fraldas_higiene": "Bebek Bakımı",
"industria_comercio_e_negocios": "İş Dünyası",
"instrumentos_musicais": "Müzik Aletleri",
"la_cuisine": "Mutfak",
"livros_importados": "İthal Kitaplar",
"livros_interesse_geral": "Genel Kitaplar",
"livros_tecnicos": "Teknik Kitaplar",
"malas_acessorios": "Valiz & Aksesuar",
"market_place": "Pazar Yeri",
"moveis_colchao_e_estofado": "Mobilya & Yatak",
"moveis_cozinha_area_de_servico_jantar_e_jardim": "Mutfak & Bahçe Mobilyası",
"moveis_escritorio": "Ofis Mobilyaları",
"moveis_quarto": "Yatak Odası",
"moveis_sala": "Oturma Odası",
"musica": "Müzik",
"papelaria": "Kırtasiye",
"pc_gamer": "Oyuncu Bilgisayarı",
"pcs": "Bilgisayar",
"perfumaria": "Parfüm",
"pet_shop": "Evcil Hayvan",
"portateis_casa_forno_e_cafe": "Kahve & Mutfak",
"portateis_cozinha_e_preparadores_de_alimentos": "Mutfak Aletleri",
"seguros_e_servicos": "Sigorta & Hizmet",
"sinalizacao_e_seguranca": "İş Güvenliği",
"tablets_impressao_imagem": "Tablet & Yazıcı",
"telefonia": "Telefon",
"telefonia_fixa": "Sabit Telefon",
}

df["product_category_name"] = df["product_category_name"].replace(category_translation)

# Yeni kolon
df["total_price"] = df["price"] + df["freight_value"]


# 🔥(FİLTRE KISMI)
st.sidebar.header("Filtreler")

# Kategori seçimi
categories = df["product_category_name"].dropna().unique()

selected_category = st.sidebar.selectbox(
    "Kategori seç",
    ["Tümü"] + list(categories)
)

# Filtre uygula
if selected_category != "Tümü":
    df = df[df["product_category_name"] == selected_category]


df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input(
    "Tarih seç",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

df = df[
    (df["order_purchase_timestamp"] >= pd.to_datetime(date_range[0])) &
    (df["order_purchase_timestamp"] <= pd.to_datetime(date_range[1]))
]


if df.empty:
    st.warning("⚠️ Seçilen tarih aralığında veri bulunamadı. Veri seti 2016-2018 yıllarını kapsamaktadır.")
    st.stop()
    
df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"]
)
df["order_estimated_delivery_date"] = pd.to_datetime(
    df["order_estimated_delivery_date"]
)
df["is_delayed"] = (
    df["order_delivered_customer_date"]
    > df["order_estimated_delivery_date"]
)
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days

# KPI hesapla
total_revenue = df["total_price"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = total_revenue / total_orders

# Yönetici Özeti Verileri

top_category = (
    df.groupby("product_category_name")["total_price"]
    .sum()
    .idxmax()
)

top_city = (
    df.groupby("customer_city")["total_price"]
    .sum()
    .idxmax()
)

delay_rate = (
    df["is_delayed"].mean() * 100
)

# Başlık
st.title("📊 Olist E-Ticaret İş Zekası Paneli")

st.caption(
    "Satış, müşteri davranışı ve lojistik performans analizi"
)

# KPI göster

st.markdown("""
<style>
.kpi-card {
    background-color: #1e1e1e;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(79,195,247,0.2);

    margin: 12px;
}

.kpi-title {
    font-size: 18px;
    color: #bbbbbb;
}

.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: #4FC3F7;
}
</style>
""", unsafe_allow_html=True)
st.markdown("## 📌 Genel Performans")

col1, col2, col3, col4 = st.columns(4) 
col5, col6, col7 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Toplam Gelir</div>
        <div class="kpi-value">{total_revenue:,.0f} ₺</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Toplam Sipariş</div>
        <div class="kpi-value">{total_orders}</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Ortalama Sipariş</div>
        <div class="kpi-value">{avg_order_value:.2f} ₺</div>
    </div>
    """, unsafe_allow_html=True)

avg_delivery = df["delivery_days"].mean()

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Ortalama Teslimat</div>
        <div class="kpi-value">{avg_delivery:.1f} Gün</div>
    </div>
    """, unsafe_allow_html=True)

delayed_orders = df["is_delayed"].sum()
delay_rate = (delayed_orders / total_orders) * 100
top_category = (
    df.groupby("product_category_name")["total_price"]
    .sum()
    .idxmax()
)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Geciken Sipariş</div>
        <div class="kpi-value">{delayed_orders}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Gecikme Oranı</div>
        <div class="kpi-value">%{delay_rate:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
with col7:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">En Karlı Kategori</div>
        <div class="kpi-value">{top_category}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

st.markdown("## 📌 Yönetici Özeti")

st.info(f"""
💰 Toplam Gelir: {total_revenue:,.0f} ₺

📦 Toplam Sipariş: {total_orders}

🏆 En Karlı Kategori: {top_category}

🌍 En Güçlü Şehir: {top_city}

🚚 Gecikme Oranı: %{delay_rate:.1f}
""")



# Tarih formatı
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

monthly_sales = df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))["total_price"].sum()
monthly_sales = monthly_sales.reset_index()
monthly_sales["order_purchase_timestamp"] = monthly_sales["order_purchase_timestamp"].astype(str)

# Grafik
st.markdown("## 📈 Satış Analizi")
fig = px.line(
    monthly_sales,
    x="order_purchase_timestamp",
    y="total_price",
    title="📈 Aylık Satış Trendi",
    labels={
        "order_purchase_timestamp": "Tarih",
        "total_price": "Toplam Gelir"
    }
)
st.plotly_chart(fig)

# En çok kazandıran ürünler
top_products = df.groupby("product_id")["total_price"].sum().sort_values(ascending=False).head(10)

top_products_df = top_products.reset_index()
top_products_df["product_name"] = [
    f"Ürün {i+1}" for i in range(len(top_products_df))
]

fig2 = px.bar(
    top_products_df,
    x="product_name",
    y="total_price",
    title="🏆 En Çok Kazandıran Ürünler",
    labels={
        "product_name": "Ürünler",
        "total_price": "Toplam Gelir"
    }
)



# 📦 Kategori analizi
st.markdown("## 📦 Ürün & Kategori Analizi")
category_sales = df.groupby("product_category_name")["total_price"].sum().sort_values(ascending=False).head(10)

category_df = category_sales.reset_index()

fig3 = px.bar(
    category_df,
    x="product_category_name",
    y="total_price",
    title="📦 En Karlı Kategoriler",
    labels={
        "product_category_name": "Kategori",
        "total_price": "Toplam Gelir"
    }
)


col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.plotly_chart(fig3, use_container_width=True)

# 👤 Müşteri analizi
st.markdown("## 👥 Müşteri ve Şehir Analizi")
customer_analysis = df.groupby("customer_id").agg({
    "total_price": "sum",
    "order_id": "nunique"
}).reset_index()

customer_analysis.columns = [
    "customer_id",
    "total_spent",
    "total_orders"
]





# En iyi müşteriler
top_customers = customer_analysis.sort_values(
    by="total_spent",
    ascending=False
).head(10)
top_customers["customer_name"] = [
    f"Müşteri {i+1}" for i in range(len(top_customers))
]

# Grafik
fig4 = px.bar(
    top_customers,
    x="customer_name",
    y="total_spent",
    title="👑 En Değerli Müşteriler",
    labels={
        "customer_name": "Müşteriler",
        "total_spent": "Toplam Harcama"
    }
)



# 🌍 Şehir Analizi Başlığı


# Şehir satışları hesapla
city_sales = (
    df.groupby("customer_city")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

city_map = (
    geolocation.groupby("geolocation_city")
    .agg({
        "geolocation_lat": "mean",
        "geolocation_lng": "mean"
    })
    .reset_index()
)

# DataFrame'e çevir
city_sales_df = city_sales.reset_index()

# Harita için şehir koordinatları

city_map = (
    geolocation.groupby("geolocation_city")
    .agg({
        "geolocation_lat": "mean",
        "geolocation_lng": "mean"
    })
    .reset_index()
)

city_sales_map = city_sales_df.merge(
    city_map,
    left_on="customer_city",
    right_on="geolocation_city",
    how="inner"
)

# Grafik oluştur
fig_city = px.bar(
    city_sales_df,
    x="customer_city",
    y="total_price",
    title="En Çok Satış Yapılan Şehirler",
    labels={
        "customer_city": "Şehir",
        "total_price": "Toplam Gelir"
    }
)

# Grafiği göster
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.plotly_chart(fig4, use_container_width=True)

with col_right2:
    st.plotly_chart(fig_city, use_container_width=True)

#Harita Başlığı
st.markdown("## 🗺️ Şehir Bazlı Satış Haritası")   
#Harita
fig_map = px.scatter_mapbox(
    city_sales_map,
    lat="geolocation_lat",
    lon="geolocation_lng",
    size="total_price",
    hover_name="customer_city",
    color="total_price",
    zoom=4,
    height=700,
    title="Brezilya Şehir Satış Yoğunluğu"
)
fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="Toplam Gelir (₺)"
    )
)

fig_map.update_layout(
    mapbox_style="carto-darkmatter",
    mapbox_center={
        "lat": -14.2350,
        "lon": -51.9253
    }
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# 🔮 Gelecek Satış Tahmini

st.markdown("## 🔮 Gelecek 6 Ay Satış Tahmini")

forecast_df = monthly_sales.copy()

forecast_df["month_num"] = range(len(forecast_df))

X = forecast_df[["month_num"]]
y = forecast_df["total_price"]

model = LinearRegression()
model.fit(X, y)

future_months = 6

future_x = np.arange(
    len(forecast_df),
    len(forecast_df) + future_months
).reshape(-1, 1)

future_predictions = model.predict(future_x)

future_df = pd.DataFrame({
    "month_num": future_x.flatten(),
    "forecast_sales": future_predictions
})

fig_forecast = px.line(
    forecast_df,
    x="month_num",
    y="total_price",
    title="Satış Trendi ve Gelecek Tahmini"
)

fig_forecast.add_scatter(
    x=future_df["month_num"],
    y=future_df["forecast_sales"],
    mode="lines+markers",
    name="Tahmin"
)

st.plotly_chart(
    fig_forecast,
    use_container_width=True
)


st.markdown("---")

st.markdown("## 📄 Proje Özeti")

st.success(f"""
Bu dashboard Olist E-Commerce veri seti kullanılarak geliştirilmiştir.

📦 Toplam Sipariş Sayısı: {total_orders}

💰 Toplam Gelir: {total_revenue:,.0f} ₺

🏆 En Karlı Kategori: {top_category}

🌍 En Güçlü Şehir: {top_city}

🚚 Ortalama Teslimat Süresi: {avg_delivery:.1f} Gün
""")

















