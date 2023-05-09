from syntax.LexerClass import Lexer

while 1:
    input_code = input(">")

    lexer = Lexer(input_code)
    tokens = lexer.tokenize()


#### Example HERE

# code_test = '''
#     SELECT
#         col1,
#         col2,
#         col3
#     FROM table1 WHERE col1 >= 30
#     ORDER_BY col2;
#
#     SELECT col4 FROM table2 WHERE 1==1;
# '''
#
# lexer = Lexer(code_test)
# tokens = lexer.tokenize()