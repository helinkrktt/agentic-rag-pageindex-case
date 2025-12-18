# src/index_builder.py - FINAL VE MANTIKSAL OLARAK DOĞRU OPENAI VERSİYONU

import os
import subprocess
from dotenv import load_dotenv
from loguru import logger
import shlex

# .env dosyasındaki API anahtarlarını yükle
load_dotenv()

# Kendi dosya adlarınızı buraya yazın.
PDF_NAME = "butce_rapor.pdf" 
INDEX_NAME = "butce_rapor.json"

def build_page_index(doc_name: str, index_name: str):
    """
    PageIndex CLI'ı kullanarak PDF'i iki aşamada işler ve indeksi oluşturur.
    OpenAI gpt-3.5-turbo modelini kullanır.
    """
    
    # MD dosyasının adı ve konumu (PDF ile aynı yerde oluştuğunu varsayıyoruz)
    base_name = doc_name.replace('.pdf', '')
    md_file_path = os.path.join(os.getcwd(), 'data', f"{base_name}.md")
    
    pageindex_cli_path = os.path.join(os.getcwd(), 'PageIndex', 'run_pageindex.py')
    
    # Not: Ortam değişkeni kısıtlamaları ve model adı bu komutta düzeltilmiştir.
    
    # -------------------------------------------------------------
    # AŞAMA 1: PDF'ten Markdown (MD) Oluşturma
    # -------------------------------------------------------------
    logger.info("Aşama 1/2: PDF'ten Markdown dosyası oluşturuluyor (Model: gpt-3.5-turbo)...")
    
    command_str_step1 = (
        f"python {pageindex_cli_path} "
        f"--pdf_path data/{doc_name} "   # Girdi: PDF
        f"--model gpt-3.5-turbo"         # Kullanılacak model
    )
    
    try:
        # subprocess shell=True ile mutlak yol zorlaması yapılıyor
        subprocess.run(command_str_step1, check=True, shell=True, cwd=os.getcwd())
        logger.success(f"Aşama 1 başarılı: Markdown dosyası oluşturuldu: {base_name}.md")

    except subprocess.CalledProcessError as e:
        logger.error(f"Aşama 1 Hatası: PDF'ten MD oluşturulamadı. Hata Kodu: 429 Kota Aşımı olabilir.")
        return # Hata durumunda fonksiyonu durdur

    # -------------------------------------------------------------
    # AŞAMA 2: Markdown'dan PageIndex JSON İndeksini Oluşturma
    # -------------------------------------------------------------
    logger.info("Aşama 2/2: Markdown dosyasından JSON indeksi oluşturuluyor (Model: gpt-3.5-turbo)...")
    
    command_str_step2 = (
        f"python {pageindex_cli_path} "
        f"--md_path data/{base_name}.md "        # Girdi: MD (Aşama 1'den)
        f"--output-file indexes/{index_name} "   # Çıktı: JSON
        f"--model gpt-3.5-turbo"              
    )

    try:
        subprocess.run(command_str_step2, check=True, shell=True, cwd=os.getcwd())
        logger.success(f"PageIndex indeksi başarıyla oluşturuldu: {INDEX_NAME}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Aşama 2 Hatası: JSON indeksi oluşturulamadı.")
        logger.error("Lütfen OpenAI API anahtarınızın kotalı/geçerli olduğundan emin olun.")
    except Exception as e:
        logger.error(f"Beklenmedik bir hata oluştu: {e}")


if __name__ == "__main__":
    logger.add("index_builder.log", rotation="10 MB")
    build_page_index(PDF_NAME, INDEX_NAME)