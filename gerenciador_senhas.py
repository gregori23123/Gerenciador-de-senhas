#!/usr/bin/env python3
"""
Gerenciador de Senhas - NOC
Armazena senhas únicas por usuário em arquivo local (senhas.json)
"""

import json
import os
import secrets
import string
import sys
from datetime import datetime

# ─── Configuração ───────────────────────────────────────────────────────────────
ARQUIVO = "senhas.json"
CHARSET = string.ascii_letters + string.digits + "@#!$"
TAMANHO = 10

# ─── Cores ANSI ────────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BG_BLUE = "\033[44m"

# ─── Persistência ──────────────────────────────────────────────────────────────
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ─── Utilitários ───────────────────────────────────────────────────────────────
def normalizar(nome):
    return nome.strip().lower()

def gerar_senha():
    return "".join(secrets.choice(CHARSET) for _ in range(TAMANHO))

def limpar():
    os.system("cls" if sys.platform == "win32" else "clear")

def linha(char="─", largura=52):
    print(C.BLUE + char * largura + C.RESET)

def cabecalho():
    limpar()
    largura = 52
    print(C.BG_BLUE + C.WHITE + C.BOLD + " GERENCIADOR DE SENHAS — NOC ".center(largura) + C.RESET)
    dados = carregar()
    print(C.DIM + f" {len(dados)} usuário(s) cadastrado(s)  │  Arquivo: {ARQUIVO}".center(largura) + C.RESET)
    linha()

# ─── Ações ─────────────────────────────────────────────────────────────────────
def cadastrar():
    cabecalho()
    print(f"\n  {C.CYAN}CADASTRAR NOVO USUÁRIO{C.RESET}\n")
    nome = input("  Nome completo: ").strip()
    if not nome:
        print(f"\n  {C.RED}✕ Nome não pode ser vazio.{C.RESET}")
        input("\n  [Enter para voltar]")
        return

    dados = carregar()
    chave = normalizar(nome)

    if chave in dados:
        print(f"\n  {C.YELLOW}⚠  '{dados[chave]['nome']}' já possui senha cadastrada.{C.RESET}")
        print(f"  Use a opção Buscar para visualizá-la.")
        input("\n  [Enter para voltar]")
        return

    senha = gerar_senha()
    dados[chave] = {
        "nome": nome,
        "senha": senha,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    salvar(dados)

    print(f"\n  {C.GREEN}✔ Senha gerada com sucesso!{C.RESET}\n")
    linha("·")
    print(f"  Usuário : {C.WHITE}{C.BOLD}{nome}{C.RESET}")
    print(f"  Senha   : {C.GREEN}{C.BOLD}{senha}{C.RESET}")
    linha("·")
    input("\n  [Enter para voltar]")

def buscar():
    cabecalho()
    print(f"\n  {C.CYAN}BUSCAR USUÁRIO{C.RESET}\n")
    termo = input("  Nome (parcial ou completo): ").strip()
    if not termo:
        input(f"\n  {C.RED}✕ Digite um nome.{C.RESET}  [Enter para voltar]")
        return

    dados = carregar()
    chave_busca = normalizar(termo)
    encontrados = {k: v for k, v in dados.items() if chave_busca in k}

    if not encontrados:
        print(f"\n  {C.RED}✕ Nenhum usuário encontrado para '{termo}'.{C.RESET}")
        input("\n  [Enter para voltar]")
        return

    print(f"\n  {C.GREEN}{len(encontrados)} resultado(s):{C.RESET}\n")
    linha("·")
    for chave, u in encontrados.items():
        print(f"  Usuário : {C.WHITE}{C.BOLD}{u['nome']}{C.RESET}")
        print(f"  Senha   : {C.GREEN}{C.BOLD}{u['senha']}{C.RESET}")
        print(f"  Criado  : {C.DIM}{u['criado_em']}{C.RESET}")
        linha("·")

    input("\n  [Enter para voltar]")

def listar():
    cabecalho()
    print(f"\n  {C.CYAN}TODOS OS USUÁRIOS{C.RESET}\n")
    dados = carregar()

    if not dados:
        print(f"  {C.DIM}Nenhum usuário cadastrado ainda.{C.RESET}")
        input("\n  [Enter para voltar]")
        return

    linha("·")
    for i, (chave, u) in enumerate(sorted(dados.items()), 1):
        print(f"  {C.DIM}{i:02d}.{C.RESET} {C.WHITE}{C.BOLD}{u['nome']:<28}{C.RESET}  "
              f"Senha: {C.GREEN}{u['senha']}{C.RESET}  "
              f"{C.DIM}{u['criado_em']}{C.RESET}")
    linha("·")
    input("\n  [Enter para voltar]")

def excluir():
    cabecalho()
    print(f"\n  {C.CYAN}EXCLUIR USUÁRIO{C.RESET}\n")
    nome = input("  Nome exato do usuário: ").strip()
    if not nome:
        input(f"\n  {C.RED}✕ Nome não pode ser vazio.{C.RESET}  [Enter para voltar]")
        return

    dados = carregar()
    chave = normalizar(nome)

    if chave not in dados:
        print(f"\n  {C.RED}✕ Usuário '{nome}' não encontrado.{C.RESET}")
        input("\n  [Enter para voltar]")
        return

    confirma = input(f"\n  {C.YELLOW}Excluir '{dados[chave]['nome']}'? (s/N): {C.RESET}").strip().lower()
    if confirma == "s":
        del dados[chave]
        salvar(dados)
        print(f"\n  {C.GREEN}✔ Usuário removido.{C.RESET}")
    else:
        print(f"\n  {C.DIM}Cancelado.{C.RESET}")

    input("\n  [Enter para voltar]")

# ─── Menu principal ─────────────────────────────────────────────────────────────
def menu():
    opcoes = {
        "1": ("Cadastrar novo usuário",  cadastrar),
        "2": ("Buscar / Ver senha",       buscar),
        "3": ("Listar todos",             listar),
        "4": ("Excluir usuário",          excluir),
        "0": ("Sair",                     None),
    }

    while True:
        cabecalho()
        print()
        for k, (desc, _) in opcoes.items():
            cor = C.RED if k == "0" else C.CYAN
            print(f"  {cor}[{k}]{C.RESET}  {desc}")
        print()
        linha()
        escolha = input("  Escolha: ").strip()

        if escolha == "0":
            limpar()
            print(f"\n  {C.DIM}Até logo!{C.RESET}\n")
            break
        elif escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print(f"\n  {C.RED}✕ Opção inválida.{C.RESET}")
            input("  [Enter para continuar]")

if __name__ == "__main__":
    menu()
'''
'''
