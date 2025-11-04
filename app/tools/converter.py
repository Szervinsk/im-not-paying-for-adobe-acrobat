from pdf2docx import Converter
import time
import os

# A função agora recebe os caminhos de entrada e saída
def run(pdf_de_entrada, word_de_saida):
    """
    Função principal para converter PDF para DOCX.
    Recebe os caminhos como parâmetros.
    """
    print(f"Iniciando a conversão de {pdf_de_entrada}...")
    start_time = time.time()

    try: 
        cv = Converter(pdf_de_entrada)
        cv.convert(docx_filename=word_de_saida, start=0, end=None)
        cv.close()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\nArquivo convertido com sucesso como: '{word_de_saida}'")
        print(f"Conversão concluída em {total_time:.2f} segundos")
        return True, f"Conversão concluída em {total_time:.2f} segundos"
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a conversão: {e}")
        return False, f"Ocorreu um erro: {e}"