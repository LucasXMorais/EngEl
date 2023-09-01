nome = str(input("Nome = "))
senha = str(input("Senha = "))
while nome == senha:
    print("Erro!!! A senha escolhida não pode ser igual ao nome")
    senha = str(input("Senha = "))
print("Seu nome foi escolhido com sucesso")
print("Obrigado por escolher Aliexpress ", nome)
