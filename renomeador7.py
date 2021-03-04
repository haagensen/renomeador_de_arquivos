#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from obtemparametros import ObtemParametros

def PrefixaArquivo(path, prefixo, aplicarsobre='n', alterar=False):
    """
    Para cada arquivo em um determinado diretório, adiciona uma
    string em seu início.

    path Indica o diretório a ser examinado.
    prefixo É a string a ser adicionada no início.
    aplicarSobre Onde aplicar a alteração. Especifique:
        "n" para alterar somente o nome do arquivo (padrão),
        "e" para alterar somente na extensão do arquivo,
        "c" para alterar tanto no nome quanto na extensão do arquivo.
    alterar Indica se a operação deverá ser efetivamente realizada.
        O padrão é False. Útil para testes.
    """

    total = 0
    saida = tuple()

    for pathname, _, filenames in os.walk(path):
        for f in filenames:

            pos = f.rfind('.')
            if pos <= 0:
                ext = ''
                nome = f
            else:
                ext = f[pos+1:]
                nome = f[0:pos]

            if aplicarsobre.lower().startswith('c'):
                arq = prefixo + nome + '.' + prefixo + ext
            else:
                if aplicarsobre.lower().startswith('e'):
                    arq = nome + '.' + prefixo + ext
                else:
                    arq = prefixo + f

            if f != arq:
                if alterar:
                    os.rename(os.path.join(pathname, f),
                              os.path.join(pathname, arq))
                tupla = os.path.join(pathname, f), os.path.join(pathname, arq)
                saida += tupla,

            total += 1

    return total, saida

if __name__ == '__main__':

    print('Renomeador de Arquivos - nº7')
    print('Por Christian Haagensen Gontijo, (C) 2021')
    print('-' * 50)

    if not sys.version_info[:2] >= (3, 4):
        print('Use Python 3.4 ou superior para rodar este programa.')
        sys.exit(2)

    op = ObtemParametros()

    par1 = op.Parametro("Path", obrigatorio=True)
    par2 = op.Parametro("Prefixo a adicionar", True)
    par3 = op.Parametro("Isto é um teste?", valores_validos=("s", "n"))
    par4 = op.Parametro("Aplicar sobre nome completo do arquivo, só o nome, "
                        "ou só a extensão?", valores_validos=("n", "e", "c"))
    op.parametros = (par1, par2, par3, par4)

    nome = os.path.basename(sys.argv[0])
    op.texto_ajuda = f'''\
        Este programa adiciona, para cada arquivo em um determinado
        path, um prefixo ao nome e/ou extensão.

        Sintaxe:
        {nome} PATH PREFIXO [TESTE] [APLICAR_EM]

        Onde:
        PATH é o path onde está(ão) o(s) arquivo(s) a alterar.
            Se houver espaços, o path deve ser informado entre aspas.
            Este parâmetro é obrigatório!
        PREFIXO é a string que será adicionada.
            Se houver espaços, o texto deve ser informado entre aspas.
            Este parâmetro é obrigatório!
        TESTE é opcional, e indica se o programa está sendo executado em
            "modo teste", isto é, as alterações não serão gravadas.
            Informe "S" para sim (padrão) ou "N" para não.
        APLICAR_EM é opcional. Informe onde a alteração será aplicada:
            no nome completo do arquivo, especificando "C"; ou
            no nome do arquivo, especificando "N" (padrão); 
            ou somente na extensão do arquivo, especificando "E".
        '''

    # Obtém parâmetros da linha de comando, ou em modo interativo
    path, prefixo, teste, aplicarSobre = op.obtem()
    alterar = (teste == 'n')

    # Exibe o que será feito
    print()
    print(f'Path: "{path}"')
    print(f'Adicionado "{prefixo}" (', end='')
    if aplicarSobre == 'c':
        print('no nome completo do arquivo)')
    elif aplicarSobre == 'e':
        print('na extensão)')
    else:
        print('no nome do arquivo)')
    print ('Modo teste:', 'sim' if not alterar else 'não', '\n')

    total, arquivos = PrefixaArquivo(path, prefixo, aplicarSobre, alterar)

    # Exibição dos resultados
    if len(arquivos) > 0:
        for arqvelho, arqnovo in arquivos:
            print(arqvelho + ' -> ' + arqnovo + (' *' if not alterar else ''))
        print('Concluído, %d arquivos, %d ' % (total, len(arquivos)) +
              ('SERIAM ' if not alterar else '') + 'alterados.\n')
    else:
        print('Nenhum arquivo alterado.')

