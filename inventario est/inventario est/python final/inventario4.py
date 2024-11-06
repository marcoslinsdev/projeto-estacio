import sqlite3
import tkinter as tk
from tkinter import messagebox

# Função para conectar ao banco de dados e criar a tabela
def conectar_db():
    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        preco REAL NOT NULL)''')
    conexao.commit()
    conexao.close()

# Função para inserir novo item no inventário
def inserir_item():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()
    
    if nome and quantidade.isdigit() and preco.replace('.', '', 1).isdigit():
        conexao = sqlite3.connect('inventario.db')
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO inventario (nome, quantidade, preco) VALUES (?, ?, ?)",
                       (nome, int(quantidade), float(preco)))
        conexao.commit()
        conexao.close()
        listar_itens()
        messagebox.showinfo("Sucesso", "Item inserido com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")

# Função para alterar um item existente
def alterar_item():
    id_item = entry_id.get()
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()
    
    if id_item.isdigit() and nome and quantidade.isdigit() and preco.replace('.', '', 1).isdigit():
        conexao = sqlite3.connect('inventario.db')
        cursor = conexao.cursor()
        cursor.execute("UPDATE inventario SET nome=?, quantidade=?, preco=? WHERE id=?",
                       (nome, int(quantidade), float(preco), int(id_item)))
        conexao.commit()
        conexao.close()
        listar_itens()
        messagebox.showinfo("Sucesso", "Item alterado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")

# Função para excluir um item
def excluir_item():
    id_item = entry_id.get()
    
    if id_item.isdigit():
        conexao = sqlite3.connect('inventario.db')
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM inventario WHERE id=?", (int(id_item),))
        conexao.commit()
        conexao.close()
        listar_itens()
        messagebox.showinfo("Sucesso", "Item excluído com sucesso!")
    else:
        messagebox.showwarning("Erro", "Digite um ID válido para excluir.")

# Função para listar todos os itens na tabela
def listar_itens():
    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM inventario")
    itens = cursor.fetchall()
    conexao.close()
    
    # Limpar a lista antes de inserir novos itens
    listbox_itens.delete(0, tk.END)
    
    # Inserir cada item na listbox
    for row in itens:
        listbox_itens.insert(tk.END, f"ID: {row[0]}, Nome: {row[1]}, Quantidade: {row[2]}, Preço: R$ {row[3]:.2f}")

# Função para limpar campos
def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

# Interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Inventário")

# Campos de entrada
frame_campos = tk.Frame(root)
frame_campos.pack(pady=10)

tk.Label(frame_campos, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(frame_campos, width=5)
entry_id.grid(row=0, column=1, padx=5)

tk.Label(frame_campos, text="Nome").grid(row=0, column=2)
entry_nome = tk.Entry(frame_campos, width=20)
entry_nome.grid(row=0, column=3, padx=5)

tk.Label(frame_campos, text="Quantidade").grid(row=1, column=0)
entry_quantidade = tk.Entry(frame_campos, width=5)
entry_quantidade.grid(row=1, column=1, padx=5)

tk.Label(frame_campos, text="Preço").grid(row=1, column=2)
entry_preco = tk.Entry(frame_campos, width=10)
entry_preco.grid(row=1, column=3, padx=5)

# Botões de ação
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_inserir = tk.Button(frame_botoes, text="Inserir Item", command=inserir_item)
btn_inserir.grid(row=0, column=0, padx=5)

btn_alterar = tk.Button(frame_botoes, text="Alterar Item", command=alterar_item)
btn_alterar.grid(row=0, column=1, padx=5)

btn_excluir = tk.Button(frame_botoes, text="Excluir Item", command=excluir_item)
btn_excluir.grid(row=0, column=2, padx=5)

btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos)
btn_limpar.grid(row=0, column=3, padx=5)

# Lista de itens
listbox_itens = tk.Listbox(root, width=60, height=10)
listbox_itens.pack(pady=10)

# Iniciar a conexão e carregar itens
conectar_db()
listar_itens()

# Executar a interface gráfica
root.mainloop()
