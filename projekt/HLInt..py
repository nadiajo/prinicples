import re
import keyword

condition_skipper = False

declarations = {}
assignments = {}


def declaration_checker(line):
    test = line.split(":")
    
    if len(test) == 1:
        return False

    if test[1] == 'integer;':
        declarations[test[0]] = 'integer'
        return True
    
    elif test[1] == 'double;':
        declarations[test[0]] = 'double'
        return True
    
    else:
        return False
    
def assignment_checker(line):
    test = line.split(":=")

    if len(test) == 1:
        return False
    
    if test[1][-1] != ';':
        return False
    
    if not test[0] in declarations:
        return False
    
    try:
        if declarations[test[0]] == 'integer':
            assignments[test[0]] = int(test[1][0])
            return True

        elif declarations[test[0]] == 'double' and len(test[1]) <= 5 and test[1][1] == '.':
            assignments[test[0]] = float(test[1][:-1])
            return True
        
        else:
            return False
    
    except:
        return False

def value_extractor(str):
    if str in assignments:
        return assignments[str]
    
    elif '.' in str:
        if len(str) <= 4 and str[1] == '.':
            return float(str)
        else: 
            return None
    else:
        if len(str) == 1:
            return int(str)
        else:
            return None

def math_checker(line):
    test = line.split("=")
    
    if len(test) == 1:
        return False
    
    if test[1][-1] != ';':
        return False
    
    if not test[0] in declarations:
        return False
    
    if '+' in test[1]:
        values = test[1].split('+')
        first_value = value_extractor(values[0])
        second_value = value_extractor(values[1][:-1])

    elif '-' in test[1]:
        values = test[1].split('-')
        first_value = value_extractor(values[0])
        #simplify mathematical operation later on because a - b = a + (b * -1)
        second_value = value_extractor(values[1][:-1]) * -1

    else:
        return False
    
    if declarations[test[0]] == 'integer':
        if isinstance(first_value,int) and isinstance(second_value,int):
            assignments[test[0]] = first_value + second_value
            return True
        
        else:
            return False
    
    if declarations[test[0]] == 'double':
        if not first_value is None and not second_value is None:
            assignments[test[0]] = first_value + second_value
            return True
        
        else:
            return False
        

def output_checker(line):

    if line[-1] != ';':
        return False
    
    if line[:8] != 'output<<':
        return False
    
    elif line[8] == '"' and line[-2] == '"':
        if '"' in line[9:-2]:
            return False
        
        else:
            print(line[9:-2])
            return True
    else:
        line = line[8:-1]

        if '+' in line:
            values = line.split('+')
            first_value = value_extractor(values[0])
            second_value = value_extractor(values[1])
            if first_value is not None and second_value is not None:
                print(first_value + second_value)
                return True
            
            else:
                return False

        elif '-' in line:
            values = line.split('-')
            first_value = value_extractor(values[0])
            second_value = value_extractor(values[1]) 

            if first_value is not None and second_value is not None:
                print(first_value - second_value)
                return True
            
            else:
                return False

        else:
            value = value_extractor(line)
            if value is None:
                return False
            
            else:
                return True

def condition_checker(line):
    global condition_skipper
    
    if line[0:3] != 'If(' and line[0:3] != 'if(':
        return False
    
    if line[-1] != ')':
        return False
    
    line = line[3:-1]
    
    if '<' in line:
        values = line.split("<")
        first_value = value_extractor(values[0])
        second_value = value_extractor(values[1])
        
        if first_value is None or second_value is None:
            return False
        
        else:
            condition_skipper = not(first_value < second_value)
            return True
    
    elif '>' in line:
        values = line.split(">")
        first_value = value_extractor(values[0])
        second_value = value_extractor(values[1])
        
        if first_value is None or second_value is None:
            return False
        
        else:
            condition_skipper = not(first_value > second_value)
            return True
        
    elif '==' in line:
        values = line.split("==")
        first_value = value_extractor(values[0])
        second_value = value_extractor(values[1])
        
        if first_value is None or second_value is None:
            return False
        
        else:
            condition_skipper = not(first_value == second_value)
            return True
        
    elif '!=' in line:
        values = line.split("!=")
        first_value = value_extractor(values[0])
        second_value = value_extractor(values[1])
        
        if first_value is None or second_value is None:
            return False
        
        else:
            condition_skipper = not(first_value != second_value)
            return True
        
    else:
        return False



def syntax_error(input_file):
    global condition_skipper
    error = False

    try:
        with open(input_file, 'r') as file:
            content = file.read()
            content = content.replace(" ","")
            content = content.split("\n")

            for line in content:
                if condition_skipper:
                    condition_skipper = False
                    continue
                elif declaration_checker(line):
                    continue
                elif assignment_checker(line):
                    continue
                elif math_checker(line):
                    continue
                elif output_checker(line):
                    continue
                elif condition_checker(line):
                    continue
                else:
                    error = True
                    break
            
            if error:
                return False
            else:
                return True



    except FileNotFoundError:
        print('NO ERROR(S) FOUND')
    except Exception as e:
        print('NO ERROR(S) FOUND')

def no_spaces(input_file, nospaces_file):
    try:
        with open(input_file, 'r') as file:
            content = file.read()
            content = content.replace(" ", "")

        with open(nospaces_file, 'w') as file:
            file.write(content)

        return True

    except:
        return False



def extract_special_characters(input_file, res_sym_file):
    try:
        with open(input_file, 'r') as input_file:
            content = input_file.read()

        # Use a regular expression to find words and special characters
        pattern = re.compile(r'\b\w+\b|\W')

        extracted_words = set()
        extracted_chars = set()

        for match in pattern.finditer(content):
            word_or_char = match.group()
            if word_or_char.isalpha() and word_or_char.isascii() and keyword.iskeyword(word_or_char):
                extracted_words.add(word_or_char)
            elif not word_or_char.isalnum() and not word_or_char.isdigit():
                extracted_chars.add(word_or_char)
        
        with open(res_sym_file, 'w') as file:
            file.write("Reserved Words:\n")
            file.write(" ".join(sorted(extracted_words)) + "\n")

            file.write("Special Characters:\n")
            special_chars_representation = [char.replace('\n', '\\n') for char in sorted(extracted_chars)]
            file.write(" ".join(special_chars_representation) + "\n")
        
        return True

    except:
        return False

if __name__ == "__main__":

    try:
        input_file = "PROG1.HL"  # Replace with the path to your input file
        nospaces_file = "NOSPACES.txt"
        res_sym_file = "RES_SYM.txt"

        if syntax_error(input_file) is True and extract_special_characters(input_file , nospaces_file) is True and no_spaces(input_file, res_sym_file) is True:
            print('NO ERROR(S)FOUND')

        else:
            print('ERROR')
    except:
        print('ERROR')