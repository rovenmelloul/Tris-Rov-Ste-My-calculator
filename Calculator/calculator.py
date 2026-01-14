class Calculator():

    def init(self):
        print("Initialize")
        pass

    def parser_expresion(self,str:str)->list:
            tokens = []
            num = ""
            for i in str:
                if i in "+-*/":
                    tokens.append(int(num))
                    tokens.append(i)
                    num = ""
                else:
                    num += i
            tokens.append(int(num))
            return tokens
        
    def start_solving(self, list_elements: list):
        i = 0
        while i < len(list_elements) - 1:
            if list_elements[i] in ("*", "/"):
                left = list_elements[i - 1]
                right = list_elements[i + 1]
                
                if list_elements[i] == "*":
                    print("we find *")
                    result = left * right
                else:  # "/"
                    result = left / right
                
                list_elements[i - 1] = result
                del list_elements[i:i + 2]  
                print("After operation:", list_elements)
            else:
                i += 1

        # Phase 2: Now handle + and - (lower precedence)
        i = 0
        while i < len(list_elements) - 1:
            if list_elements[i] in ("+", "-"):
                left = list_elements[i - 1]
                right = list_elements[i + 1]
                
                if list_elements[i] == "+":
                    result = left + right
                else:  # "-"
                    result = left - right
                
                list_elements[i - 1] = result
                del list_elements[i:i + 2]  # remove operator and right operand
                
                # Do NOT increment i — same reason as above
                print("After operation:", list_elements)
            else:
                i += 1

        return list_elements
    
    def add():
        pass
    
    def add():
        pass

    def add():
        pass

    def save_to_log():
        pass


c = Calculator()
print(c.start_solving(c.parser_expresion("23+4+12*2")))