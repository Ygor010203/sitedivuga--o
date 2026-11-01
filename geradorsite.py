import os
import subprocess
import requests
from bs4 import BeautifulSoup

ARQUIVO_HTML = "index.html"

def adicionar_por_link():
    print("--- ADICIONAR ACHADO POR LINK ---")
    link = input("Cole o link de afiliado aqui: ").strip()
    
    if not link:
        print("❌ Link vazio. Tente novamente.")
        return

    print("🔍 Puxando informações e foto da página (seguindo redirecionamento)...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    nome = "Achado Imperdível"
    preco = "Confira no site"
    imagem = "https://via.placeholder.com/150"

    try:
        # allow_redirects=True faz o Python seguir o link meli.la até a página final do produto
        resposta = requests.get(link, headers=headers, timeout=15, allow_redirects=True)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # 1. Tenta pegar pelo meta tag 'og:title' (geralmente é o nome limpo do produto)
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                nome = og_title["content"].strip()
            
            # Se não achar no og:title, tenta pegar do título da página (<title>)
            elif soup.title and soup.title.string:
                nome_limpo = soup.title.string.strip()
                if len(nome_limpo) > 3:
                    # Remove sujeiras comuns do Mercado Livre no título
                    nome = nome_limpo.split('|')[0].split('-')[0].strip()

            # Limita o tamanho para não quebrar o layout do card
            if len(nome) > 70:
                nome = nome[:70] + "..."

            # 2. Puxa a foto oficial do produto (OpenGraph)
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                imagem = og_image["content"]

    except Exception as e:
        print(f"⚠️ Aviso na busca automática (usando valores padrão): {e}")

    # Monta o card HTML bonitinho com o nome real do produto injetado
    novo_card = f"""
            <div class="product-card">
                <img src="{imagem}" alt="{nome}" class="product-img">
                <div class="product-info">
                    <div class="product-name">{nome}</div>
                    <div class="product-price">{preco}</div>
                    <a href="{link}" class="btn-product" target="_blank">Ver Oferta</a>
                </div>
            </div>
    """

    # Injeta no index.html logo acima do marcador
    if os.path.exists(ARQUIVO_HTML):
        with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
            conteudo_html = f.read()

        marcador = "<!-- INJECAO_AUTOMATICA -->"
        if marcador in conteudo_html:
            # Coloca o novo produto logo acima do marcador para ir empilhando os novos
            novo_html = conteudo_html.replace(marcador, novo_card + "\n            " + marcador)
            
            with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
                f.write(novo_html)
            
            print(f"\n🚀 Sucesso! Produto adicionado: '{nome}'")
            
            # Automação do Git: Salva, Commita e Envia para o GitHub Pages sozinho!
            try:
                print("☁️ Subindo alterações para o GitHub Pages...")
                subprocess.run(["git", "add", "index.html"], check=True)
                subprocess.run(["git", "commit", "-m", f"Adiciona produto: {nome}"], check=True)
                subprocess.run(["git", "push", "origin", "main"], check=True)
                print("✅ Site atualizado e publicado no ar com sucesso!")
            except Exception as git_erro:
                print(f"⚠️ Produto salvo no PC, mas houve um erro ao enviar pro Git: {git_erro}")

        else:
            print(f"\n❌ Erro: Tag {marcador} não foi encontrada no index.html.")
    else:
        print(f"\n❌ Erro: Arquivo index.html não encontrado na pasta.")

if __name__ == "__main__":
    adicionar_por_link()