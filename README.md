# Teste de Visão Computacional da V-LAB!

Esse teste é uma breve análise e processamento de um vídeo público com o intuito de indentificar nome de pessoas e anônimaliza-los.

## Tecnologias utilizadas

É um pequeno script em python, não modularizado por conta do tempo.
Foi utilizada as seguintes biliotecas:
- Opencv : Para utilizar técnicas de leitura e manipulação de frames de vídeo, preprocessamento em imagens como  mudança do colorspace para tons de cinza, encontrar um limiar que mais ajude os próximos algoritmos e também para a criação de retangulos para anonimizar os nomes encontrados.
- Pytesseract : É uma ferramenta OCR para python que reconheci o texto e o classifica.
- difflib: Essa biblioteca tem um feauture muito interessante que da em porcentagem a semelhança de strings. Como a taxa de falso positivos encontrados no texto foi extramente grande da primeira vez e em alguns frames o texto reconhecido pelo pytesseract não é exato e muda alguns caracteres do normal, foi utilizado essa lib para caso encontre palavras semelhantes as considerassem. 

## Experimento
Foi utilizado o video que se encontra no link abaixo junto com o video de resultado. Não foi feita nenhum tipo de avaliação do método por questão de tempo, mas acredito que melhorando a questão de preprocessamento que foi bem simples, mudanças na ferramenta OCR como configuração e utilizando de regiões de interresse melhorariam em muito o tempo de processamento quanto a acurácia.

# Site das Bibliotecas utilizadas
- https://pypi.org/project/opencv-python/
- https://pypi.org/project/pytesseract/
- https://docs.python.org/3/library/difflib.html
