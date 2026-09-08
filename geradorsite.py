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

    print("🔍 Puxando informações e foto da página...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    nome = "Achado Imperdível"
    preco = "Confira no site"
    imagem = "https://via.placeholder.com/150"

    try:
        resposta = requests.get(link, headers=headers, timeout=10)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # Puxa o título da página como nome do produto (se houver)
            if soup.title and soup.title.string:
                nome_limpo = soup.title.string.strip()
                if len(nome_limpo) > 3:
                    nome = nome_limpo[:70] # Limita o tamanho para não quebrar o layout

            # Puxa a foto oficial do produto (OpenGraph)
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                imagem = og_image["content"]
    except Exception as e:
        print(f"⚠️ Aviso na busca automática (usando valores padrão): {e}")

    # Monta o card HTML bonitinho
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

    # Injeta no index.html logo abaixo do marcador
    if os.path.exists(ARQUIVO_HTML):
        with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
            conteudo_html = f.read()

        marcador = "<!-- INJECAO_AUTOMATICA -->"
        if marcador in conteudo_html:
            # Coloca o novo produto logo acima do marcador para ir empilhando os novos
            novo_html = conteudo_html.replace(marcador, novo_card + "\n            " + marcador)
            
            with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
                f.write(novo_html)
            
            print("\n🚀 Sucesso! Produto adicionado no HTML local.")
            
            # Automação do Git: Salva, Commita e Envia para o GitHub Pages sozinho!
            try:
                print("☁️ Subindo alterações para o GitHub Pages...")
                subprocess.run(["git", "add", "index.html"], check=True)
                subprocess.run(["git", "commit", "-m", "Adiciona novo produto via script"], check=True)
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