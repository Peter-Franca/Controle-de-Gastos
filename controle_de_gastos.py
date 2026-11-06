import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA_PROGRAMA, "controle_gastos.db")


def visualizar_gastos():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    print("\n--- LISTA DE GASTOS ---")
    cursor.execute("SELECT * FROM gastos")
    gastos = cursor.fetchall()

    if not gastos:
        print("Nenhum gasto encontrado!")
    else:
        for registro in gastos:
            print(f"ID: {registro[0]} | Categoria: {registro[1]} | Valor: R${registro[2]:.2f} | Data: {registro[3]}")

    conexao.close()

def inicializar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

    

def add_gasto(categoria, valor, data):
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    comando_sql = """
        INSERT INTO gastos (descricao, valor, data)
        VALUES (?, ?, ?)
    """
    cursor.execute(comando_sql, (categoria, valor, data))
    conexao.commit()
    conexao.close()

inicializar_banco()

print(""" PROGRAMA DE CONTROLE DE GASTOS
Organize os seus gastos mês a mês!""")

finalizar_app = False

while not finalizar_app:
    opcao = int(input("""\nSelecione uma opção:
    1 - Adicionar gastos
    2 - Visualizar/Editar gastos
    3 - Excluir gastos
    4 - Relatórios e gráficos
    5 - Sair
    Escolha uma opção: """))
    
    

    if opcao == 1:
        categorias = {
            "1": "Alimentação",
            "2": "Transporte",
            "3": "Saúde",
            "4": "Lazer",
            "5": "Educação",
            "6": "Compras",
            "7": "Outros"
        }

        descricao_gasto = input("""Selecione a categoria:
        1 - Alimentação
        2 - Transporte
        3 - Saúde
        4 - Lazer
        5 - Educação
        6 - Compras
        7 - Outros 
        Escolha: """)

        categoria_gasto = categorias.get(descricao_gasto)

        if categoria_gasto is None:
            print("Categoria inválida!")
            continue

        valor_gasto = float(input("Digite o valor (Exemplo: 50,00 - Utilize vírgula): ").replace(",", "."))
        data_gasto = input("Digite a data (DD/MM/AAAA): ")

       
        add_gasto(categoria_gasto, valor_gasto, data_gasto)
        print(f"\nGasto em '{categoria_gasto}' adicionado com sucesso!")

    elif opcao == 2:
        opcao_menu_2 = int(input("""\nVisualizar/Editar Gastos
        1 - Visualizar todos os gastos
        2 - Editar um gasto
        3 - Voltar ao menu principal
        """))
        if opcao_menu_2 == 1:
            visualizar_gastos()
        
        elif opcao_menu_2 == 2:
            visualizar_gastos()
            conexao = sqlite3.connect(CAMINHO_BANCO)
            cursor = conexao.cursor()
            
            id_gasto = int(input("Digite o ID do gasto que deseja alterar: "))

            cursor.execute(
                "SELECT * FROM gastos WHERE id = ?",
                (id_gasto,)
            )

            gasto = cursor.fetchone()

            if gasto is None:
                print("Gasto não encontrado!")
                conexao.close()
                continue

            opcao_edicao = int(input("""
            O que deseja alterar?

            1 - Valor
            2 - Data
            """))
            if opcao_edicao == 1:
                alteracao_valor = float(input("Defina o novo valor para esse gasto: ").replace(",", "."))

                cursor.execute(
                    "UPDATE gastos SET valor = ? WHERE id = ?",
                    (alteracao_valor, id_gasto)
                )
                conexao.commit()
                conexao.close()

                print("Valor alterado com sucesso!")

            elif opcao_edicao == 2:
                alteracao_data = input("Digite a nova data (DD/MM/AAAA): ")

                cursor.execute(
                    "UPDATE gastos SET data = ? WHERE id = ?",
                    (alteracao_data, id_gasto)
                )
                conexao.commit()
                conexao.close()

                print("Data alterada com sucesso!")

            else:
                print("Opção inválida!")
                conexao.close()

        elif opcao_menu_2 == 3:
            print("Voltando ao menu principal...")
                

    elif opcao == 3:
        visualizar_gastos()

        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()

        id_gasto = int(input("Digite o ID do gasto que deseja excluir: "))

        cursor.execute(
            "SELECT * FROM gastos WHERE id = ?",
            (id_gasto,)
        )

        gasto = cursor.fetchone()
        if gasto is None:
            print("Gasto não encontrado!")
            conexao.close()
            continue

        print(f"ID: {gasto[0]} | Categoria: {gasto[1]} | Valor: R${gasto[2]:.2f} | Data: {gasto[3]}")

        opcao_exclusao = int(input("""Tem certeza que deseja excluir esse gasto? 
        1 - Sim
        2 - Não
         """))
        if opcao_exclusao == 1:
            cursor.execute(
                "DELETE FROM gastos WHERE id = ?",
                (id_gasto,)
        )
            conexao.commit()

            print("Gasto excluído com sucesso!")

        elif opcao_exclusao == 2:
            print("""Exclusão cancelada,
        voltando ao menu principal...""")

        else:
            print("""Opção inválida,
        voltando ao menu principal...""")
             
        conexao.close()

    
    elif opcao == 4:
        
        conexao = sqlite3.connect(CAMINHO_BANCO)
        df = pd.read_sql_query("SELECT * FROM gastos", conexao)
        if df.empty:
            print("Nenhum gasto cadastrado para gerar relatórios!")
            conexao.close()
            continue

        
        opcao_relatorio = int(input("""Relatórios e gráficos
        1 - Gerar relatório básico
        2 - Gerar gráfico
        """))

        if opcao_relatorio == 1:
            
            print(df.head())
            
            total_gastos = df["valor"].sum()
            print(f"Total de gastos: R${total_gastos:.2f}")

            quantidade_gastos = len(df)
            print(f"Quantidade de gastos: {quantidade_gastos}")

        elif opcao_relatorio == 2:
            gastos_categoria = df.groupby("descricao")["valor"].sum()
            gastos_categoria = gastos_categoria.reset_index()
            sns.barplot(data=gastos_categoria, x="descricao", y="valor")
            plt.title("Gastos por categoria")
            plt.xlabel("Categorias")
            plt.ylabel("Valor (R$)")
            plt.show()
            
            
            print(gastos_categoria)

        conexao.close()

    elif opcao == 5:
            print("Saindo do programa... Até mais!")
            finalizar_app = True

    else:
        print("Opção inválida! Escolha uma opção de 1 a 5.")    





    



            





    
    

            






          
        






