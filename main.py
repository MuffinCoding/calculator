import math

def is_number(token: str) -> bool:
    return any(x in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."] for x in list(token))

def is_string(token: str) -> bool:
    return any(x in ["\"", " ", ":", "_", "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z"] for x in list(token))

def tokenizer(string: str) -> list[str]:
    tokens = []

    val = ""

    in_string = False

    for point in range(len(string)):
        match string[point]:
            case " ":
                if in_string:
                    val += " "
                else:
                    if val != "":
                        tokens.append(val)
                    val = ""
            case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" | ".":
                val += string[point]
            case "-" | "+" | "*" | "/" | "%" | "^" | "(" | ")":
                if val != "":
                    tokens.append(val)
                val = ""
                if string[point] == "-" and len(list(string)) > point + 1 and list(string)[point + 1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "π"]:
                    val = "-"
                else:
                    tokens.append(string[point])
            case "π":
                tokens.append(string[point])
            case ":" | "_" | "A" | "a" | "B" | "b" | "C" | "c" | "D" | "d" | "E" | "e" | "F" | "f" | "G" | "g" | "H" | "h" | "I" | "i" | "J" | "j" | "K" | "k" | "L" | "l" | "M" | "m" | "N" | "n" | "O" | "o" | "P" | "p" | "Q" | "q" | "R" | "r" | "S" | "s" | "T" | "t" | "U" | "u" | "V" | "v" | "W" | "w" | "X" | "x" | "Y" | "y" | "Z" | "z":
                val += string[point]
            case "=":
                tokens.append("=")
            case "\"":
                in_string = not in_string
                val += "\""
            case "\\":
                if len(list(string)) > point + 1 and list(string)[point + 1] == "\"":
                    in_string = not in_string
                val += "\\"

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
        case "^" | "POW":
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
        if is_string(token) and (not token.startswith(":") or token in [":MEM", ":DEL", ":DEFINE"]):
            output.append(token)
        if is_number(token) and not is_string(token):
            output.append(token)
        if is_string(token) and token in [":RUN", ":AT", ":LEN"]:
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
            case "π" | ":PI":
                output.append(float(math.pi))
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

def parse(token: str | float | int, mem: dict, temp_mem: dict, main_use: bool = True, replace: bool = True) -> tuple[float | int, dict, dict]:
    temp = token, mem, temp_mem

    if main_use:
        if token in mem and type(mem[token]) == list:
            temp = calculate("", mem, temp_mem, list(reversed(mem[token])), False)
        elif token not in mem and type(token) == str and is_string(token):
            temp = token[1:-1], mem, temp_mem
        elif token in mem and type(mem[token]) == str and is_string(mem[token]):
            temp = mem[token], mem, temp_mem
        elif type(token) != int and type(token) != float and token not in mem and is_number(token):
            temp = float(token) if "." in list(token) else int(token), mem, temp_mem
        elif token in mem and type(mem[token]) == str:
            temp = float(mem[token]) if "." in list(mem[token]) else int(mem[token]), mem, temp_mem
        elif token in mem and type(mem[token]) != str and replace:
            temp = mem[token], mem, temp_mem
    else:
        if token in temp_mem and type(temp_mem[token]) == list:
            temp = calculate("", mem, temp_mem, list(reversed(mem[token])))
        elif token not in temp_mem and type(token) == str and is_string(token):
            temp = token[1:-1], mem, temp_mem
        elif token in temp_mem and type(temp_mem[token]) == str and is_string(temp_mem[token]):
            temp = temp_mem[token], mem, temp_mem
        elif type(token) != int and type(token) != float and token not in temp_mem and is_number(token):
            temp = float(token) if "." in list(token) else int(token), mem, temp_mem
        elif token in temp_mem and type(temp_mem[token]) == str:
            temp = float(temp_mem[token]) if "." in list(temp_mem[token]) else int(temp_mem[token]), mem, temp_mem
        elif token in temp_mem and type(temp_mem[token]) != str and replace:
            temp = temp_mem[token], mem, temp_mem

    return temp

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

def calculate(string_to_parse: str, mem: dict, temp_mem: dict, tokens: list = [], main_use: bool = True) -> tuple[float | int, dict, dict]:
    if tokens == []:
        tokens = tokenizer(string_to_parse)

        tokens = rpn(tokens)

    x = 0

    while True:
        # print("MEM START: ", tokens, x, mem, temp_mem, main_use)

        if tokens == []:
            tokens = [0]

        match tokens[x]:
            case "^" | "*" | "/" | "%" | "-" | "+":
                op = tokens.pop(x)

                right, mem, temp_mem = parse(tokens.pop(x - 1), mem, temp_mem, main_use=main_use)

                left, mem, temp_mem = parse(tokens.pop(x - 2), mem, temp_mem, main_use=main_use)

                tokens.insert(x - 2, operate(left, right, op))
                
                x = 0
            case "=":
                tokens.pop(x)

                right, mem, temp_mem = parse(tokens.pop(x - 1), mem, temp_mem, main_use=main_use, replace=False)

                left = tokens.pop(x - 2)

                mem[left] = right
                tokens.append(right)
                
                x = 0
            case ":MEM":
                tokens.pop()
                tokens.append(mem)
                
                x = 0
            case ":DEL":
                mem.pop(tokens.pop(), None)
                tokens.pop()
                
                x = 0
            case ":DEFINE":
                tokens.pop(x)
                temp = []
                while len(tokens) >= 2:
                    token = tokens.pop()

                    if main_use:
                        if is_string(token) and token not in mem:
                            if f"{tokens[0]}_meta" not in mem:
                                mem[f"{tokens[0]}_meta"] = []
                            mem[f"{tokens[0]}_meta"].append(token)
                    else:
                        if is_string(token) and token not in temp_mem:
                            if f"{tokens[0]}_meta" not in temp_mem:
                                mem[f"{tokens[0]}_meta"] = []
                            mem[f"{tokens[0]}_meta"].append(token)
                    temp.append(token)

                mem[tokens.pop()] = temp

                x = 0
            case ":RUN":
                tokens.pop(x)

                name = ""

                point_name = 0

                for token in tokens:
                    point_name += 1

                    if main_use:
                        if token in mem and f"{token}_meta" in mem:
                            name = token
                            break
                    else:
                        if token in temp_mem and f"{token}_meta" in temp_mem:
                            name = token
                            break

                point = 0

                for y in reversed(range(x)):
                    if y < point_name:
                        break

                    num, mem, temp_mem = parse(tokens.pop(y), mem, temp_mem, main_use=main_use)

                    temp_mem[mem[f"{name}_meta"][point]] = num

                    point += 1

                if len(tokens) == 1:
                    num, mem, temp_mem = parse(tokens.pop(0), mem, temp_mem, main_use=main_use, replace=False)

                    tokens.append(num)

                x = 0
            case ":AT":
                tokens.pop(x)

                point = int(tokens.pop(x - 1))

                token = mem[tokens.pop(x - 2)]

                if token[0] == "\"" and token[-1] == "\"":
                    tokens.insert(x - 2, token[1:-1][point])
                else:
                    tokens.insert(x - 2, token[point])

                x = 0
            case ":LEN":
                tokens.pop(x)

                val = tokens.pop(x - 1)

                if type(val) != str:
                    val = str(val)

                if val[0] == "\"" and val[-1] == "\"":
                    tokens.insert(x - 1, len(val[1:-1]))
                else:
                    tokens.insert(x - 1, len(val))
                    
                x = 0
            case _:
                if type(tokens[x]) == str and tokens[x].startswith(":"):
                    token = tokens.pop(x)

                    right, mem, temp_mem = parse(tokens.pop(x - 1), mem, temp_mem, main_use=main_use)

                    left, mem, temp_mem = parse(tokens.pop(x - 2), mem, temp_mem, main_use=main_use)

                    tokens.insert(x - 2 if x - 2 >= 0 else x + 2, operate(left, right, parse_command(token)))

                    x = 0

        if len(tokens) == 1:
            if main_use:
                if type(tokens[0]) == str and is_string(tokens[0]):
                    if tokens[0] in mem:
                        token = tokens.pop()
                        new, mem, temp_mem = parse(token, mem, temp_mem, main_use=main_use)
                        tokens.append(new)
            else:
                if type(tokens[0]) == str and is_string(tokens[0]):
                    if tokens[0] in temp_mem:
                        token = tokens.pop()
                        new, mem, temp_mem = parse(token, mem, temp_mem, main_use=main_use)
                        tokens.append(new)

        # print("MEM END:   ", tokens, x, mem, temp_mem, main_use)

        x += 1
        if x > len(tokens) - 1:
            x = 0

        if len(tokens) == 1:
            break

    x = 0

    if len(tokens) == 1:
        return tokens[0], mem, temp_mem

    return calculate(" ".join(tokens[0]), mem, temp_mem, main_use=main_use)

def main():
    mem = {}
    lines = []

    while True:
        inp = ""
        if lines == []:
            inp = input("calc 2000 > ")
        else:
            line = lines.pop(0).rstrip("\r\n")
            print(f"calc 2000 > {line}")
            inp = line

        if inp.startswith(":LOAD "):
            with open(inp[6:], "r", encoding="utf-8") as file:
                lines = file.readlines()

            continue

        res, mem, _ = calculate(inp, mem, {})

        print(res)

if __name__ == "__main__":
    main()
