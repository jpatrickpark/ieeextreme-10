from math import log, floor
if __name__ == "__main__":
    line1, line2, line3, line4, line5 = input(), input(), input(), input(), input()
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    base, symbols = line1.split()
    base = int(base)
    value_to_symbol = {}
    symbol_to_value = {}
    for i in range(base):
        value_to_symbol[i] = symbols[i]
        symbol_to_value[symbols[i]] = i
    first = line2.strip()
    second = line3[1:].strip()
    
    first_reversed = first[::-1]
    second_reversed = second[::-1]
    carry = 0
    result = ""
    for i in range(min(len(first),len(second))):
        current_added_value = symbol_to_value[first_reversed[i]]+symbol_to_value[second_reversed[i]]+carry
        if current_added_value >= base:
            carry = 1
            current_added_value -= base
        else:
            carry = 0
        result += value_to_symbol[current_added_value]
    if (len(first)-len(second)) == 0:
        if carry:
            result += value_to_symbol[1]
    else:
        if len(first)>len(second):
            longer_element = first_reversed
            longer_length = len(first)
        else:
            longer_element = second_reversed
            longer_length = len(second)
        difference = abs(len(first)-len(second))
        for i in range(longer_length-difference,longer_length,1):
            current_added_value = symbol_to_value[longer_element[i]]+carry
            if current_added_value >= base:
                carry = 1
                current_added_value -= base
            else:
                carry = 0
            result += value_to_symbol[current_added_value]
        if carry:
            result += value_to_symbol[1]
        
            
    
    print(" "*(len(line5) - len(result)) + result[::-1])
