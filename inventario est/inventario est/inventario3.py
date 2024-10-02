import sqlite3

# Conexão com o banco de dados e criação da tabela
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
    nome = input("Digite o nome do item: ")
    quantidade = int(input("Digite a quantidade: "))
    preco = float(input("Digite o preço: "))

    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO inventario (nome, quantidade, preco) VALUES (?, ?, ?)",
                   (nome, quantidade, preco))
    conexao.commit()
    conexao.close()
    print("Item inserido com sucesso!")

# Função para alterar um item existente
def alterar_item():
    listar_itens()
    id_item = int(input("Digite o ID do item que deseja alterar: "))
    nome = input("Digite o novo nome do item: ")
    quantidade = int(input("Digite a nova quantidade: "))
    preco = float(input("Digite o novo preço: "))

    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE inventario SET nome=?, quantidade=?, preco=? WHERE id=?",
                   (nome, quantidade, preco, id_item))
    conexao.commit()
    conexao.close()
    print("Item alterado com sucesso!")

# Função para excluir um item
def excluir_item():
    listar_itens()
    id_item = int(input("Digite o ID do item que deseja excluir: "))

    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM inventario WHERE id=?", (id_item,))
    conexao.commit()
    conexao.close()
    print("Item excluído com sucesso!")

# Função para listar todos os itens na tabela
def listar_itens():
    conexao = sqlite3.connect('inventario.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM inventario")
    itens = cursor.fetchall()
    
    print("\nID | Nome        | Quantidade | Preço")
    print("---------------------------------------")
    for row in itens:
        print(f"{row[0]:<3} | {row[1]:<10} | {row[2]:<10} | R$ {row[3]:<6.2f}")
    
    conexao.close()

# Função principal do menu
def menu():
    while True:
        print("\nMenu:")
        print("1. Inserir item")
        print("2. Alterar item")
        print("3. Excluir item")
        print("4. Listar itens")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_item()
        elif opcao == '2':
            alterar_item()
        elif opcao == '3':
            excluir_item()
        elif opcao == '4':
            listar_itens()
        elif opcao == '5':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Conectar ao banco de dados e iniciar o menu
conectar_db()
menu()
