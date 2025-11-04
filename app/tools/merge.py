from pypdf import PdfWriter
import os

# A função agora recebe a LISTA de arquivos e o NOME da saída
def run(lista_de_pdfs, saida_path):
    """
    Função principal para juntar (merge) vários PDFs.
    Recebe os caminhos como parâmetros.
    """
    print("Iniciando 'merge'...")
    try:
        merger = PdfWriter()
        
        for pdf in lista_de_pdfs:
            print(f"Adicionando '{pdf}'...")
            merger.append(pdf)
        
        merger.write(saida_path)
        merger.close()
        
        print(f"\n--- SUCESSO! ---")
        print(f"PDFs juntados e salvos como: '{saida_path}'")
        return True, "Arquivos juntados com sucesso!"
        
    except Exception as e:
        print(f"\nOcorreu um erro durante a mesclagem: {e}")
        return False, f"Ocorreu um erro: {e}"