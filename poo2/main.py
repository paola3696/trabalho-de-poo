#Integrantes do grupo: Sarah Evelen, Paola Loeblem, Guilherme Evangelista, Sara Isabelly
#Turma:2°A informática 
#Programação Orientada a Objetos

from collections import Counter
from extra import red,fim, clear,green,yellow

# Contando elementos em uma lista
itens = ["caneta", "lápis", "borracha", "caneta", "caneta", "lápis"]
contagem = Counter(itens)

print("Itens no estoque:")
for item, quantidade in contagem.items():
    print(f"{item}: {quantidade}")

# Importa as classes definidas anteriormente
from usuario import Usuario, ServidorDepae, ProfConselheiro, Avaliador, Turma

def definir_nota(valor):
    try:
        if valor < 0 or valor > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        print(f"Nota {valor} registrada com sucesso.")

    except ValueError as e:
        print((f'{red}Erro: {e}{fim}'))
   

# Testando a função
definir_nota(12)  # Gera uma exceção
definir_nota(8)   # Nota válida

# Função para solicitar login do usuário

#tratamento de exceção com try, except e raise

def solicitar_login():
    try:
        email = input("Digite o seu email: ")
        senha = input("Digite a sua senha: ")

        usuario = Usuario.buscar_usuario_por_email(email)
        if usuario:
            if usuario.login(email, senha):
                return usuario
            else:
                raise ValueError("Senha incorreta.")
        else:
            raise ValueError("Usuário não encontrado.")
    except ValueError as e:
        print((f'{red}Erro: {e}{fim}'))
   
    return None

# Função para cadastrar novos usuários
def cadastrar_usuario():
    try:
        tipo = input("Digite o tipo de usuário (ServidorDepae, ProfConselheiro, Avaliador): ")
        if tipo not in ["ServidorDepae", "ProfConselheiro", "Avaliador"]:
            raise ValueError((f'{red}Tipo de usuário inválido.{fim}'))
        
        
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")

        if tipo == "ServidorDepae":
            departamento = input("Digite o departamento: ")
            return ServidorDepae(nome, email, senha, departamento)
        elif tipo == "ProfConselheiro":
            conselho = input("Digite o conselho: ")
            return ProfConselheiro(nome, email, senha, conselho)
        elif tipo == "Avaliador":
            area_atuacao = input("Digite a área de atuação: ")
            return Avaliador(nome, email, senha, area_atuacao)

    except ValueError as e:
        print((f'{red}Erro: {e}{fim}'))
    
    return None

# Função principal
def main():
    clear()
    usuarios = []  # Lista para armazenar os usuários
    estoque = None  # Estoque que será administrado pelo ServidorDepae

    while True:
        print("\nMenu:")
        print("1. Fazer login")
        print("2. Cadastrar novo usuário")
        print("3. Listar todos os usuários")
        print("4. Sair\n")
        try:
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                usuario = solicitar_login()
                if usuario:
                    if isinstance(usuario, ServidorDepae):

                        # Menu para o ServidorDepae
                        while True:
                            print("\nMenu ServidorDepae:")
                            print("1. Listar materiais do estoque")
                            print("2. Adicionar material ao estoque")
                            print("3. Remover material do estoque")
                            print("4. Sair")
                            opcao_servidor = input("Escolha uma opção: ")

                            if opcao_servidor == "1":
                                usuario.listar_materiais()
                            elif opcao_servidor == "2":
                                material = input("Digite o nome do material: ")
                                quantidade = int(input("Digite a quantidade: "))
                                usuario.controlar_material(material, quantidade, adicionar=True)
                            elif opcao_servidor == "3":
                                material = input("Digite o nome do material: ")
                                quantidade = int(input("Digite a quantidade: "))
                                usuario.controlar_material(material, quantidade, adicionar=False)
                            elif opcao_servidor == "4":
                                break
                            else:
                                print((f'{red}Opção inválida.{fim}'))
                    
                    elif isinstance(usuario, ProfConselheiro):
                        # Menu para o ProfConselheiro
                        while True:
                            clear()
                            print("\nMenu ProfConselheiro:")
                            print("1. Cadastrar nova turma")
                            print("2. Adicionar material ao estoque via ServidorDepae")
                            print("3. Remover material do estoque via ServidorDepae")
                            print("4. Sair")
                            opcao_prof = input("Escolha uma opção: ")

                            if opcao_prof == "1":
                                nome_turma = input("Digite o nome da turma: ")
                                turma = usuario.cadastrar_turma(nome_turma)
                                print(f"Turma {turma.nome} cadastrada com sucesso.")
                            elif opcao_prof == "2":
                                material = input("Digite o nome do material: ")
                                try:
                                    quantidade = int(input("Digite a quantidade: "))
                                    if quantidade <= 0:
                                        raise ValueError("A quantidade deve ser positiva.")
                                    if estoque:
                                        usuario.gerenciar_estoque(estoque, material, quantidade, adicionar=True)
                                    else:
                                        raise ValueError("Estoque não está disponível. Verifique se o ServidorDepae está logado.")
                                
                                except ValueError as e:
                                    print((f'{red}Erro: {e}{fim}'))

                            elif opcao_prof == "3":
                                material = input("Digite o nome do material: ")
                                try:
                                    quantidade = int(input("Digite a quantidade: "))
                                    if quantidade <= 0:
                                        raise ValueError("A quantidade deve ser positiva.")
                                    if estoque:
                                        usuario.gerenciar_estoque(estoque, material, quantidade, adicionar=False)
                                    else:
                                        raise ValueError("Estoque não está disponível. Verifique se o ServidorDepae está logado.")
                                
                                except ValueError as e:
                                    print((f'{red}Erro: {e}{fim}'))

                            elif opcao_prof == "4":
                                break
                            else:
                                print("Opção inválida.")

                    elif isinstance(usuario, Avaliador):
                        # Menu para o Avaliador
                        while True:
                            clear()
                            print("\nMenu Avaliador:")
                            print("1. Lançar nota para uma turma")
                            print("2. Sair")
                            opcao_avaliador = input("Escolha uma opção: ")

                            if opcao_avaliador == "1":
                                try:
                                    turma_nome = input("Digite o nome da turma: ")
                                    valor = float(input("Digite a nota: "))
                                    if valor < 0 or valor > 10:
                                        raise ValueError("A nota deve estar entre 0 e 10.")
                                    turma = next((t for u in usuarios if isinstance(u, ProfConselheiro) for t in u.turmas if t.nome == turma_nome), None)
                                    if turma:
                                        usuario.lancar_nota(turma, valor)
                                        print(f"Nota {valor} lançada para a turma {turma.nome}.")
                                    else:
                                        raise ValueError("Turma não encontrada.")
                                    
                                except ValueError as e:
                                    print((f'{red}Erro: {e}{fim}'))

                            elif opcao_avaliador == "2":
                                break
                            else:
                                print("Opção inválida.")
            
            elif opcao == "2":
                usuario = cadastrar_usuario()
                if usuario:
                    usuarios.append(usuario)
                    if isinstance(usuario, ServidorDepae):
                        estoque = usuario.estoque  # Define o estoque se o usuário cadastrado for um ServidorDepae

            elif opcao == "3":
                Usuario.listar_usuarios()

            elif opcao == "4":
                break
            else:
                print((f'{red}Opção inválida, tente novamente.{fim}'))
        except Exception as e:
            print((f'{red}Erro inesperado: {e}{fim}'))


if __name__ == "__main__":
    main()
