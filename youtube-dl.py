#!/usr/bin/env python

from urllib.request import Request, urlretrieve, urlopen
from sys import argv, exit
from json import loads

def download():
    print('Obtendo informações...')
    try:
        session = Request('https://boxshared.herokuapp.com/boxfile', headers={'server':'youtube', 'url':argv[1]})
        r = loads(urlopen(session).read())
        if r[len(r)-1]['message'] == 'success':
            print('Informações obtidas')
        else:
            print('Video não encontrado!')
            exit(2)
    except Exception as a:
        print(f'Erro: {a}')
        exit(3)
    print('Listando formatos/videos...')
    num = 0
    for a in range(0, len(r)-1):
        if 'name' in r[a]:
            print(f'{a}:------------------------------------------------------\n   Nome: {r[a]["name"]}\n   Tamanho: {r[a]["size"]}\n   Qualidade: {r[a]["quality"]}\n')
            num += 1
    try:
        option = int(input('Digite o numero da opção: '))
    except Exception as a:
        print(f'Erro: {a}')
        exit(5)
    if option > num-1:
        print('Não tenho essa quantidade de opções!')
        exit(1)
    print('Baixando...')
    try:
        urlretrieve(r[option]['url'], r[option]['name'], reporthook=downloading)
        print('\033[2KVideo baixado')
        exit(0)
    except Exception as a:
        print(f'\033[2K\rErro: {a}')
        exit(4)

def downloading(bs, bn, tt):
    total = tt/1024
    downloaded = (bn*bs)/1024
    percent = (downloaded/total)*100
    if total <= 0:
        total, percent = 0, 0
    print(f'\033[2KTotal: {total:.0f}KB Baixado: {downloaded:.0f}KB {percent:.2f}%\r\033[1A')

if len(argv) < 2:
    exit(0)
elif 'youtu' in argv[1] and not 'list=' in argv[1]:
    download()
elif argv[1] in ('-h', '--help', 'help'):
    print(f'{argv[0]} [link|--help]\n --help Exibe esta ajuda\n Não tenho suporte a lista de reprodução!')
    exit(0)
else:
    print('Parametro ou link invalido!')
    exit(2)
