#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

print()
print('Renomeador 2a # por Christian Haagensen Gontijo')
print('-' * 60)
print('Este programa substitui, para cada arquivo em um ' +
      'determinado path, caracteres com codificação inválida ' +
      'para UTF-8.')
print()

total = 0
i = 0
gfse = sys.getfilesystemencoding()
path = input("Path: ")
print()

for pathname, dirs, filenames in os.walk(path):
    for f in filenames:

        utf = f.encode("utf-8")

        print("Arquivo ....:   " + f)
        # print ("GFSE: ", end=""); print (f.encode(gfse, errors="replace"))
        print("UTF-8 ......: ", end="")
        print(utf)
        # print ("UTF-8 Dec...:"  + utf.decode())
        # print ()

        novo = utf  # usa UTF-8, com outros ocorre erro
        novo = novo.replace(b"a\xcc\x81", b"\xc3\xa1")  # á
        novo = novo.replace(b"e\xcc\x81", b"\xc3\xa9")
        novo = novo.replace(b"minas_compradas\xcc\x81", b"\xc3\xad")
        novo = novo.replace(b"o\xcc\x81", b"\xc3\xb3")
        novo = novo.replace(b"u\xcc\x81", b"\xc3\xba")
        novo = novo.replace(b"o\xcc\x82", b"\xc3\xb4")  # ô
        novo = novo.replace(b"o\xcc\x83", b"\xc3\xb5")  # õ
        novo = novo.replace(b"c\xcc\xa7", b"\xc3\xa7")  # ç
        novo = novo.replace(b"a\xcc\x83", b"\xc3\xa3")  # ã
        novo = novo.replace(b"a\xcc\x82", b"\xc3\xa2")  # â
        novo = novo.replace(b"e\xcc\x82", b"\xc3\xaa")  # ê
        novo = novo.replace(b"A\xcc\x80", b"\xc3\x80")  # À
        novo = novo.replace(b"E\xcc\x81", b"\xc3\x89")  # É
        novo = novo.replace(b"U\xcc\x81", b"\xc3\x9a")  # Ú
        novo = novo.replace(b"A\xcc\x81", b"\xc3\x81")  # Á

        # print ("Novo, bytes : ", end="")
        # print (novo)
        # print ("Novo (str) .:   " + novo.decode())

        if novo.decode() != f:
            print("Arquivo: " + f)
            print("Novo: " + novo.decode())
            # print ("Arquivo e Novo *diferem *, renomeando...")
            os.rename(os.path.join(pathname, f),
                      os.path.join(pathname, novo.decode()))
            i += 1

        # print('-' * 60)
        total += 1

print("%d arquivos, %d alterados." % (total, i))
