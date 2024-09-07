import os 

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Linha para melhor Visualização
def linha(tam=50):
    return ('\033[1m-\033[m')*tam


# Criando o Cabeçalho do projeto
def cabecalho(texto):
    print(linha())
    print(f'\033[1m{texto.center(50)}\033[m')
    print(linha())


# Criando função para o menu
def menu(lista):
    c=1
    for item in lista:
        print(f'\033[1m{c} - {item}\033[m')
        c=c+1
    print(linha())


# Trata o erro de número inteiro
def verint(num):
    while True:
        try:
            n_int=(input(num))
            if n_int.isnumeric():
                break
        except:
            print('\033[31mErro: Opção Inválida. Digite novamente\033[m')
            continue
    return n_int
            

# Trata o erro de valor string 
def verstr(texto):
    while True:
        try:
            v_str=str(input(texto))
        except:
            print('\033[31mErro ao cadastrar as informções.\033[m')
            continue
        if v_str=='':
            continue
        else:
            return v_str.upper()


# Trata o erro de valor float 
def verfloat(txt):
    while True:
        try:
            v_float=float(input(txt))
        except:
            print('\033[31mErro ao cadastrar as informções.\033[m')
            continue
        else:
            return v_float