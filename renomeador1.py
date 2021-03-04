#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from obtemparametros import ObtemParametros

def TrocaNoArquivo(path, velho, novo, aplicarsobre='n', alterar=False):
    """
    Para cada arquivo em um determinado diretório, substitui uma
    string por outra.

    path Indica o diretório a ser examinado.
    velho É a string que será pesquisada.
    novo É a nova string a ser colocada.
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

            if aplicarsobre.lower().startswith('c'):
                arq = f.replace(velho, novo)
            else:
                pos = f.rfind('.')
                if aplicarsobre.lower().startswith('e'):
                    arq = f[0:pos] + f[pos:].replace(velho, novo)
                else:
                    arq = f[0:pos].replace(velho, novo) + f[pos:]

            if f != arq:
                if alterar:
                    os.rename(os.path.join(pathname, f),
                              os.path.join(pathname, arq))
                tupla = os.path.join(pathname, f), os.path.join(pathname, arq)
                saida += tupla,

            total += 1

    return total, saida

if __name__ == '__main__':

    print('Renomeador de Arquivos - nº1')
    print('Por Christian Haagensen Gontijo, (C) 2020')
    print('-' * 50)

    if not sys.version_info[:2] >= (3, 4):
        print('Use Python 3.4 ou superior para rodar este programa.')
        sys.exit(2)

    op = ObtemParametros()

    par1 = op.Parametro("Path", obrigatorio=True)
    par2 = op.Parametro("Tirar esta string", True)
    par3 = op.Parametro("Trocar por")
    par4 = op.Parametro("Isto é um teste?", valores_validos=("s", "n"))
    par5 = op.Parametro("Aplicar sobre nome completo do arquivo, só o nome, "
                        "ou só a extensão?", valores_validos=("n", "e", "c"))
    op.parametros = (par1, par2, par3, par4, par5)

    nome = os.path.basename(sys.argv[0])
    op.texto_ajuda = f'''\
        Este programa substitui, para cada arquivo em um determinado
        path, uma string por outra.

        Sintaxe:
        {nome} PATH TEXTO_VELHO TEXTO_NOVO [TESTE] [APLICAR_EM]

        Onde:
        PATH é o path onde está(ão) o(s) arquivo(s) a alterar.
            Se houver espaços, o path deve ser informado entre aspas.
            Este parâmetro é obrigatório!
        TEXTO_VELHO é a string que será alterada.
            Se houver espaços, o texto deve ser informado entre aspas.
            Este parâmetro é obrigatório!
        TEXTO_NOVO é a string a ser incluída no lugar da anterior.
            Se houver espaços, o texto deve ser informado entre aspas.
        TESTE é opcional, e indica se o programa está sendo executado em
            "modo teste", isto é, as alterações não serão gravadas.
            Informe "S" para sim (padrão) ou "N" para não.
        APLICAR_EM é opcional. Informe onde a alteração será aplicada:
            no nome completo do arquivo, especificando "C"; ou
            no nome do arquivo, especificando "N" (padrão); 
            ou somente na extensão do arquivo, especificando "E".
        '''

    # Obtém parâmetros da linha de comando, ou em modo interativo
    path, velho, novo, teste, aplicarSobre = op.obtem()
    alterar = (teste == 'n')

    # Exibe o que será feito
    print()
    print(f'Path: "{path}"')
    print(f'Alterando "{velho}" para "{novo}" (', end='')
    if aplicarSobre == 'c':
        print('no nome completo do arquivo)')
    elif aplicarSobre == 'e':
        print('na extensão)')
    else:
        print('no nome do arquivo)')
    print ('Modo teste:', 'sim' if not alterar else 'não', '\n')

    total, arquivos = TrocaNoArquivo(path, velho, novo, aplicarSobre, alterar)

    # Exibição dos resultados
    if len(arquivos) > 0:
        for arqvelho, arqnovo in arquivos:
            print(arqvelho + ' -> ' + arqnovo + (' *' if not alterar else ''))
        print('Concluído, %d arquivos, %d ' % (total, len(arquivos)) +
              ('SERIAM ' if not alterar else '') + 'alterados.\n')
    else:
        print('Nenhum arquivo alterado.')
