import math 
import re

def mdc(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def simplificar_fracao(num, den):
    if den == 0:
        raise ValueError("O denominador não pode ser zero.")
    if den < 0:
        num, den = -num, -den 
    g = mdc(num, den)
    return num // g, den // g

def classificar_numero(entrada):
    entrada_orig = entrada.strip()
    s = entrada_orig.replace(" ", "").replace(",", ".")

    if not s:
        raise ValueError("Entrada sem número, digite seu número")

    match_raiz = re.match(r"^[vV√](\d+)$", s)
    if match_raiz:
        val = int(match_raiz.group(1))
        raiz_exata = math.isqrt(val)
        if raiz_exata * raiz_exata == val:
            num, den = raiz_exata, 1
            tipo = "raiz_exata"
        else:
            return{
                "entrada":entrada_orig,
                "pertence":["I", "R"],
                "observação": f"A raiz não é exata (√{val} ≈ {math.sqrt(val):.4f}...), portanto irracional."
            }
    elif "("in s and")" in s:
        match_dizima = re.match(r"^([+-]?\d+)(?:\.(\d*))?\s*\(\s*(\d+)\s*\)$", s)
        if match_dizima:
            inteiro = match_dizima.group(1)
            nao_periodico = match_dizima.group(2) or ""
            periodico = match_dizima.group(3)

            sinal = -1 if inteiro.startswith("-") else 1
            inteiro_abs = inteiro.lstrip("-+") or "0"

            str_antes = inteiro_abs + nao_periodico 
            str_com = inteiro_abs + nao_periodico + periodico

            val_antes = int(str_antes)
            val_com = int(str_com)

            num = (val_com - val_antes) * sinal
            den = int("9" * len(periodico) + "0" * len(nao_periodico))
            num, den = simplificar_fracao(num, den)

            if nao_periodico:
                tipo = f"dízima_composta (fração geratriz {num}/{den})"
            else:
                tipo = f"dízima_simples (fração geratriz {num}/{den})"
        else:
            raise ValueError("Formato de dízima periódica inválido.")

    elif "/"in s:
        partes = s.split("/")
        if len(partes) != 2:
            raise ValueError("Formato de fração inválido.")
        num, den = int(partes[0]), int(partes[1])
        num, den = simplificar_fracao(num, den)
        tipo  = "fracao"

    elif "." in s:
        partes = s.split(".")
        casas = len(partes[1])
        den = 10 ** casas
        num = int(s.replace(".", "")) 
        num, den = simplificar_fracao(num, den)
        tipo = "decimal_exato"

    else:
        num = int(s)
        den = 1
        tipo = "inteiro"

    if den == 1:
        if num >= 0:
            pertence = ["N", "Z", "Q", "R"]
        if tipo == "raiz_exata":
            obs = f"A raiz é exata e vale {num}."
        elif tipo.startswith("dizima"):
            obs = f"A geratriz é {num}."
        elif tipo == "fracao":
            obs = f"A fração simplifica para {num}."
        elif num == 0:
            obs = "O número é zero."
        else:
            obs = f"O número é um inteiro -> {num}."
    else:
        pertence = ["Q", "R"]
        if tipo == "fracao":
            obs = f"Fração equivalente ao decimal {num/den}."
        elif tipo == "decimal_exato":
            obs = f"Decimal exato equivalente a {num}/{den}."
        elif tipo.startswith("dizima_composta"):
            obs = f"Dízima periódica composta, geratriz {num}/{den}."
        elif tipo.startswith("dizima_simples"):
            obs = f"Dízima periódica, fração geratriz {num}/{den}."
        else:
            obs = f"Fração racional {num}/{den}."

    return {
        "entrada": entrada_orig,
        "pertence": ", ".join(pertence),
        "observação": obs
    }

def  crivo(n):
    if n < 2:
        return []
    primos = [True] * (n + 1)
    primos[0] = primos[1] = False
    for i in range(2, int(n**0.5) + 1):
        if primos[i]:
            for j in range(i*i, n + 1, i):
                primos[j] = False
    return [i for i, is_primo in enumerate(primos) if is_primo]

def listar_divisores(n):
    n = abs(n)
    if n == 0:
        return []
    divisores = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisores.add(i)
            divisores.add(n // i)
    return sorted(list(divisores))

def menu():
    print("Menu de opções:")
    print("1. Classificar número")
    print("2. Listar divisores")
    print("3. Listar primos até n")
    print("4. Sair")

    opcao = input("Escolha uma opção (1-4): ").strip()

    if opcao == "1":
        entrada = input("Digite o número a ser classificado: ")
        try:
            resultado = classificar_numero(entrada)
            print(f"Entrada: {resultado['entrada']}")
            print(f"Pertence a: {resultado['pertence']}")
            print(f"Observação: {resultado['observação']}")
        except ValueError as e:
            print(f"Erro: {e}")
    
    elif opcao == "2":
        try:
            n = int(input("Digite o número para listar divisores: "))
            divisores = listar_divisores(n)
            print(f"Divisores de {n}: {', '.join(map(str, divisores))}")
        except ValueError:
            print("Erro: Por favor, digite um número inteiro válido.")
    
    elif opcao == "3":
        try:
                val = int(input("\nDigite o valor limite n para calcular os primos: "))
                primos = crivo(val)
                print(f"\nPrimos até {val}: {', '.join(map(str, primos)) if primos else 'Nenhum'}")
        except ValueError:
                print("\n[ERRO] Por favor, digite um número inteiro válido.")
    
    elif opcao == "4":
            print("Saindo...")
            return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    menu()