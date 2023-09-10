import math

def tokenizer(string: str) -> list[str]:
    tokens = []

    val = ""

    for key, x in enumerate(list(string)):
        match x:
            case " ":
                if val != "":
                    tokens.append(val)
                val = ""
            case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" | ".":
                val += x
            case "-" | "+" | "*" | "/" | "%" | "^" | "(" | ")":
                if val != "":
                    tokens.append(val)
                val = ""
                if x == "-" and len(list(string)) > key + 1 and list(string)[key + 1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "π"]:
                    val = "-"
                else:
                    tokens.append(x)
            case "π":
                tokens.append(x)
            case ":" | "_" | "A" | "a" | "B" | "b" | "C" | "c" | "D" | "d" | "E" | "e" | "F" | "f" | "G" | "g" | "H" | "h" | "I" | "i" | "J" | "j" | "K" | "k" | "L" | "l" | "M" | "m" | "N" | "n" | "O" | "o" | "P" | "p" | "Q" | "q" | "R" | "r" | "S" | "s" | "T" | "t" | "U" | "u" | "V" | "v" | "W" | "w" | "X" | "x" | "Y" | "y" | "Z" | "z":
                val += x
            case "=":
                tokens.append("=")

    tokens.append(val)

    return tokens

def associative(op):
    match op:
        case "^" | ":POW":
            return "R"
        case "*" | "/" | "%" | "-" | "+" | ":MULTI" | ":DIV" | ":MOD" | ":SUB" | ":SUM":
            return "L"

def precedence(op):
    match op:
        case "^" | ":POW":
            return 4
        case "*" | "/" | "%" | ":MULTI" | ":DIV" | ":MOD":
            return 3
        case "-" | "+" | ":SUB" | ":SUM":
            return 2
    return 1

def rpn(tokens: list[str]) -> list[str]:
    output = []
    operators = []

    for token in tokens:
        is_number = any(x in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."] for x in list(token))
        is_string = any(x in [":", "_", "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z"] for x in list(token))
        
        if is_number:
            output.append(token)
        if is_string and (not token.startswith(":") or token in [":MEM", ":DEL", ":DEFINE"]):
            output.append(token)
        if is_string and token in [":RUN"]:
            operators.append(token)

        match token:
            case "^" | "*" | "/" | "%" | "-" | "+" | ":POW" | ":MULTI" | ":DIV" | ":MOD" | ":SUB" | ":SUM":
                if len(operators) > 0 and operators[-1] != "("and (precedence(token) < precedence(operators[-1]) or (precedence(token) == precedence(operators[-1]) and associative(token) == "L")):
                    output.append(operators.pop())
                operators.append(token)
            case "(":
                operators.append(token)
            case ")":
                if len(operators) != 0 and operators[-1] != "(":
                    output.append(operators.pop())
                if len(operators) != 0 and operators[-1] == "(":
                    operators.pop()
            case "π":
                output.append(token)
            case "=":
                operators.append(token)

    for op in reversed(operators):
        output.append(op)
    
    return output

def operate(left: int | float, right: int | float, op: str) -> int | float:
    match op:
        case "^":
            return left ** right
        case "*":
            return left * right
        case "/":
            return left / right
        case "%":
            return left % right
        case "-":
            return left - right
        case "+":
            return left + right

def parse(token: str | float | int, mem: dict) -> float | int:
    if token in mem and type(mem[token]) == list:
        tokens = list(reversed(mem[token]))
        result, mem = calculate("", mem, tokens)
        return result
    elif type(token) != int and type(token) != float and token not in mem:
        return float(token) if "." in list(token) else int(token)
    elif token in mem:
        return mem[token]
    else:
        return token

def parse_command(token: str) -> str:
    match token:
        case ":SUM":
            return "+"
        case ":SUB":
            return "-"
        case ":MULTI":
            return "*"
        case ":DIV":
            return "/"
        case ":MOD":
            return "%"
        case ":POW":
            return "^"
        case _:
            return "+"

def calculate(string: str, mem: dict, tokens: list = []) -> tuple[float | int, dict]:
    if tokens == []:
        tokens = tokenizer(string)

        tokens = rpn(tokens)

    x = 0

    while True:
        print(tokens, x)

        if len(tokens) == 1:
            is_string = any(x in [":", "_", "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z"] for x in list(tokens[0]))

            if is_string:
                if tokens[0] in mem:
                    new = parse(tokens[0], mem)
                    tokens.pop()
                    tokens.append(new)

        if tokens == []:
            tokens = [0]

        match tokens[x]:
            case "^" | "*" | "/" | "%" | "-" | "+":
                op = tokens.pop(x)

                right = parse(tokens.pop(x - 1), mem)

                left = parse(tokens.pop(x - 2), mem)

                tokens.insert(x - 2, operate(left, right, op))
                
                x = 0
            case "=":
                tokens.pop(x)

                right = parse(tokens.pop(x - 1), mem)

                left = tokens.pop(x - 2)

                mem[left] = right

                tokens.append(mem[left])

                x = 0
            case ":MEM":
                tokens.pop()
                tokens.append(mem)
            case ":DEL":
                mem.pop(tokens.pop(), None)
                tokens.pop()
            case ":DEFINE":
                tokens.pop(x)
                temp = []
                while len(tokens) >= 2:
                    temp.append(tokens.pop())
                mem[tokens.pop()] = temp
            case ":RUN":
                tokens.pop(x)

                right = parse(tokens.pop(x - 1), mem)

                left = parse(tokens.pop(x - 2), mem)

                mem["x"] = left
                mem["y"] = right

                tokens.append(parse(tokens.pop(), mem))

                x = 0
            case _:
                if type(tokens[x]) == str and tokens[x].startswith(":"):
                    token = tokens.pop(x)

                    right = parse(tokens.pop(x - 1), mem)

                    left = parse(tokens.pop(x - 2), mem)

                    tokens.insert(x - 2 if x - 2 >= 0 else x + 2, operate(left, right, parse_command(token)))

                    x = 0

        x += 1
        if x > len(tokens) - 1:
            x = 0

        if len(tokens) == 1:
            break

    x = 0

    if len(tokens) == 1:
        return tokens[0], mem
    
    mem.pop("x")
    mem.pop("y")

    return calculate(" ".join(tokens[0]), mem)

def main():
    mem = {}

    while True:
        inp = input("calc 2000 > ")

        res, mem = calculate(inp, mem)

        print(res)

if __name__ == "__main__":
    main()