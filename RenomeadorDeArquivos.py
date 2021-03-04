#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter
import os


class Eventos:
    def ObtemValor():
        return 3.141592


class RenomeadorDeArquivos:

    # Handlers
    def cmdRenomear_Click(self):
        e = Eventos
        valor = e.ObtemValor()
        tkinter.messagebox.showinfo(title="Aviso", message="Valor é %f" %valor)

    def PopulaLista(self, lst):
        for file in os.environ:
            lst.insert(file)

    # Funções internas
    def __init__(self, tk):
        self.constroiGUI(tk)
        self.PopulaLista(self.lstArquivos)

    def constroiGUI(self, tk):
        self.title = "olá"
        tkinter.title = "oi"
        tk.title = "Renomeador de Arquivos"
        self.cmdRenomear = tkinter.Button()
        self.cmdRenomear.config(text="Renomear arquivos")
        self.cmdRenomear.config(command=self.cmdRenomear_Click)
        self.cmdRenomear.pack()
        self.lstArquivos = tkinter.Listbox()
        self.lstArquivos.pack()


tk = tkinter.Tk()
r = RenomeadorDeArquivos(tk)
tk.mainloop()
