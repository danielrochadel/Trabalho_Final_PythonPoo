from abc import ABC, abstractmethod


# =======================================================
# R4. INTERFACE (capacidade do pet, estilo slide 28 e 30)
# =======================================================
class Vacinavel(ABC):
    @abstractmethod
    def vacinar(self):
        pass



# =======================================================
# R1, R3 e R8. CLASSE ABSTRATA MÃE (molde principal)
# =======================================================
class Pet(ABC):
    def __init__(self, nome, peso, castrado = False):
        # R3: atributos protegidos
        # nome e peso passam pelos setters para ja validar na criacao
        self.set_nome(nome)
        self.set_peso(peso)
        self._vacinado = False
        self._castrado = castrado

    # Getters e Setters simples (estilo da aula)
    def get_nome(self):
        return self._nome

    def set_nome(self, novo_nome):
        # R3: validacao - nome nao pode ficar vazio
        if novo_nome.strip() == "":
            raise ValueError("o nome nao pode ficar vazio.")
        self._nome = novo_nome.strip()

    def get_peso(self):
        return self._peso

    def set_peso(self, novo_peso):
        # R3: validacao exigida no requisito
        # se o peso for zero ou negativo, o setter recusa e lanca um erro
        if novo_peso <= 0:
            raise ValueError("peso invalido! O peso precisa ser maior que zero.")
        self._peso = novo_peso

    def get_vacinado(self):
        return self._vacinado

    def get_castrado(self):
        return self._castrado

    def castrar(self):
        self._castrado = True

    # R1: metodo abstrato
    @abstractmethod
    def calcular_banho(self):
        pass

    # R1: metodo normal que usa o metodo abstrato
    def ficha(self):
        valor = self.calcular_banho()
        return f"{self._nome} ({self._peso}kg) -> Banho: R$ {valor:.2f}"

    # R8: representação em texto do objeto (slide 30)
    def __str__(self):
        status_vacina = "Sim" if self._vacinado else "Nao"
        status_castrado = "Sim" if self._castrado else "Nao"
        return f"Nome: {self._nome} | Peso: {self._peso}kg | Vacinado: {status_vacina} | Castrado: {status_castrado}"


# =======================================================
# R2 e R4. CLASSES FILHAS (herança com super e interface)
# =======================================================
class Cachorro(Pet, Vacinavel):
    def __init__(self, nome, peso, raca, castrado = False):
        # R2: chamando o construtor da mãe com super (slide 29)
        super().__init__(nome, peso, castrado)
        # R2 e R3: atributo próprio da classe filha
        self._raca = raca

    def get_raca(self):
        return self._raca

    # R2: implementando o metodo abstrato com regra própria
    # no cachorro o preco do banho depende do porte (peso)
    def calcular_banho(self):
        if self._peso <= 10:
            return 50.0   # porte pequeno
        elif self._peso <= 25:
            return 70.0   # porte medio
        return 90.0       # porte grande

    # R4: metodo da interface
    def vacinar(self):
        if self._vacinado:
            return f"{self._nome} ja estava vacinado."
        self._vacinado = True
        return f"{self._nome} tomou a vacina de cachorro!"

    # R8: sobrescrevendo __str__
    def __str__(self):
        return f"[Cachorro] {super().__str__()} | Raca: {self._raca}"


class Gato(Pet, Vacinavel):
    def __init__(self, nome, peso, pelagem, castrado = False):
        super().__init__(nome, peso, castrado)
        self._pelagem = pelagem

    def get_pelagem(self):
        return self._pelagem

    # R2: regra diferente para o gato
    # no gato o preco depende da pelagem (pelo longo da mais trabalho)
    def calcular_banho(self):
        if self._pelagem.lower() == "longa":
            return 70.0
        return 50.0

    # R4: metodo da interface
    def vacinar(self):
        if self._vacinado:
            return f"{self._nome} ja estava vacinado."
        self._vacinado = True
        return f"{self._nome} tomou a vacina de gato!"

    # R8: sobrescrevendo __str__
    def __str__(self):
        return f"[Gato] {super().__str__()} | Pelagem: {self._pelagem}"


# =======================================================
# R6. LISTA COM 5 OBJETOS INICIAIS (o minimo pedido e 3)
# =======================================================
lista_pets = [
    Cachorro("Bob", 18.0, "Labrador", False),
    Cachorro("Caramelo", 7.5, "Vira lata", False),
    Gato("Marrie", 4.0, "Longa", True),
    Gato("Leléco", 3.8, "Longa", True),
    Gato("Frajola", 3.5, "Curta", True)
]


# Funções de apoio para o menu
def cadastrar():
    print("\n--- Cadastrar Pet ---")
    tipo = input("Digite 1 para Cachorro ou 2 para Gato: ")

    # confere o tipo antes de pedir o resto dos dados
    if tipo != "1" and tipo != "2":
        print("Tipo invalido!")
        return

    nome = input("Nome: ")

    # se a pessoa digitar letra no peso, o float() da erro
    # entao trato aqui para o programa nao fechar
    try:
        peso = float(input("Peso (kg): ").replace(",", "."))
    except ValueError:
        print("Erro: digite um numero para o peso. Cadastro cancelado.")
        return

    resp_castrado = input("E castrado? (s/n): ").lower()
    castrado = resp_castrado in ["s", "sim"]

    # R3: se o setter recusar (peso <= 0 ou nome vazio), ele lanca
    # ValueError e o except mostra a mensagem sem fechar o programa
    try:
        if tipo == "1":
            raca = input("Raca: ")
            novo = Cachorro(nome, peso, raca, castrado)
            lista_pets.append(novo)
            print("Cachorro cadastrado com sucesso!")
        else:
            pelagem = input("Pelagem (Curta/Longa): ")
            novo = Gato(nome, peso, pelagem, castrado)
            lista_pets.append(novo)
            print("Gato cadastrado com sucesso!")
    except ValueError as erro:
        print("Erro:", erro, "Cadastro cancelado.")


def listar():
    print("\n--- Lista de Pets ---")
    if len(lista_pets) == 0:
        print("Nenhum pet cadastrado.")
    else:
        for pet in lista_pets:
            print(pet)  # R8: chama o __str__ de cada um


def buscar():
    print("\n--- Buscar Pet ---")
    busca = input("Digite o nome do pet: ").lower()
    achou = False
    for pet in lista_pets:
        if pet.get_nome().lower() == busca:
            print("Encontrado:", pet)
            print("Ficha:", pet.ficha())
            achou = True
            break
    if not achou:
        print("Pet nao encontrado.")


def remover():
    print("\n--- Remover Pet ---")
    nome_remover = input("Digite o nome para remover: ").lower()
    achou = False
    for pet in lista_pets:
        if pet.get_nome().lower() == nome_remover:
            lista_pets.remove(pet)
            print("Pet removido com sucesso!")
            achou = True
            break
    if not achou:
        print("Pet nao encontrado.")


# R5. POLIMORFISMO: laço for chamando o mesmo metodo em todos
def acao_sistema():
    print("\n--- Acao do Sistema (Polimorfismo) ---")
    print("1 - Calcular banho de todos")
    print("2 - Vacinar todos os pets")
    op = input("Escolha: ")

    if op == "1":
        print("\nCalculando precos:")
        for pet in lista_pets:
            # Polimorfismo: cada objeto calcula o banho do seu jeito
            print(pet.ficha())
    elif op == "2":
        print("\nVacinando os pets:")
        for pet in lista_pets:
            # Polimorfismo: cachorro e gato respondem com mensagens diferentes
            print(pet.vacinar())
    else:
        print("Opcao invalida.")


# =======================================================
# R7. MENU PRINCIPAL (estilo slide 24)
# =======================================================
def menu():
    while True:
        print("\n=== MENU PET SHOP ===")
        print("1 Cadastrar")
        print("2 Listar")
        print("3 Buscar")
        print("4 Remover")
        print("5 Acao do sistema")
        print("0 Sair")

        opcao = input("Opcao: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            buscar()
        elif opcao == "4":
            remover()
        elif opcao == "5":
            acao_sistema()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opcao invalida! Tente novamente.")


# Inicia o programa
menu()
