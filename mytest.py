from collections import deque 
def parse_brackets(source):
    stack_of_opened = deque()
    for i in source:
        if i == '(' or i == '[' or i == '{':
            stack_of_opened.append(i)
        elif not stack_of_opened or (i == ')' and stack_of_opened.pop() != '(') or (i == ']' and stack_of_opened.pop() != '[') or (i == '}' and stack_of_opened.pop() != '{'):
            return False
    if stack_of_opened:
        return False
    else:
        return True

print(parse_brackets('[{}]'))  #True
print(parse_brackets('[{}[()][]]'))  #True
print(parse_brackets('[{]}'))  # False
print(parse_brackets('[{]}'))  # False
print(parse_brackets('([{}]'))  # False
print(parse_brackets('[{}]]'))  # False
