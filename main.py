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
        case "^":
            return "R"
        case "*" | "/" | "%" | "-" | "+":
            return "L"

def precedence(op):
    match op:
        case "^":
            return 4
        case "*" | "/" | "%":
            return 3
        case "-" | "+":
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
        if is_string:
            if token.startswith(":"):
                operators.append(token)
                continue
            output.append(token)

        match token:
            case "^" | "*" | "/" | "%" | "-" | "+":
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

def calculate(string: str, vars: dict) -> float | int:
    tokens = tokenizer(string)

    tokens = rpn(tokens)

    x = 0

    while True:
        print(tokens, x, tokens[x])

        if len(tokens) == 1:
            is_string = any(x in [":", "_", "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z"] for x in list(tokens[0]))

            if is_string:
                if tokens[0] in vars:
                    new = vars[tokens[0]] if type(vars[tokens[0]]) != str else float(vars[tokens[0]]) if "." in list(vars[tokens[0]]) else int(vars[tokens[0]])
                    tokens.pop()
                    tokens.append(new)

        match tokens[x]:
            case "^" | "*" | "/" | "%" | "-" | "+":
                op = tokens.pop(x)

                right = math.pi
                if type(tokens[x - 1]) != int and type(tokens[x - 1]) != float and tokens[x - 1] not in vars:
                    right = float(tokens.pop(x - 1)) if "." in list(tokens[x - 1]) else int(tokens.pop(x - 1))
                elif tokens[x - 1] in vars:
                    right = float(vars[tokens[x - 1]]) if "." in list(tokens[x - 1]) else int(vars[tokens[x - 1]])
                    tokens.pop(x - 1)
                else:
                    right = tokens.pop(x - 1)

                left = math.pi
                if type(tokens[x - 2]) != int and type(tokens[x - 2]) != float and tokens[x - 2] not in vars:
                    left = float(tokens.pop(x - 2)) if "." in list(tokens[x - 2]) else int(tokens.pop(x - 2))
                elif tokens[x - 2] in vars:
                    left = float(vars[tokens[x - 2]]) if "." in list(tokens[x - 2]) else int(vars[tokens[x - 2]])
                    tokens.pop(x - 2)
                else:
                    left = tokens.pop(x - 2)

                tokens.insert(x - 2, operate(left, right, op))
                
                x = 0
            case "=":
                tokens.pop(x)

                right = math.pi
                if type(tokens[x - 1]) != int and type(tokens[x - 1]) != float and tokens[x - 1] not in vars:
                    right = float(tokens.pop(x - 1)) if "." in list(tokens[x - 1]) else int(tokens.pop(x - 1))
                elif tokens[x - 1] in vars:
                    right = float(vars[tokens[x - 1]]) if "." in list(tokens[x - 1]) else int(vars[tokens[x - 1]])
                    tokens.pop(x - 1)
                else:
                    right = tokens.pop(x - 1)
                left = tokens.pop(x - 2)

                vars[left] = right

                tokens.append(vars[left])

                x = 0
            case ":MEM":
                tokens.pop()
                tokens.append(vars)
            case ":SUM":
                tokens.pop(x)

                right = math.pi
                if type(tokens[x - 1]) != int and type(tokens[x - 1]) != float and tokens[x - 1] not in vars:
                    right = float(tokens.pop(x - 1)) if "." in list(tokens[x - 1]) else int(tokens.pop(x - 1))
                elif tokens[x - 1] in vars:
                    right = float(vars[tokens[x - 1]]) if "." in list(tokens[x - 1]) else int(vars[tokens[x - 1]])
                    tokens.pop(x - 1)
                else:
                    right = tokens.pop(x - 1)

                left = math.pi
                if type(tokens[x - 2]) != int and type(tokens[x - 2]) != float and tokens[x - 2] not in vars:
                    left = float(tokens.pop(x - 2)) if "." in list(tokens[x - 2]) else int(tokens.pop(x - 2))
                elif tokens[x - 2] in vars:
                    left = float(vars[tokens[x - 2]]) if "." in list(tokens[x - 2]) else int(vars[tokens[x - 2]])
                    tokens.pop(x - 2)
                else:
                    left = tokens.pop(x - 2)

                tokens.insert(x - 2, operate(left, right, "+"))

        x += 1
        if x > len(tokens) - 1:
            x = 0

        if len(tokens) == 1:
            break

    x = 0

    if len(tokens) == 1:
        return tokens[0], vars

    return calculate(calculate(" ".join(tokens[0]), vars))

def main():
    vars = {}

    while True:
        inp = input("calc 2000 > ")

        res, vars = calculate(inp, vars)

        print(res)

if __name__ == "__main__":
    main()