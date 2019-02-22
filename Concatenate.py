input_list = ["A", "B", "B", "A", "C", "C", "C", "C", "C", "C"]
output_list = []
i = 0

input_list.append("")

while i < len(input_list):
    temp = ""
    current_letter = input_list[i]
    if current_letter == "":
        break
    for j in range(i, len(input_list)):
        if input_list[j] == current_letter:
            temp += input_list[j]
        else:
            upto = j
            break
    output_list.append(temp)
    i = upto-1
    i += 1
print(output_list)
