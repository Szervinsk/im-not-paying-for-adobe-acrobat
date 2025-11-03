# Importa as funções 'run' e as renomeia
from tools.converter import run as converter
from tools.merge import run as merge
import sys

def sair():
    """Função para sair do programa."""
    print("Saindo... Tchau!")
    sys.exit()

def start():
    # Dicionário de funções
    switch = {
        '1': converter,
        '2': merge,
        '3': sair  # Agora 'sair' é uma função
    }

    # Loop principal do menu
    while True:
        print("\n" + "="*30)
        print("     I'm Not Paying For Adobe")
        print("="*30)
        print("Opções disponíveis:")
        print("1. Converter PDF para Word")
        print("2. Mesclar arquivos PDF")
        print("3. Sair")
        
        escolha = input("Selecione uma opção (1-3): ")

        # Pega a função do dicionário
        # Se não encontrar, usa a lambda para mostrar "Opção inválida"
        func = switch.get(escolha, lambda: print("Opção inválida. Tente novamente."))
        
        # Executa a função
        func()
        
        # Pausa para o usuário ver o resultado antes de voltar ao menu
        if escolha in ('1', '2'):
            input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    # Nenhuma mudança aqui
    print("Iniciando o aplicativo...")
    start()