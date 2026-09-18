# Olist E-Commerce Business Intelligence Dashboard

İnteraktif bir e-ticaret iş zekâsı (Business Intelligence) dashboard'u. Proje, Olist e-ticaret veri seti kullanılarak satış performansı, müşteri davranışı ve lojistik süreçlerini analiz etmek amacıyla geliştirilmiştir.

## Proje Hakkında

Dashboard, e-ticaret verilerini tek bir arayüzde incelemeyi ve iş kararlarını destekleyebilecek temel metrikleri görselleştirmeyi amaçlar.

Uygulamada:
- Toplam gelir ve toplam sipariş sayısı
- Ortalama sipariş değeri
- Ortalama teslimat süresi
- Geciken sipariş sayısı ve gecikme oranı
- En yüksek gelir üreten ürün ve kategoriler
- Müşteri bazlı harcama analizi
- Şehir bazlı satış performansı
- Aylık satış trendleri
- Kategori ve tarih filtreleri
- Şehir bazlı satış haritası
- Gelecek 6 aya yönelik basit satış tahmini
- Analiz sonuçlarına dayalı yönetici özeti ve iş önerileri

sunulmaktadır.

## Dashboard

Uygulama Streamlit ile geliştirilmiştir ve Plotly kullanılarak interaktif grafikler oluşturulmuştur.

## Kullanılan Teknolojiler

- **Python**
- **Pandas** – veri temizleme, birleştirme ve analiz
- **NumPy** – sayısal işlemler
- **Plotly** – interaktif grafikler ve harita görselleştirmeleri
- **Streamlit** – interaktif dashboard
- **Scikit-learn** – Linear Regression ile satış tahmini
- **Jupyter Notebook** – keşifsel veri analizi

## Veri

Projede Olist e-ticaret veri setinin sipariş, ürün, müşteri, sipariş kalemi ve konum verileri kullanılmaktadır.

Veri işleme sürecinde farklı tablolar order_id, product_id ve customer_id üzerinden birleştirilerek analiz için tek bir veri yapısı oluşturulmuştur.

Ayrıca ürün kategorileri dashboard içerisinde daha anlaşılır olması amacıyla Türkçeleştirilmiştir.

## Proje Yapısı

```
olist-ecommerce-business-intelligence-dashboard/
│
├── app/
│   └── app.py
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_orders_dataset.csv
│   └── olist_products_dataset.csv
│
├── notebook/
│   └── analysis.ipynb
│
├── requirements.txt
└── README.md
```

## Çalıştırma

Projeyi yerel ortamda çalıştırmak için:

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

Ardından Streamlit uygulaması tarayıcıda açılır.

## Analiz Akışı

1. Veri setleri yüklenir.
2. Sipariş, ürün, müşteri ve konum verileri birleştirilir.
3. Tarih alanları ve teslimat metrikleri analiz için hazırlanır.
4. Gelir, sipariş ve teslimat metrikleri hesaplanır.
5. Ürün, kategori, müşteri ve şehir bazlı analizler oluşturulur.
6. Sonuçlar interaktif grafiklerle dashboard üzerinde sunulur.
7. Linear Regression kullanılarak gelecek 6 ay için basit bir satış trend tahmini oluşturulur.

## Amaç

Bu proje; veri analizi, veri görselleştirme ve iş zekâsı yaklaşımını bir araya getirerek ham e-ticaret verilerinden anlamlı ve görsel içgörüler üretmeyi amaçlamaktadır.