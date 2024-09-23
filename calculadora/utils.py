import re
# O simbolo circunflexo significa "começa com". O símbolo de cifrão significa "termina com".
# A lista 0-9 significa que você quer encontrar tal número até tal número numa cadeia de caracteres. Neste caso, a /
# variável quer encontrar a primeira vez que um número (ou o ponto) aparecer nessa cadeia.
NUM_OR_DOT_REGEX = re.compile(f'^[0-9.]$')

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid

def isEmpty(string: str):
    return string == ''