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
        self.select_stmt = CaselessKeyword('select') + delimitedList(Word(alphas), ',')('columns') + \
                      CaselessKeyword('from') + Word(alphas + nums + '_')('table') + \
                      Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                        oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))))('conditions')

        self.insert_stmt = CaselessKeyword('insert into') + Word(alphas + nums + '_')('table') + \
                      CaselessKeyword('values') + Group(delimitedList(Word(alphas + nums), ','))('values_insert')

        self.update_stmt = CaselessKeyword('UPDATE') + Word(alphas + nums + '_')('table') + \
                      CaselessKeyword('SET') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                        Word('=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)), ','))('assignments') + \
                      Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                        oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))))('conditions')

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
