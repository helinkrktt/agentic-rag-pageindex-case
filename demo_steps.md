# CASE 2: Agentic RAG System (PageIndex + LangChain) — DEMO ADIMLARI

Bu doküman, Agentic RAG sisteminin kurulumunu, indeks oluşturma ve Agent'ı çalıştırma adımlarını özetler.

## 1. Kurulum (Setup)

1.  **Repository Klonlama:** Proje dosyasını yerel makineye indirin.
2.  **Sanal Ortam:** Sanal ortamı etkinleştirin.
    python -m venv venv
    source venv/bin/activate  # Linux/Mac için
    # veya
    venv\Scripts\activate     # Windows için

3.  **Gereksinimler:** Gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    pip install openai # (LangChain uyumsuzluğunu gidermek için)
    ```
4.  **.env Dosyası:** `.env` dosyasını oluşturun ve geçerli bir OpenAI API Anahtarı ekleyin (`OPENAI_API_KEY="sk-..."`).
5.  **Doküman:** `data/` klasörüne işlenecek PDF'i (örn. `butce_rapor.pdf`) ekleyin.

## 2. İndeks Oluşturma (Adım 2 Simülasyonu)

PageIndex'in LLM çağrıları nedeniyle kota sorunu yaşandığı için bu aşama manuel olarak simüle edilmiştir:

1.  **İndeksleme (Simülasyon):** Normalde `python src/index_builder.py` çalıştırılmalıdır.
2.  **Manuel İndeks:** `indexes/butce_rapor.json` dosyası, Retriever'ın okuyabileceği geçerli bir JSON formatında manuel olarak oluşturulmuştur.

## 3. Testlerin Çalıştırılması (Opsiyonel)

Retriever'ın indeksi doğru okuyup okumadığını kontrol etmek için testler çalıştırılabilir:

```bash
pip install pytest
python -m pytest -s -v tests/test_agent.py

## 4. Agent'ın Çalıştırılması ve Demo

Sistem, bir LangChain Ajanı (Agent) olarak çalışır. Ajan, sorunun türüne göre otonom olarak hangi aracı (Tool) kullanacağına karar verir.

Örnek Kullanıcı Sorguları ve Ajan Davranışı
RAG Sorgusu: "2012 yılı bütçe raporunun kapsamı ve içeriği nelerdir? İlgili sayfa numarasını belirt."

Ajan Davranışı: search_docs aracını tetikler, PageIndex düğümlerini tarar ve yanıtı kaynak göstererek döner.

Hesaplama Sorgusu: "1200 TL'nin %18 KDV'si ne kadardır?"

Ajan Davranışı: Matematiksel bir işlem olduğunu anlar, calculator aracını tetikler ve sonucu döner.

Beklenen Cevap Formatı
Ajanın tüm yanıtları aşağıdaki zorunlu formatta sunulur:

Answer (Kısa Cevap)
---
Detailed Explanation (Detaylı Açıklama - Opsiyonel)

Sources (KAYNAKLAR):
- Başlık — node_id — sayfa — similarity_score
