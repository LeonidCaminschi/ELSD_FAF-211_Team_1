#            Made with <3
#########################################
#        This is still in the           #
#        development stage.             #
#        Please, be patient             #
#        for a better structure.        #
#########################################
# Some feedback would be helpful. Thanks!

from pyparsing import CaselessKeyword, Word, alphas, nums, Optional, Combine, Group, delimitedList, ParseException, \
    QuotedString, Suppress, oneOf

class Lexer:
    def __init__(self):
        # Define the SQL syntax
        self.select_stmt = CaselessKeyword('select') + delimitedList(Word(alphas + nums + "_"), ',')('columns') + \
                      CaselessKeyword('from') + Word(alphas + nums + '_')('table') + \
                      Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                        oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))))('conditions')

        self.insert_stmt = CaselessKeyword('insert into') + Word(alphas + nums + '_')('table') + \
                      CaselessKeyword('values') + Group(delimitedList(Word(alphas + nums), ','))('values_insert')

        self.update_stmt = CaselessKeyword('UPDATE') + Word(alphas + nums + '_')('table') + \
                      CaselessKeyword('SET') + delimitedList(Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums)))('col_to_assign') + \
                        Word('=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums))('value_to_assign'), ',')))('assignments') + \
                      Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                        oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))), ',')('conditions')

        self.create_table_stmt = CaselessKeyword('CREATE TABLE') + Word(alphas + nums + '_')('table') + \
                      CaselessKeyword('WITH') + delimitedList(Word(alphas + nums + "_"), ',')('columns')

        self.delete_table_stmt = CaselessKeyword('DELETE TABLE') + Word(alphas + nums + '_')('table')

        self.generate_key_stmt = CaselessKeyword('generate key') + (Word(nums) + Word(nums) + Word(nums) + Word(nums))('privileges') + \
                                                               Word(nums)('timeout')

        self.create_user_stmt = CaselessKeyword('create user') + \
                           Word(alphas)('username') + \
                           Combine(Word(alphas) + Optional(Word(nums)))('password') + \
                           Word(alphas + '@' + alphas + '.' + alphas)('mail') + \
                           Combine(Word(alphas + nums))('token')

        self.login_stmt = CaselessKeyword('login') + \
                      Word(alphas)('username') + \
                      Combine(Word(alphas) + Optional(Word(nums)))('password')

        self.help_stmt = CaselessKeyword('help')('help')

        self.change_file_stmt = CaselessKeyword('change table')
