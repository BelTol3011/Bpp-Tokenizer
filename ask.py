def ask(possibilities=["Y", "N"]):
    for i in range(0, len(possibilities)):
        possibilities[i] = possibilities[i].upper()
    while True:
        for p in possibilities:
            print(p+" ", end="")
        inp = input("\n-->")
        if inp.upper() in possibilities:
            return inp.upper()
        print("Eingabe ungültig!")

if __name__ == "__main__":
    print(ask(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]))