import streamlit as st
import os
from tools.converter import run as converter_run
from tools.merge import run as merge_run
# Não precisamos mais do defaultdict
# from collections import defaultdict 

# --- Configuração da Página ---
st.set_page_config(page_title="PDF Utils", layout="centered")
st.title("I'm Not Paying For Adobe! 💸")
st.caption("Um aplicativo simples para Converter e Juntar PDFs.")

# --- Define os caminhos ---
UPLOAD_DIR = "upload"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- BARRA LATERAL (Simplificada) ---
st.sidebar.title("Arquivos Finais")

try:
    # 1. Lista todos os arquivos no diretório
    files_in_upload = os.listdir(UPLOAD_DIR)
    
    # 2. Filtra para mostrar APENAS os arquivos finais (outputs)
    #    (Arquivos convertidos ou mesclados)
    final_files = [f for f in files_in_upload if 
                   f.endswith('_convertido.docx') or  # Arquivos da Aba 1
                   f.endswith('documento_juntado.pdf') or # Arquivos da Aba 2 (mude se o nome padrão mudar)
                   (f.endswith('.pdf') and 'juntado' in f) # Um filtro extra para mesclagem
                  ]
    
    # Remove duplicados (caso os filtros peguem o mesmo)
    final_files = sorted(list(set(final_files)))


    # 3. Mostra os arquivos finais na barra lateral
    if not final_files:
        st.sidebar.info("Nenhum arquivo final foi gerado ainda.")
    else:
        st.sidebar.markdown("---")
        
        for file_name in final_files:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            
            st.sidebar.write(file_name) # Mostra o nome do arquivo
            
            # Colunas para os botões de Download e Deletar
            col1, col2 = st.sidebar.columns(2)
            
            # Botão de Download
            with open(file_path, "rb") as f:
                col1.download_button(
                    label="⬇️ Baixar",
                    data=f,
                    file_name=file_name,
                    key=f"download_{file_name}"
                )
            
            # Botão de Deletar
            if col2.button("🗑️ Deletar", key=f"delete_{file_name}"):
                try:
                    os.remove(file_path)
                    st.rerun() # Recarrega a página para atualizar a lista
                except Exception as e:
                    st.sidebar.error(f"Erro ao deletar {file_name}")

        st.sidebar.markdown("---")

    # Botão para limpar a pasta 'upload' (continua útil)
    if st.sidebar.button("⚠️ Limpar TODOS os arquivos"):
        # Pega a lista COMPLETA de arquivos (incluindo os PDFs originais)
        all_files = [f for f in os.listdir(UPLOAD_DIR) if not f.startswith('.')]
        
        if not all_files:
            st.sidebar.info("A pasta já está vazia.")
        else:
            for file_to_delete in all_files:
                try:
                    os.remove(os.path.join(UPLOAD_DIR, file_to_delete))
                except Exception as e:
                    pass # Ignora erros
            
            st.sidebar.success("Pasta 'upload' limpa!")
            st.rerun()

except Exception as e:
    st.sidebar.error(f"Erro ao ler a pasta 'upload': {e}")
# --- FIM DA BARRA LATERAL ---


# --- Cria as Abas ---
# (Esta parte está IDÊNTICA à que você enviou)
tab1, tab2 = st.tabs(["1. Converter PDF para Word", "2. Mesclar arquivos PDF"])

# --- Aba 1: Conversor ---
with tab1:
    st.header("Conversor PDF -> Word")
    
    uploaded_file = st.file_uploader(
        "Selecione um arquivo PDF", 
        type="pdf",
        key="uploader_pdf_word"
    )
    
    if uploaded_file is not None:
        # SALVA o arquivo original na pasta upload
        pdf_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.info(f"Arquivo '{uploaded_file.name}' carregado.")

        if st.button("Converter para Word"):
            # Define o nome do arquivo convertido
            output_name = os.path.splitext(uploaded_file.name)[0].lower() + '_convertido.docx'
            docx_path = os.path.join(UPLOAD_DIR, output_name)
            
            with st.spinner("Convertendo... Isso pode demorar um pouco..."):
                sucesso, mensagem = converter_run(pdf_path, docx_path)
            
            if sucesso:
                st.success(f"Sucesso! {mensagem}")
                
                with open(docx_path, "rb") as f:
                    st.download_button(
                        label="Baixar arquivo .docx",
                        data=f,
                        file_name=output_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                if st.button("Converter outro arquivo"):
                    st.session_state.uploader_pdf_word = None
                    st.rerun()
            
            else:
                st.error(mensagem)
                if st.button("Tentar com outro arquivo"):
                    st.session_state.uploader_pdf_word = None
                    st.rerun()

# --- Aba 2: Mesclador ---
with tab2:
    st.header("Juntar (Merge) PDFs")
    
    uploaded_files = st.file_uploader(
        "Selecione dois ou mais arquivos PDF", 
        type="pdf", 
        accept_multiple_files=True,
        key="uploader_pdf_merge"
    )
    
    if uploaded_files and len(uploaded_files) >= 2:
        
        output_filename = st.text_input(
            "Nome do arquivo final:", 
            "documento_juntado.pdf"
        )

        if st.button("Juntar PDFs"):
            lista_de_caminhos = []
            
            # Salva todos os arquivos temporariamente
            for file in uploaded_files:
                temp_path = os.path.join(UPLOAD_DIR, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                lista_de_caminhos.append(temp_path)

            final_output_path = os.path.join(UPLOAD_DIR, output_filename)

            with st.spinner("Juntando arquivos..."):
                sucesso, mensagem = merge_run(lista_de_caminhos, final_output_path)
            
            if sucesso:
                st.success(f"Sucesso! {mensagem}")
                
                with open(final_output_path, "rb") as f:
                    st.download_button(
                        label="Baixar PDF juntado",
                        data=f,
                        file_name=output_filename,
                        mime="application/pdf"
                    )
                
                if st.button("Juntar outros arquivos"):
                    st.session_state.uploader_pdf_merge = None
                    st.rerun()
            else:
                st.error(mensagem)
                if st.button("Tentar novamente"):
                    st.session_state.uploader_pdf_merge = None
                    st.rerun()
    
    elif uploaded_files:
        st.warning("Você precisa selecionar pelo menos 2 arquivos para juntar.")