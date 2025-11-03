from pdf2docx import Converter
import time
import os

def run():
    """
    Função principal para converter PDF para DOCX.
    """
    print("\n--- 1. Conversor de PDF para Word ---")
    
    # Pergunta o nome do arquivo ao usuário
    pdf_name = input("Digite o nome do arquivo PDF (ex: meu_arquivo.pdf): ")
    
    # Os caminhos agora são relativos ao 'main.py', não ao 'converter.py'
    # app/upload/arquivo.pdf
    pdf_de_entrada = os.path.join('upload', pdf_name)
    
    # Cria um nome de saída
    output_name = pdf_name.lower().replace('.pdf', '_convertido.docx')
    word_de_saida = os.path.join('upload', output_name)

    # --- Verificação ---
    if not os.path.exists(pdf_de_entrada):
        print(f"Erro: Arquivo não encontrado em '{pdf_de_entrada}'")
        print("Verifique se o arquivo está na pasta 'upload'.")
        return # Para a função se o arquivo não existir

    # --- Início da Conversão ---
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
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a conversão: {e}")