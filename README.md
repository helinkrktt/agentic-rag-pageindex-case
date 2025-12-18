## CASE 2: Agentic RAG System (PageIndex & LangChain Integration)
Bu proje, VectifyAI/PageIndex'in hiyerarşik ve akıl yürütme tabanlı indeksleme yapısını LangChain kütüphanesi ile birleştirerek; kaynak atıflı, otonom araç kullanım yeteneğine sahip bir Agentic RAG sistemi sunar.

## OBJECTIVE (Amaç)
Bu vakanın temel amacı, PageIndex'in hiyerarşik indeks yapısını kullanarak ilgili doküman parçalarını bulmak ve bir LangChain Ajanı aracılığıyla kullanıcı sorularını kaynak göstererek cevaplamaktır. Sistem, sadece metin okumakla kalmaz, karmaşık sorgularda araçları (tools) otonom olarak seçer.

## PROJECT STRUCTURE (Dosya Yapısı)
Proje, modüler bir yapıda ve genişletilebilir şekilde tasarlanmıştır:

data/: İşlenecek ham dökümanları (PDF/TXT) içerir.

indexes/: PageIndex tarafından üretilen JSON hiyerarşik ağaç yapılarını saklar.

src/: Uygulamanın çekirdek kodlarını barındırır.

agent_runner.py: Ajanın karar mekanizmasını ve ana döngüsünü yönetir.

tools.py: Ajanın yeteneklerini (Arama ve Hesaplama) tanımlar.

retriever_pageindex.py: PageIndex JSON çıktısını sorgulayan wrapper modülüdür.

index_builder.py: Belgeleri PageIndex kullanarak işler ve indeksler.

tests/: Sistemin doğruluğunu teyit eden minimum 3 adet birim testi içerir.

demo_steps.md: Kurulum ve çalıştırma için hızlı kullanım rehberidir.

## AGENT CAPABILITIES (Ajan Yetenekleri)
Ajan, karmaşık sorguları yanıtlamak için şu araçları (tools) kullanır:

PageIndex_Search: Doküman içeriğiyle ilgili bilgi toplamak için hiyerarşik indeksi tarar.

Calculator: Sayısal veriler üzerinde güvenli aritmetik işlemler yapar.

Source Attribution: Her cevabı mutlaka node_id ve sayfa numarası gibi kanıtlarla destekler.

## REQUIRED ANSWER FORMAT (Zorunlu Cevap Formatı)
Ajan, çıktılarını her zaman aşağıdaki standart yapıda sunar:

Answer (short) --- Detailed Explanation (optional)

Sources:

Title — node_id — page — similarity_score

## SETUP & RUN (Kurulum ve Çalıştırma)
Sistemi ayağa kaldırmak için şu adımları izleyin:

Bağımlılıkları kurun: pip install -r requirements.txt.

.env dosyasını oluşturup OPENAI_API_KEY bilginizi girin.

İndeks oluşturun: python src/index_builder.py.

Ajanı başlatın: python src/agent_runner.py.

Testleri çalıştırın: python -m pytest tests/test_agent.py.

## NOTES (Önemli Notlar)
PageIndex, dökümanı hiyerarşik bir ağaç yapısında sunduğu için ajan daha isabetli aramalar yapar.

Halüsinasyonları önlemek için cevaplar tamamen PageIndex düğümlerindeki verilere dayandırılmıştır.

API kota sınırlamaları durumunda, sistemin test edilebilirliği için simüle edilmiş indeks dosyaları kullanılabilir.