#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from obtemparametros import ObtemParametros


def uppercase_arquivos(path, aplicar_sobre="n", alterar=False):
    total = 0
    saida = tuple()

    for pathname, dirs, filenames in os.walk(path):
        for f in filenames:

            if aplicar_sobre == "c":
                arq = f.upper()
            else:
                pos = f.rfind(".")
                if aplicar_sobre == "n":
                    arq = f[0:pos].upper() + f[pos:]
                else:
                    arq = f[0:pos] + f[pos:].upper()

            if f != arq:
                if alterar:
                    os.rename(os.path.join(pathname, f),
                              os.path.join(pathname, arq))
                tupla = os.path.join(pathname, f), os.path.join(pathname, arq)
                saida += tupla,

            total += 1

    return total, saida


if __name__ == "__main__":

    print('Renomeador de Arquivos - nº3')
    print('Por Christian Haagensen Gontijo, (C) 2020')
    print('-' * 50)

    if not sys.version_info[:2] >= (3, 4):
        print("Use Python 3.4 ou superior para rodar este programa.")
        sys.exit(1)

    op = ObtemParametros()
    par1 = op.Parametro("Path", obrigatorio=True)
    par2 = op.Parametro("Isto é um teste?", valores_validos=("s", "n"))
    par3 = op.Parametro("Aplicar sobre nome completo do arquivo, só o nome, "
                        "ou só a extensão?", valores_validos=("n", "e", "c"))
    op.parametros = (par1, par2, par3)

    nome = os.path.basename(sys.argv[0])
    op.texto_ajuda = f'''\
        Este programa altera o nome dos arquivos em determinado path
        para maiúsculas.
        
        Sintaxe:
        {nome} PATH [TESTE] [APLICAR_EM]

        Onde:
        PATH é o path onde está(ão) o(s) arquivo(s) a alterar.
            Se houver espaços, o path deve ser informado entre aspas.
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
    path, teste, aplicarSobre = op.obtem()
    alterar = (teste == 'n')

    total, arquivos = uppercase_arquivos(path, aplicarSobre, alterar)

    for arqvelho, arqnovo in arquivos:
        print(arqvelho + " -> " + arqnovo +
                (" *" if (not alterar) else ""))
    print("Concluído, %d arquivos, %d " % (total, len(arquivos)) +
            ("SERIAM " if (not alterar) else "") + "alterados.")
    print()

    print("Terminado.")
