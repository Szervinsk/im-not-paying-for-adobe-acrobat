from pypdf import PdfWriter
import os

def run():
    """
    Função principal para juntar (merge) vários PDFs.
    """
    print("\n--- 2. Mesclar arquivos PDF ---")
    
    pdfs_para_juntar = []
    
    # Loop para adicionar arquivos
    while True:
        pdf_name = input("Digite o nome de um PDF (ou 'fim' para parar): ")
        
        if pdf_name.lower() == 'fim':
            break
            
        pdf_path = os.path.join('upload', pdf_name)
        
        if os.path.exists(pdf_path):
            pdfs_para_juntar.append(pdf_path)
            print(f"'{pdf_name}' adicionado à lista.")
        else:
            print(f"Aviso: Arquivo '{pdf_path}' não encontrado. Pulando.")

    if len(pdfs_para_juntar) < 2:
        print("Você precisa de pelo menos 2 arquivos para mesclar.")
        return

    # Pergunta o nome do arquivo de saída
    saida_name = input("Digite o nome do arquivo final (ex: documento_juntado.pdf): ")
    saida_path = os.path.join('upload', saida_name)
    
    # --- Início do Merge ---
    try:
        merger = PdfWriter()
        print("Iniciando 'merge'...")
        
        for pdf in pdfs_para_juntar:
            merger.append(pdf)
        
        merger.write(saida_path)
        merger.close()
        
        print(f"\n--- SUCESSO! ---")
        print(f"PDFs juntados e salvos como: '{saida_path}'")
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a mesclagem: {e}")