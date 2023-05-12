from LexerClass import Lexer
from ParserClass import Parser

import warnings
warnings.simplefilter('ignore')

path = input("Path to table: -> ")
# path = "data/data.csv"
parser = Parser()
while 1:
    if not path:
        path = input("Path to table: -> ")
    print("-> ", end="")
    code = input()
    result = parser.execute_sql(code, path)
    print(result)