Site de Ofertas Automatizado

Site de ofertas de afiliados do Mercado Livre, publicado na Vercel e atualizado automaticamente a cada novo produto adicionado. Foi criado para eu não precisar editar o HTML na mão e para manter o catálogo sempre indexado no Google.

Site no ar: https://sitedivuga-o.vercel.app

O que o projeto faz
Gera a página index.html com os produtos do catálogo (nome, foto, preço e link de afiliado).
Gera e atualiza o sitemap.xml, para o Google encontrar e indexar as páginas.
Publica as mudanças automaticamente: cada atualização no repositório gera um novo deploy na Vercel.
Faz parte de um conjunto de automações: o catálogo vem do mesmo produtos.csv usado pelo bot de ofertas do Telegram.
Tecnologias
Python (geração do site e do sitemap)
HTML e CSS
SEO básico (sitemap, meta tags e verificação no Google Search Console)
Git, GitHub e Vercel (deploy contínuo)
Estrutura do repositório
Arquivo	Função
geradorsite.py	Script que gera o index.html e o sitemap.xml
index.html	Página principal do site
sitemap.xml	Mapa do site para os buscadores
Como rodar localmente
Tenha o Python 3 instalado.
Deixe o produtos.csv na mesma pasta do script.
Execute:
bash
py geradorsite.py
Abra o index.html no navegador para conferir o resultado.
Fluxo de atualização
Adiciono o link de afiliado do produto.
O script atualiza o index.html e o sitemap.xml.
O commit vai para o GitHub.
A Vercel publica a nova versão automaticamente.
Aprendizados
Automatizar um processo repetitivo de publicação.
Boas práticas de SEO para sites estáticos.
Deploy contínuo com GitHub e Vercel.
Autor

Ygor Oliveira Borges GitHub · LinkedIn
