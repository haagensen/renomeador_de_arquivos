#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ObtemParametros
    Escrito por Christian Haagensen Gontijo, maio/2020
"""
import sys, os.path as osp


class ObtemParametros:
    """
    ObtemParametros
    ===============

    Uma classe para obtenção de parâmetros passados a programas,
    via "linha de comando" ou (se nenhum parâmetro tiver sido passado)
    através de um "modo interativo", onde o programa irá pedir cada
    um dos parâmetros desejados.

    Para tanto, basta criar diversos objetos "Parametro" (tantos quanto 
    o seu programa esperar), definindo obrigatoriedade, valores válidos,
    etc, e adicioná-los à lista "parametros".

    Feito isto, é apenas questão de chamar o método "obtem()" para que
    a classe obtenha os valores de cada um dos parâmetros especificados.

    O usuário também pode conseguir uma "ajuda" a partir daqui: se ele
    especificar, na linha de comando, um parâmetro de ajuda (por padrão,
    "/?", ou variantes como "/h", "-?", "-h" ou "--help"; tudo isso ajustável
    via variável "parametros_ajuda"), ele receberá a ajuda definida na
    variável "texto_ajuda".

    """

    texto_ajuda = ''
    parametros_ajuda = ('/?', '/h', '-?', '-h', '--help')
    parametros = []

    class Parametro:
        """
        Classe auxiliar para obtenção de um "parâmetro", ou seja, 
        um argumento a ser passado a um programa, com validações de
        valores.
        """

        _dic = dict()

        def __init__(self, 
                     nome, 
                     obrigatorio = False,
                     valores_validos = None,
                     sensivel_a_caso = False):
            """
            nome: Texto a ser apresentado ao usuário, quando o 
                programa pedir a ele, em "modo interativo", o valor
                deste parâmetro.
            obrigatorio: Define se o parâmetro deve ser especificado.
            valores_validos: Opcional. Tupla indicando os valores válidos
                que o parâmetro pode ter. Se informada, deve conter ao
                menos um elemento, que será considerado o "valor padrão",
                usado caso o usuário responda algo considerado "inválido"
                (ou seja, algo que não estiver nesta tupla).
            sensivel_a_caso: Opcional. Indica se a resposta dada pelo
                usuário deve diferenciar maiúsculas de minúsculas. Por
                padrão, nenhuma diferenciação é feita.
            """

            if not isinstance(obrigatorio, bool):
                msg = 'Parâmetro "obrigatorio" deve ser um booleano.'
                raise TypeError(msg)
            elif not isinstance(sensivel_a_caso, bool):
                msg = 'Parâmetro "sensivel_a_caso" deve ser um booleano.'
                raise TypeError(msg)
            elif valores_validos is not None:
                if not isinstance(valores_validos, tuple):
                    msg = 'Parâmetro "valores_validos" deve ser uma tupla.'
                    raise TypeError(msg)
                elif len(valores_validos) < 1:
                    raise ValueError('Parâmetro "valores_validos", '
                                     'se especificado, deve conter '
                                     'ao menos um item.')

            self._dic = {"nome": nome, 
                         "obrigatorio": obrigatorio,
                         "sensivel_a_caso": sensivel_a_caso}
            if valores_validos is not None:
                self._dic["valores_validos"] = valores_validos

        def __repr__(self):
            rep = (f'Nome: {self._dic["nome"]}, '
                  f'obrigatório: {str(self._dic["obrigatorio"])}, '
                  f'sensivel_a_caso: {str(self._dic["sensivel_a_caso"])}')
            if 'valores_validos' in self._dic:
                rep += ', valores válidos: ' + str(self._dic["valores_validos"])
            return rep

    def _obtem_resposta_valida(self, valor_informado, param):
        """
        Verifica se o "valor informado" está entre os "valores válidos"
        para uma resposta. Se estiver, retorna o próprio valor; se não, 
        retorna o "valor padrão" (primeiro elemento dos "valores válidos")
        """
        resposta = valor_informado
        if 'valores_validos' in param._dic:
            if param._dic["sensivel_a_caso"]:
                resposta = (valor_informado
                           if valor_informado in param._dic["valores_validos"]
                           else param._dic["valores_validos"][0])
            else:
                resposta = (valor_informado
                           if valor_informado.lower() in
                            [x.lower() for x in param._dic["valores_validos"]]
                           else param._dic["valores_validos"][0])
        return resposta

    def _obtem_parametros_modo_interativo(self):

        if len(self.parametros_ajuda) > 0:
            print(f'Inicie este programa com "{osp.basename(sys.argv[0])} '
                  f'{self.parametros_ajuda[0]}" se precisar de'
                   ' ajuda quanto aos parâmetros pedidos abaixo.')

        saida = list()

        for param in self.parametros:

            # monta uma string contendo os "valores válidos" para este 
            # parâmetro, e o valor "default" (que é o primeiro valor válido)
            vv = ''
            if 'valores_validos' in param._dic:
                vv += ' ('
                vv += ''.join([str(valor) + '/' 
                         for valor in param._dic["valores_validos"]])[:-1]
                vv += ') [' + param._dic["valores_validos"][0] + ']'

            resposta = input(f'{param._dic["nome"]}{vv}: ')

            # Parâmetro obrigatório?
            if param._dic["obrigatorio"] and resposta == '':
                print('Este parâmetro é obrigatório. Não é possível continuar.')
                sys.exit(1)

            # Resposta informada está entre os "valores válidos"
            # para uma resposta?
            resposta = self._obtem_resposta_valida(resposta, param)
            saida.append(resposta)

        return saida

    def _obtem_parametros_linha_comando(self):

        saida = list()

        # Cada parâmetro passado via linha de comando é associado com
        # os "parâmetros" definidos nesta classe, na ordem informada.
        for i in range(1, len(self.parametros) + 1):

            # O parâmetro pode ou não ter sido informado.
            if i > len(sys.argv) - 1:

                # Parâmetro esperado, mas não passado na linha de comando
                if self.parametros[i-1]._dic["obrigatorio"]:
                    print(f'O {i}º parâmetro é obrigatório, mas não foi '
                           'especificado. Não é possível continuar.')
                    sys.exit(1)
                elif "valores_validos" in self.parametros[i-1]._dic:
                    resposta = self.parametros[i-1]._dic["valores_validos"][0]
                else:
                    resposta = ''

            else:

                # Verifica se a resposta informada está entre
                # os "valores válidos" para uma resposta.
                resposta = self._obtem_resposta_valida(sys.argv[i], 
                                                       self.parametros[i-1])

            saida.append(resposta)

        return saida

    def obtem(self):
        """ Obtém parâmetros passados na linha de comando, e 
        retorna cada um deles.
        """

        # Requerendo ajuda?
        if len(sys.argv) > 1 and sys.argv[1] in self.parametros_ajuda:
            from textwrap import dedent 
            print(dedent(self.texto_ajuda))
            sys.exit(1)
        # Nenhum argumento: usa o "modo interativo"
        elif len(sys.argv) == 1:
            args = self._obtem_parametros_modo_interativo()
        else:
            args = self._obtem_parametros_linha_comando()

        # Neste ponto, "args" pode não conter todos os parâmetros esperados
        # pelo programa (podem ter sido passados parâmetros vazios, por 
        # exemplo). Retorna uma coleção contendo o mesmo número de
        # elementos que o número de parâmetros
        for _ in range(len(self.parametros) - len(args)):
            args.append(None)

        return args


if __name__ == '__main__':

    nome = osp.basename(sys.argv[0])

    op = ObtemParametros()

    op.texto_ajuda = (f"""
    Este programa demonstra o uso da classe ObtemParametros,
    num falso renomeador de arquivos em linha de comando.

    Sintaxe:
    {nome} PATH TEXTO NOVO [TESTE] [APLICAR_EM]

    Opções:
    PATH é o path do arquivo. Deve ser informado.
    TEXTO é a string a procurar. Deve ser informada.
    NOVO é a string a ser incluída no lugar da anterior.
    TESTE é opcional, informe "S" para sim (padrão) ou "N" para não.
    APLICAR_EM é opcional. Valores válidos são "C", "N" (padrão),
        ou ainda "E" para outra coisa qualquer.
    """)

    par1 = op.Parametro('Path', obrigatorio=True)
    par2 = op.Parametro('Tirar esta string', True)
    par3 = op.Parametro('Trocar por')
    par4 = op.Parametro('Isto é um teste?', valores_validos=('s', 'n'))
    par5 = op.Parametro('Aplicar c, n ou e?', valores_validos=('n', 'e', 'c'))

    op.parametros = [par1, par2, par3, par4, par5]

    # Apresenta cabeçalho
    print('Programa de exemplo de classe')
    print('Por Christian Haagensen Gontijo, (C) 2020')
    print('-' * 50)

    # Faz a mágica
    path, a_trocar, trocar_por, teste, aplicar_sobre = op.obtem()

    # Tcha-raaam!
    print(f'Path: "{path}", trocar: "{a_trocar}", por: "{trocar_por}", '
          f'teste? {teste}, aplicar sobre: {aplicar_sobre}')
    print('Fim do exemplo da classe.')
