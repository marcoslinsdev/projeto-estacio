from mailbox import mboxMessage
import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv
import os

# Configurando o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar produto
def add_item():
    name = entry_name.get()
    quantity = entry_quantity.get()
    supplier = entry_supplier.get()

    if not name or not quantity or not supplier:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número")
        return

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (name, quantity, supplier) VALUES (?, ?, ?)', (name, quantity, supplier))
    conn.commit()
    conn.close()
    load_items()
    clear_entries()

# Função para carregar os itens
def load_items():
    tree_inventory.delete(*tree_inventory.get_children())
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    for row in rows:
        tree_inventory.insert('', 'end', values=row)
    conn.close()

# Função para remover item
def remove_item():
    selected_item = tree_inventory.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um item para remover")
        return

    item_id = tree_inventory.item(selected_item, 'values')[0]
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    load_items()

# Função para atualizar item
def update_item():
    selected_item = tree_inventory.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um item para atualizar")
        return

    item_id = tree_inventory.item(selected_item, 'values')[0]
    name = entry_name.get()
    quantity = entry_quantity.get()
    supplier = entry_supplier.get()

    if not name or not quantity or not supplier:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número")
        return

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET name = ?, quantity = ?, supplier = ? WHERE id = ?', (name, quantity, supplier, item_id))
    conn.commit()
    conn.close()
    load_items()
    clear_entries()

# Função para limpar os campos
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_supplier.delete(0, tk.END)

# Função para exportar para CSV
def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    conn.close()

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nome', 'Quantidade', 'Fornecedor'])
        writer.writerows(rows)

    
    mboxMessage.showinfo("Exportação", "Dados exportados com sucesso!")

# Função para importar do CSV
def import_csv():
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pular cabeçalho
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        for row in reader:
            cursor.execute('INSERT INTO inventory (name, quantity, supplier) VALUES (?, ?, ?)', (row[1], row[2], row[3]))
        conn.commit()
        conn.close()

    load_items()
    messagebox.showinfo("Importação", "Dados importados com sucesso!")

# Criando a janela principal com Tkinter
root = tk.Tk()
root.title("Sistema de Controle de Inventário")

# Entradas para nome, quantidade e fornecedor
tk.Label(root, text="Nome do Produto:").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Quantidade:").grid(row=1, column=0)
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=1, column=1)

tk.Label(root, text="Fornecedor:").grid(row=2, column=0)
entry_supplier = tk.Entry(root)
entry_supplier.grid(row=2, column=1)

# Botões para adicionar, remover, atualizar e limpar
tk.Button(root, text="Adicionar", command=add_item).grid(row=3, column=0)
tk.Button(root, text="Remover", command=remove_item).grid(row=3, column=1)
tk.Button(root, text="Atualizar", command=update_item).grid(row=3, column=2)
tk.Button(root, text="Limpar Campos", command=clear_entries).grid(row=3, column=3)

# Botões para exportar/importar CSV
tk.Button(root, text="Exportar para CSV", command=export_csv).grid(row=4, column=0)
tk.Button(root, text="Importar CSV", command=import_csv).grid(row=4, column=1)

# Tabela de inventário
columns = ('id', 'name', 'quantity', 'supplier')
tree_inventory = tk.ttk.Treeview(root, columns=columns, show='headings')
tree_inventory.heading('id', text='ID')
tree_inventory.heading('name', text='Nome do Produto')
tree_inventory.heading('quantity', text='Quantidade')
tree_inventory.heading('supplier', text='Fornecedor')
tree_inventory.grid(row=5, column=0, columnspan=4)

# Carregar itens no início
load_items()

# Inicializando o banco de dados e rodando a aplicação
init_db()
root.mainloop()
