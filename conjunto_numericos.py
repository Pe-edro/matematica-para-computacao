from ast import While
import math #carrega o modulo math para funções matemáticas
import re #carrega o modulo re para expressões regulares

def mdc(a, b):              #Função para calcular o máximo divisor comum (MDC) de dois números inteiros a e b usando o algoritmo de Euclides.
    while b:                #Enquanto b não for zero
        a, b = b, a % b     #A função retorna o valor absoluto de a, que é o MDC dos dois números.
    return abs(a)           #Retorna o MDC

def simplificar_fracao(num, den):                                    #Função para simplificar uma fração 
    if den == 0:                                                     #Garente que o denominador não seja zero, caso seja, levanta um erro.
        raise ValueError("O denominador não pode ser zero.")
    if den < 0:                    #Garente que sempre o denominador seja positivo mesmo se ele for negativo, inverte o sinal de numerador e denominador.
        num, den = -num, -den      
    g = mdc(num, den)   #chama a função mdc para encontrar o máximo divisor comum entre o numerador e o denominador.
    return num // g, den // g #Divide o numerador e o denominador pelo divisor comum, o operador // é usado para garantir que o resultado seja um número inteiro.

def classificar_numero(entrada):
    entrada_orig = entrada.strip()  #Remove espaços em branco nas pontas e padroniza numeros com virgulas para pontos decimais 
    s = entrada_orig.replace(" ", "").replace(",", ".")

    if not s:   #Verifica se a entrada está vazia, caso esteja, levanta um erro.
        raise ValueError("Entrada sem número, digite seu número")

    
    if re.match(r"^[vV√](\d+)$", s): #identifica se a entrada começa com "v", "V" ou "√" seguido de um número.
        match_raiz = re.match(r"^[vV√](\d+)$", s)
        val = int(match_raiz.group(1)) #pega apenas o numero dentro da raiz
        raiz_exata = math.isqrt(val) #calcula a parte inteira da raiz quadrada

        if raiz_exata * raiz_exata == val: #se o quadrado da raiz inteira for igual ao valor original, então a raiz é exata.
            num, den = raiz_exata, 1
            tipo = "raiz_exata"
        else:
            return { #se não for exata, retorna que o número é irracional.
                "entrada": entrada_orig,
                "pertence": "I, R",
                "observação": f"A raiz não é exata (√{val} ≈ {math.sqrt(val):.4f}...), portanto irracional."
            }
    #Indentifica se a entrada possui parênteses, indicando que é uma dízima pariódica       
    elif "(" in s and ")" in s:
        #Utiliza uma expressão regular para identificar o padrão de dízima periódica, que pode ter uma parte inteira, uma parte decimal não periódica e uma parte decimal periódica.
        match_dizima = re.match(r"^([+-]?\d+)(?:\.(\d*))?\s*\(\s*(\d+)\s*\)$", s)
        if match_dizima:
            inteiro = match_dizima.group(1)
            nao_periodico = match_dizima.group(2) or ""
            periodico = match_dizima.group(3)

            sinal = -1 if inteiro.startswith("-") else 1 #descobre se o número é positivo ou negativo
            inteiro_abs = inteiro.lstrip("-+") or "0" #remove o sinal para fazer o cálculo

            #monta a string para a regra matemática da fração geratriz
            str_antes = inteiro_abs + nao_periodico #Inclui tudo antes do período
            str_com = inteiro_abs + nao_periodico + periodico #Inclui tudo antes do período e o período

            val_antes = int(str_antes)
            val_com = int(str_com)

            #Cálculo do numerador: (tudo junto) menos (o que vem antes do período)
            num = (val_com - val_antes) * sinal
            den = int("9" * len(periodico) + "0" * len(nao_periodico)) #Cálculo do denominador: 9's para cada dígito do período e 0's para cada dígito não periódico
            num, den = simplificar_fracao(num, den)

            if nao_periodico: #Define se a dizima é composta ou simples, dependendo se há dígitos não periódicos.
                tipo = "dizima_composta"
            else:
                tipo = "dizima_simples"
        else:
            raise ValueError("Formato de dízima periódica inválido.")

    #Define se é uma fração comum pelo caractere "/"    
    elif "/" in s:
        partes = s.split("/")
        if len(partes) != 2:
            raise ValueError("Formato de fração inválido.")
        num, den = int(partes[0]), int(partes[1])
        num, den = simplificar_fracao(num, den) #Reduz a fração ao menor termo
        tipo = "fracao"

    #Idenntifica se é um número decimal exato
    elif "." in s:
        partes = s.split(".")
        casas = len(partes[1]) #Conta quantas casas decimais existem após o ponto
        den = 10 ** casas #Cria o denominador correspondente
        num = int(s.replace(".", ""))  #remove o ponto para poder virar denominador
        num, den = simplificar_fracao(num, den)
        tipo = "decimal_exato"

    #Se não for nenhum dos casos acima, considera que é um número inteiro
    else:
        num = int(s)
        den = 1
        tipo = "inteiro"

    #se o denominador for 1, então o número é um inteiro e pertence a N, Z, Q e R (dependendo se é positivo ou negativo)
    if den == 1:
        if num >= 0:
            pertence = ["N", "Z", "Q", "R"] #positivos
        else:
            pertence = ["Z", "Q", "R"] #negativos
            
        if tipo == "raiz_exata":
            obs = f"A raiz é exata e vale {num}."
        elif tipo.startswith("dizima"):
            obs = f"A fração geratriz simplifica para o inteiro {num}."
        elif tipo == "fracao":
            obs = f"A fração simplifica para o inteiro {num}."
        elif num == 0:
            obs = "O número é zero."
        else:
            obs = f"O número é um inteiro -> {num}."

    #Se o denominar for maior que 1, o número é fracionário/decimal puro
    else:
        pertence = ["Q", "R"]
        #Define as observações para números que permanecem em formato de fração
        if tipo == "fracao":
            obs = f"Fração equivalente ao decimal {num/den}."
        elif tipo == "decimal_exato":
            obs = f"Decimal exato equivalente a {num}/{den}."
        elif tipo == "dizima_composta":
            obs = f"Dízima periódica composta, fração geratriz {num}/{den}."
        elif tipo == "dizima_simples":
            obs = f"Dízima periódica simples, fração geratriz {num}/{den}."
        else:
            obs = f"Fração racional {num}/{den}."
    #Retorna o dicionario com o relatório completo formatado
    return {
        "entrada": entrada_orig,
        "pertence": ", ".join(pertence),
        "observação": obs
    }

#Crivo de Eratóstenes
def  crivo(n):
    if n < 2: #Se n for menor que 2, não há números primos, então retorna uma lista vazia.
        return []
    primos = [True] * (n + 1) #Cria uma lista grande com true, o indice da lista representa o número. No começo assume que todos são primos. 
    primos[0] = primos[1] = False #Definição manual que 0 e 1 não são primos.
    for i in range(2, int(n**0.5) + 1): #Laço de repetição que vai ate a raiz quadrada de n, matematicamente nenhum fator composto restará após esse point.
        if primos[i]:
            for j in range(i*i, n + 1, i): #Laço de repetição que marca todos os múltiplos de i como não primos, começando do quadrado de i.
                primos[j] = False
    return [i for i, is_primo in enumerate(primos) if is_primo] #Retorna uma lista de números primos, filtrando os índices da lista original que ainda são True.

def listar_divisores(n):
    n = abs(n) #Tranforma o número em positivo.
    if n == 0: #Se o número for zero, não há divisores definidos, então retorna uma lista vazia.
        return []
    divisores = set() #Ultiliza comando set para garantir que não haja divisores repetidos.
    for i in range(1, int(math.sqrt(n)) + 1): #Laço de repetição que vai de 1 até a raiz quadrada de n, para encontrar divisores.
        if n % i == 0: #Se o resto da divisão for 0, encontamos um divisor.
            divisores.add(i) #Adiciona o divisor menor 
            divisores.add(n // i) #Adiciona o divisor maior correspondente
    return sorted(list(divisores)) #Retorna a lista de divisores ordenada.

def menu():
    while True: #Cria um laço de repetição infinito para o menu, permitindo que o usuário faça várias operações até escolher sair.
        print("Menu de opções:")
        print("1. Classificar número")
        print("2. Listar divisores")
        print("3. Listar primos até n")
        print("4. Sair")

        opcao = input("Escolha uma opção (1-4): ").strip() #Capturaa opção do usuario e remove espaços extras.

        if opcao == "1":
            entrada = input("Digite o número a ser classificado: ")
            try: #Chama a função de classificaçãoe exibe os dados do relatorio retornado.
                resultado = classificar_numero(entrada)
                print(f"Entrada: {resultado['entrada']}")
                print(f"Pertence a: {resultado['pertence']}")
                print(f"Observação: {resultado['observação']}")
            except ValueError as e: #captura erros de validação da própia função
                print(f"Erro: {e}")
    
        elif opcao == "2":
            try:
                n = int(input("Digite o número para listar divisores: "))
                divisores = listar_divisores(n)
                #Converte os números da lista em texto e os junta separados por vírgula. 
                print(f"Divisores de {n}: {', '.join(map(str, divisores))}")
            except ValueError:
                #Captua erro se o usuário digitar algo que não seja um número inteiro.
                print("Erro: Por favor, digite um número inteiro válido.")
    
        elif opcao == "3":
            try:
                val = int(input("\nDigite o valor limite n para calcular os primos: "))
                primos = crivo(val)
                #Exibe os números Primos encontrados e avisa caso não haja nenhum número primo (Ex: 1).
                print(f"\nPrimos até {val}: {', '.join(map(str, primos)) if primos else 'Nenhum'}")
            except ValueError:
                print("\n[ERRO] Por favor, digite um número inteiro válido.")
    
        elif opcao == "4":
            #exibe que estamos saindo do programa e encerra o laço de repetição.
            print("Saindo...")
            return
        else:
            #Exibe mensagem de erro caso o usuário digite uma opção inválida.
            print("Opção inválida. Por favor, escolha uma opção válida.")

#garante que o menu só será inicializado se o arquivo for executado diretamente.
if __name__ == "__main__":
    menu()