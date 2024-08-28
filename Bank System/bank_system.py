menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    
    opcao = input(menu)
    
    if opcao == "d":
        print("\nDepósito")
        
        deposito = float(input("\nInsira o valor a ser depositado: "))
        
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
            
        else:
            print("Operação inválida, tente novamente.")
    
    elif opcao == "s":
        print("\nSaque")
        
        while numero_saques < LIMITE_SAQUES:
            
            print(f"\nQuantidade de saques efetuados: {numero_saques}\n")
            saque = float(input("Insira quanto deseja sacar [0] para sair:"))
            
            if (saque <= limite):
                
                if (saque <= saldo):
                    saldo -= saque
                    numero_saques += 1
                    
                    if saque == 0:
                        break
                    
                    extrato += f"Saque: R$ {saque:.2f}\n"
                
                else:
                    print("\nNão é possível sacar o dinheiro por falta de saldo, tente novamente.")

                    
            else:
                print("\nValor limite de saque Alcançado, tente outro valor:")

    elif opcao == "e":
        print("\nExtrato")
        print("Não foram feitas movimentações na conta." if not extrato else extrato)
        print(f"\n\n Saldo da conta: R$ {saldo:.2f}")
    
    elif opcao == "q":
        break
    
    else:
        print("Insira uma opção válida.")