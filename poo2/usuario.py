import hashlib

# Classe de exceção personalizada
class EstoqueInsuficienteException(Exception):
    def _init_(self, material, quantidade, mensagem="Estoque insuficiente"):
        self.material = material
        self.quantidade = quantidade
        super()._init_(mensagem)

# Função que gerencia o estoque e levanta exceções personalizadas
class Estoque:
    def _init_(self):
        self.materiais = {}

    def adicionar_material(self, material, quantidade):
        self.materiais[material] = self.materiais.get(material, 0) + quantidade

    def remover_material(self, material, quantidade):
        try:
            if material not in self.materiais or self.materiais[material] < quantidade:
                raise EstoqueInsuficienteException(material, quantidade)
            self.materiais[material] -= quantidade
        except EstoqueInsuficienteException as e:
            print(f"Erro: {e.mensagem} - Material: {e.material}, Quantidade solicitada: {e.quantidade}")
        finally:
            print("Operação de controle de estoque finalizada.")

# Testando a classe
estoque = Estoque()
estoque.adicionar_material("Caneta", 10)
estoque.remover_material("Caneta", 15)  # Gera uma exceção personalizada

# Classe base para todos os tipos de usuários do sistema
class Usuario:
    usuarios_cadastrados = []  # Lista que armazena todos os usuários cadastrados

    def __init__(self, nome, email, senha):
        # Inicializa um novo usuário com nome, email e uma senha criptografada
        self.nome = nome
        self.email = email
        self.senha_hash = self._gerar_hash(senha)
        Usuario.usuarios_cadastrados.append(self)  # Adiciona o usuário à lista de usuários cadastrados

    def _gerar_hash(self, senha):
        # Criptografa a senha usando SHA-256
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def validar_senha(self, senha):
        # Verifica se a senha fornecida corresponde ao hash armazenado
        return self.senha_hash == self._gerar_hash(senha)

    def login(self, email, senha):
        # Realiza o login verificando email e senha
        if self.email == email and self.validar_senha(senha):
            print(f"Login bem-sucedido para o usuário {self.nome}")
            return True
        else:
            print("Falha no login. Verifique suas credenciais.")
            return False

    @classmethod
    def buscar_usuario_por_email(cls, email):
        # Busca um usuário pelo email na lista de usuários cadastrados
        for usuario in cls.usuarios_cadastrados:
            if usuario.email == email:
                return usuario
        return None

    @classmethod
    def listar_usuarios(cls):
        # Exibe informações de todos os usuários cadastrados
        for usuario in cls.usuarios_cadastrados:
            print(usuario.info())

    def info(self):
        # Retorna uma string com informações do usuário
        return f"Usuário: {self.nome}, Email: {self.email}"

# Classe que representa um avaliador, herda de Usuario
class Avaliador(Usuario):
    def __init__(self, nome, email, senha, area_atuacao):
        super().__init__(nome, email, senha)  # Chama o construtor da classe base
        self.area_atuacao = area_atuacao  # Define a área de atuação do avaliador

    def lancar_nota(self, turma, valor):
        # Lança uma nota para uma turma específica
        nota = Nota(turma, valor)
        turma.adicionar_nota(nota)  # Adiciona a nota à turma

    def info(self):
        # Retorna uma string com informações do avaliador
        return f"Avaliador: {self.nome}, Área de Atuação: {self.area_atuacao}"

# Classe que representa um servidor do DEPAE, herda de Usuario
class ServidorDepae(Usuario):
    def __init__(self, nome, email, senha, departamento):
        super().__init__(nome, email, senha)  # Chama o construtor da classe base
        self.departamento = departamento  # Define o departamento do servidor
        self.estoque = Estoque()  # Cria um estoque associado ao servidor

    def controlar_material(self, material, quantidade, adicionar=True):
        # Controla o estoque de materiais, adicionando ou removendo quantidades
        if adicionar:
            self.estoque.adicionar_material(material, quantidade)
        else:
            self.estoque.remover_material(material, quantidade)

    def listar_materiais(self):
        # Lista todos os materiais e suas quantidades no estoque
        self.estoque.listar_materiais()

    def info(self):
        # Retorna uma string com informações do servidor DEPAE
        return f"ServidorDepae: {self.nome}, Departamento: {self.departamento}"

# Classe que representa um professor conselheiro, herda de Usuario
class ProfConselheiro(Usuario):
    def __init__(self, nome, email, senha, conselho):
        super().__init__(nome, email, senha)  # Chama o construtor da classe base
        self.conselho = conselho  # Define o conselho do professor
        self.turmas = []  # Lista de turmas do professor
        self.estoque = Estoque() # Cria um estoque associado ao professor

    def cadastrar_turma(self, nome_turma):
        # Cadastra uma nova turma e a adiciona à lista de turmas
        turma = Turma(nome_turma)
        self.turmas.append(turma)
        return turma

    def adicionar_material(self, material, quantidade):
        
        self.estoque.adicionar_material(material, quantidade)
    
    def remover_material(self, material, quantidade):        

        self.estoque.listar_materiais()
            
    def info(self):
        # Retorna uma string com informações do professor conselheiro
        return f"ProfConselheiro: {self.nome}, Conselho: {self.conselho}"

# Classe para gerenciar o estoque de materiais
class Estoque:
    def __init__(self):
        self.materiais = {}  # Dicionário para armazenar materiais e suas quantidades

    def adicionar_material(self, material, quantidade):
        # Adiciona uma quantidade de material ao estoque
        if material in self.materiais:
            self.materiais[material] += quantidade
        else:
            self.materiais[material] = quantidade

    def remover_material(self, material, quantidade):
        # Remove uma quantidade de material do estoque, se disponível
        if material in self.materiais and self.materiais[material] >= quantidade:
            self.materiais[material] -= quantidade
            if self.materiais[material] == 0:
                del self.materiais[material]
        else:
            print("Material insuficiente ou inexistente no estoque.")

    def listar_materiais(self):
        # Lista todos os materiais e suas respectivas quantidades
        for material, quantidade in self.materiais.items():
            print(f"{material}: {quantidade}")

# Classe que representa uma turma
class Turma:
    def __init__(self, nome):
        self.nome = nome  # Nome da turma
        self.alunos = []  # Lista de alunos da turma
        self.notas = []  # Lista de notas atribuídas à turma

    def adicionar_aluno(self, aluno):
        # Adiciona um aluno à turma, se ele ainda não estiver nela
        if aluno not in self.alunos:
            self.alunos.append(aluno)

    def remover_aluno(self, aluno):
        # Remove um aluno da turma
        if aluno in self.alunos:
            self.alunos.remove(aluno)

    def adicionar_nota(self, nota):
        # Adiciona uma nota para a turma
        self.notas.append(nota)

# Classe que representa uma nota
class Nota:
    def __init__(self, turma, valor):
        self.turma = turma  # A turma associada à nota
        self.valor = valor  # O valor da nota

    def definir_nota(self, valor):
        # Define um novo valor para a nota
        self.valor = valor