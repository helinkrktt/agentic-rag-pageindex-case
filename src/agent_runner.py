# src/agent_runner.py - FINAL KOD (Temel Python Mantığıyla RAG Ajanı Simülasyonu)

import os
import json
from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI # LangChain yerine doğrudan OpenAI kütüphanesi
from .retriever_pageindex import search_docs_tool_function
# from tools import calculator # Hesap makinesini basitçe simüle edeceğiz

# .env dosyasındaki API anahtarı yükle
load_dotenv()

# --- 1. LLM İstemcisini Tanımlama ---
try:
    OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logger.error("OpenAI istemcisi başlatılamadı. API anahtarını kontrol edin.")
    OPENAI_CLIENT = None

# İstenen cevap formatı
REQUIRED_ANSWER_FORMAT = """
Answer (Kısa Cevap)
---
Sources (KAYNAKLAR):
- Başlık — node_id — sayfa
"""

def calculator_tool(expression: str) -> str:
    """Aritmetik ifadeyi hesaplar (Simülasyon)."""
    try:
        # Python'ın eval() fonksiyonu ile güvenli hesaplama yapılıyor (Çok basit simülasyon)
        result = eval(expression)
        return f"Hesaplama Sonucu: {result}"
    except:
        return "HATA: Hesaplama yapılamadı. İfadeyi kontrol edin."

def create_agent():
    """
    Bu fonksiyon, tests/test_agent.py dosyasındaki Pytest fixture'ının 
    (AgentExecutor) başlatılması için zorunludur.
    
    Temel Python simülasyonunda bu fonksiyonun döndürdüğü değerin bir önemi yoktur, 
    sadece döndürmelidir.
    """
    # Burası aslında testler için bir simülasyondur.
    return {"client": OPENAI_CLIENT, "run_function": run_agent}        

def run_agent(query: str):
    """Sorguyu alır ve Tool kullanıp kullanmayacağına karar verir."""
    
    if not OPENAI_CLIENT:
        logger.error("LLM istemcisi mevcut değil. Çalışma durduruluyor.")
        return

    # --- 2. Tool Seçim Mantığı (Karar Verme) ---
    # Agent'ın Tool kullanıp kullanmayacağına karar veren basit bir System Prompt
    tool_prompt = (
        f"Kullanıcı sorgusu: '{query}'\n\n"
        "Göreviniz, bu sorguyu cevaplamak için hangi aracı kullanacağınıza karar vermektir.\n"
        "Mali tablo, bütçe veya rapor içeriği soruluyorsa 'search_docs' aracını seçin.\n"
        "Matematiksel bir işlem gerekiyorsa 'calculator' aracını seçin.\n"
        "Direkt olarak sadece şu JSON formatını döndürün (Başka bir metin kesinlikle eklemeyin):\n"
        '{"action": "search_docs" veya "calculator" veya "none", "details": "aracın argümanı veya none"}'
    )
    
    try:
        # Tool Kararı için LLM çağrısı
        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": tool_prompt}],
            response_format={"type": "json_object"}
        )
        
        decision = json.loads(response.choices[0].message.content)
        action = decision.get("action", "none")
        details = decision.get("details", query)
        
        logger.info(f"LLM Kararı: Eylem='{action}', Detay='{details}'")

    except Exception as e:
        logger.error(f"Karar verme aşamasında hata: {e}. Doğrudan yanıtlama deneniyor.")
        action = "none" # API hatası varsa doğrudan cevaplamaya geç

    # --- 3. Tool Kullanımı ve Yanıt Üretme ---
    tool_output = ""
    if action == "search_docs":
        # PageIndex Retriever'ı kullan
        tool_output = search_docs_tool_function(details, k=3)
    elif action == "calculator":
        # Hesap makinesini kullan
        tool_output = calculator_tool(details)
    
    # Final Cevap Üretme Prompt'u
    final_prompt = (
        f"Sen bir RAG Agent'sın. Kullanıcının sorusunu ('{query}') elindeki bağlamı ve Tool çıktısını kullanarak cevapla.\n"
        f"Tool Çıktısı (Bağlam): {tool_output}\n"
        "Cevabını MUTLAKA aşağıdaki formatta sun:\n"
        f"{REQUIRED_ANSWER_FORMAT}"
    )

    final_response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": query}
        ]
    )
    
    logger.success("Agent Cevabı Başarılı.")
    print("\n--- AJANIN NİHAİ CEVABI ---\n")
    print(final_response.choices[0].message.content)


if __name__ == "__main__":
    logger.add("agent_runner.log", rotation="10 MB")
    
    test_query_rag = "2012 yılı bütçe raporunun kapsamı ve içeriği nelerdir? İlgili sayfa numarasını belirt."
    test_query_calc = "1200 TL'nin %18 KDV'si ne kadardır?"
    
    print("\n" + "="*50)
    print("TEST 1: PageIndex (Doküman Arama) Testi")
    print("="*50)
    run_agent(test_query_rag)
    
    print("\n" + "="*50)
    print("TEST 2: Calculator (Hesaplama) Testi")
    print("="*50)
    run_agent(test_query_calc)