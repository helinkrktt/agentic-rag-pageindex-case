# src/retriever_pageindex.py - DÜZELTİLMİŞ VE AGENT TOOL'A HAZIR VERSİYON

import json
from typing import List, Dict, Any
from loguru import logger
import os

# --- KONFİGÜRASYON ---
# İndeks dosyasının adı ve konumu (index_builder.py'de kullanılan ile uyumlu olmalı)
INDEX_FILE = "indexes/butce_rapor.json" # Önceki butce_rapor.json dosya adını kullanıyoruz.

class PageIndexRetriever:
    """PageIndex JSON çıktısını yükleyen ve Agent tarafından sorgulanan sınıf."""

    def __init__(self):
        # 1. Hata: Global değişken tutarsızlığı giderildi.
        if not os.path.exists(INDEX_FILE):
            logger.warning(f"PageIndex indeksi bulunamadı: {INDEX_FILE}. Boş indeks ile başlatılıyor.")
            self.index_data = {"nodes": []}
        else:
            self.index_data = self._load_index()
            # Yüklenen indeksin içinde 'nodes' anahtarı olmalı. Yoksa boş listeyle başlat.
            if 'nodes' not in self.index_data or not isinstance(self.index_data['nodes'], list):
                 logger.warning(f"İndeks içeriği hatalı/boş. Boş indeks ile başlatılıyor.")
                 self.index_data = {"nodes": []}
            else:
                 logger.info(f"PageIndex indeksi başarıyla yüklendi. {len(self.index_data['nodes'])} düğüm bulundu.")

    def _load_index(self) -> Dict:
        """Kayıtlı JSON ağaç indeksini yükler."""
        try:
            # 1. Hata: INDEX_FILE değişkeni kullanıldı.
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"İndeks yüklenirken bir hata oluştu: {e}")
            return {"nodes": []}

    # 2. Hata: Girinti düzeltildi.
    def search_docs(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Agent tarafından Tool olarak kullanılacak olan ana arama fonksiyonu.
        Basit keyword eşleştirme simülasyonu yapar.
        """
        if not self.index_data.get('nodes'):
            return [{"error": "PageIndex indeksi boş. Lütfen indeks oluşturmayı kontrol edin."}]

        logger.info(f"PageIndex Retriever, dokümanlarda arama yapıyor: '{query}'")
        query_lower = query.lower()
        results = []
        
        # 3. Hata: Mock data yerine basit simülasyon mantığı eklendi.
        for node in self.index_data.get('nodes', []):
             node_content = (node.get('content', '') or node.get('node_text', '')).lower()
             node_summary = node.get('summary', '') or node.get('node_summary', '')
             
             # Sorgu eşleşmesi varsa (gerçek PageIndex'i simüle ediyoruz)
             if query_lower in node_content:
                 results.append({
                     "title": node.get('title', 'Başlık Yok'),
                     "node_id": node.get('node_id', 'ND-000'),
                     "summary": node_summary,
                     "page": node.get('page', 'N/A'),
                     "score": 1.0, # Simülasyon skoru
                     "content": node_content[:500] + "..." # İçeriği 500 karakterle kısaltalım
                 })

        return results[:k]

# Sınıfı bir örnek (instance) olarak başlatalım
PAGE_INDEX_RETRIEVER = PageIndexRetriever()

# search_docs fonksiyonunu Agent'ın kullanması için dışarıya açıyoruz
def search_docs_tool_function(query: str, k: int = 5) -> str:
    """search_docs metodunu çağırır ve çıktıyı LLM'in okuyacağı string'e dönüştürür."""
    results = PAGE_INDEX_RETRIEVER.search_docs(query, k)
    
    if 'error' in results[0] if results else False:
         return results[0]['error']

    # LLM'in cevabı formatlamak için ihtiyacı olan veriyi hazırlıyoruz
    context_list = []
    for hit in results:
        # Agent'ın hem içeriği hem de kaynağı görmesi gerekiyor
        context_list.append(
            f"KAYNAK DÜĞÜM (NODE_ID: {hit.get('node_id')}, SAYFA: {hit.get('page')}):\n"
            f"BAŞLIK: {hit.get('title')}\n"
            f"ÖZET/İÇERİK: {hit.get('summary')}\n"
            f"SKOR: {hit.get('score')}\n"
            f"İÇERİK: {hit.get('content')}\n"
            f"---"
        )
    return "\n".join(context_list)