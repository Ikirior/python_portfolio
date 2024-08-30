import textwrap

def menu():
    menu = """\n
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc] \tNova conta
    [lc] \tListar contas
    [nu] \tNovo usuario
    [q] \tSair
    =>"""
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios, cpf):
    nome = input("\nInsira seu nome: ")
    data_nascimento = input("Insira sua data de nascimento (DIA/MES/ANO): ")
    
    print("\nEndereço:")
    logradouro = input("Rua: ")
    numero = input("Numero: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    
    usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    return usuarios, usuario

def filtrar_usuario(cpf, usuarios):
    
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuarios, usuario
    
    return criar_usuario(usuarios, cpf)

def criar_conta_corrente(usuario, contas):
    agencia = "0001"
    numero_conta = str(len(contas) + 1)
    conta_corrente = {"agencia": agencia, "numero_conta": numero_conta, "usuario":usuario, "saldo": 0, "extrato": ""}
    contas.append(conta_corrente)
    return contas, conta_corrente

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")

def depositar(valor, conta_corrente):
    if valor > 0:
        conta_corrente["saldo"] += valor
        conta_corrente["extrato"] += f"Depósito: R$: {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} efetuado com sucesso.")
    else:
        print("Operação inválida, tente novamente.")
    
    return conta_corrente
    
def sacar(valor, conta_corrente, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Limite de saques diários atingido.")
    elif valor > limite:
        print("Valor do saque excede o limite permitido.")
    elif valor > conta_corrente["saldo"]:
        print("Saldo insuficiente.")
    else:
        conta_corrente["saldo"] -= valor
        conta_corrente["extrato"] += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} efetuado com sucesso.")
    
    return conta_corrente, numero_saques
    
def criar_extrato(conta_corrente):
        print("Não foram feitas movimentações na conta." if not conta_corrente["extrato"] else conta_corrente["extrato"])
        print(f"\n\n Saldo da conta: R$ {conta_corrente["saldo"]:.2f}")       

def filtrar_contas_por_usuario(usuario, contas):
    contas_usuario = [conta for conta in contas if conta['usuario'] == usuario]
    return contas_usuario

def main():
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    
    usuarios = []
    contas = []
    
    # Login
    print("\nBem vindo(a) ao sistema bancário. Por favor, realize o login.")
    cpf = int(''.join(filter(str.isdigit, input("Insira o seu CPF (numeros): "))))
    
    usuarios, usuario = filtrar_usuario(cpf, usuarios)
    
    contas_usuario = filtrar_contas_por_usuario(usuario, contas)
    
    if contas_usuario:
        conta_corrente = contas_usuario[0]
        print(f"Usuário já possui conta. Conta ativa: {conta_corrente['numero_conta']}")
    else:
        contas, conta_corrente = criar_conta_corrente(usuario, contas)
        print(f"Conta criada com sucesso. Agência: {conta_corrente['agencia']} | Conta: {conta_corrente['numero_conta']}")
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            valor = float(input("\nInsira o valor a ser depositado: "))
            conta_corrente = depositar(valor=valor, conta_corrente=conta_corrente)
        
        elif opcao == "s":
            valor = float(input("\nInsira o valor a ser sacado: "))
            conta_corrente, numero_saques = sacar(valor=valor, conta_corrente=conta_corrente, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        
        elif opcao == "e":
            criar_extrato(conta_corrente=conta_corrente)
        
        elif opcao == "nc":
            contas, conta_corrente = criar_conta_corrente(usuario=usuario, contas=contas)
            print(f"Conta criada com sucesso. Agencia: {conta_corrente['agencia']} | Conta: {conta_corrente['numero_conta']}")
        
        elif opcao == "lc":
            listar_contas(contas=contas)
        
        elif opcao == "nu":
            cpf_novo = int(''.join(filter(str.isdigit, input("Insira o novo CPF (numeros): "))))
            usuarios, usuario = filtrar_usuario(cpf=cpf_novo, usuarios=usuarios)
            print(f"Novo usuário criado com sucesso. Agora é {usuario['nome']}")
        elif opcao == "q":
            break
        
        else:
            print("Insira uma opção válida.")

if __name__ == "__main__":
    


    main()