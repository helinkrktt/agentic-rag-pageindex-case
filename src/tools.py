from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool 
from simpleeval import simple_eval # Hesaplama için güvenli kütüphane
from loguru import logger
from typing import List

# PageIndex sorgulamasını yapan fonksiyonu içe aktar
from .retriever_pageindex import search_docs_tool_function 

# --- GEREKSİNİM: Input Şemasını Tanımlama (LangChain'in güncel Tool API'si için opsiyonel ama önerilir) ---
class SearchDocsInput(BaseModel):
    """search_docs aracı için girdi şeması."""
    query: str = Field(description="Dokümanda aranacak anahtar sorgu.")

class CalculatorInput(BaseModel):
    """calculator aracı için girdi şeması."""
    expression: str = Field(description="Hesaplama yapılacak matematiksel ifade (örn: '5 + 3 * (10 / 2)').")


# 1. TOOL: search_docs (PageIndex retriever'ı çağırır)
@tool(args_schema=SearchDocsInput)
def search_docs(query: str) -> str:
    """
    Bu araç, PageIndex sisteminde dokümanlardaki özel, dahili bilgileri arar ve çeker. 
    Genel bilgi, politika detayları, kurulum adımları veya finansal veriler gibi 
    belirli bir dokümanda yer alan konular hakkında bilgi edinmek için kullanılmalıdır.
    """
    logger.info(f"Agent, search_docs aracını çağırıyor...")
    
    # retriever_pageindex.py dosyasındaki fonksiyonu çağırıyoruz
    context = search_docs_tool_function(query)
    
    # Agent'a döndürülecek metin
    return context

# 2. TOOL: calculator (Matematik Hesaplama)
@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """
    Bu araç, bir matematiksel ifadeyi (örneğin: '5 + 3 * (10 / 2)') güvenli bir şekilde değerlendirir. 
    Dokümandan çekilen değerler üzerinde toplama, çıkarma, çarpma veya bölme gibi 
    aritmetik işlemler gerektiğinde KESİNLİKLE bu aracı kullanın.
    """
    logger.info(f"Agent, calculator aracını çağırıyor: {expression}")
    try:
        # simple_eval, Python'ın tehlikeli eval() fonksiyonuna göre daha güvenlidir.
        result = simple_eval(expression)
        return str(result)
    except Exception as e:
        logger.error(f"Hesaplama hatası: {e}")
        return f"Hesaplama yapılırken bir hata oluştu: {e}"

# 3. TÜM ARAÇLARIN LİSTESİ

# Agent'a sunulacak tüm araçların listesi
ALL_TOOLS: List = [search_docs, calculator]