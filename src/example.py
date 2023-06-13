#            Made with <3               #
#########################################
#        This is still in the           #
#        development stage.             #
#        Please, be patient             #
#        for a better structure.        #
#########################################
# Some feedback would be helpful. Thanks!

from LexerClass import Lexer
from ParserClass import Parser

import pandas as pd

import warnings
warnings.simplefilter('ignore')

# while 1:
#     path = input("Path to table: -> ")
#     try:
#         file = pd.read_csv(path)
#         if file.shape != None:
#             break
#     except FileNotFoundError:
#         print(f"The file with path '{path}' was not found. Please try again!")

parser = Parser()
while 1:
    if parser.filename is None:
        path = input("Path to table: -> ")
        try:
            file = pd.read_csv(path)
        except FileNotFoundError:
            print(f"The file with path '{path}' was not found. Please try again!")
            continue

    print("-> ", end="")
    code = input()
    if code == "QUIT":
        break
    result = parser.execute_sql(code, path)
    print(result)

print("Session finished successfully!")