#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from obtemparametros import ObtemParametros


def alterna_no_caracter(path, caractere='-', alterar=False):

    if caractere.strip() == '':
        caractere = "-"
    total = 0
    saida = tuple()

    for pathname, _, filenames in os.walk(path):

        for f in filenames:

            arq, extensao = os.path.splitext(f)
            arq = arq.split(f" {caractere} ")
            if len(arq) == 2:
                arq = arq[1] + " " + caractere + " " + arq[0] + extensao
            else:
                arq = f

            if f != arq:
                if alterar:
                    os.rename(os.path.join(pathname, f),
                              os.path.join(pathname, arq))
                tupla = os.path.join(pathname, f), os.path.join(pathname, arq)
                saida += tupla,

            total += 1

    return total, saida


if __name__ == "__main__":

    print('Renomeador de Arquivos - nº6')
    print('Por Christian Haagensen Gontijo, (C) 2020')
    print('-' * 50)

    if not sys.version_info[:2] >= (3, 4):
        print("Use Python 3.4 ou superior para rodar este programa.")
        sys.exit(1)

    op = ObtemParametros()
    par1 = op.Parametro("Path", obrigatorio=True)
    par2 = op.Parametro("Caractere separador")
    par3 = op.Parametro("Isto é um teste?", valores_validos=("s", "n"))
    op.parametros = (par1, par2, par3)

    nome = os.path.basename(sys.argv[0])
    op.texto_ajuda = f'''\
        Este programa verifica determinado path, alterando o nome daqueles
        arquivos que contenham um determinado separador (por padrão, um "-")
        em seu nome, de forma que o que vem APÓS o separador passará a vir
        ANTES dele, e vice-versa.

        Por exemplo, "Becoming Steve Jobs - Brent Schlender.epub" => 
                     "Brent Schlender - Becoming Steve Jobs.epub"

        Sintaxe:
        {nome} PATH [SEPARADOR] [TESTE]

        Onde:
        PATH é o path onde está(ão) o(s) arquivo(s) a alterar.
            Se houver espaços, o path deve ser informado entre aspas.
            Este parâmetro é obrigatório!
        SEPARADOR é opcional. O caractere separador a usar. Por padrão, "-".
        TESTE é opcional, e indica se o programa está sendo executado em
            "modo teste", isto é, as alterações não serão gravadas.
            Informe "S" para sim (padrão) ou "N" para não.
        '''

    # Obtém parâmetros da linha de comando, ou em modo interativo
    path, caractere, teste = op.obtem()
    alterar = (teste == 'n')

    total, arquivos = alterna_no_caracter(path, caractere, alterar)

    for arqvelho, arqnovo in arquivos:
        print(arqvelho + " -> " + arqnovo +
                (" *" if (not alterar) else ""))
    print("Concluído, %d arquivos, %d " % (total, len(arquivos)) +
            ("SERIAM " if (not alterar) else "") + "alterados.")
    print()

    print("Terminado.")
