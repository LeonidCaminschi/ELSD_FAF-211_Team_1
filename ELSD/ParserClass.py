#       Made with <3
########################################
#       This is still in the
#       development stage.
#       Please, be patient
#       for a better structure.
#########################################

import pandas as pd
import secrets
import time
from pyparsing import CaselessKeyword, Word, alphas, nums, Optional, Combine, Group, delimitedList, ParseException, \
    QuotedString, Suppress, oneOf

# Define the SQL syntax
select_stmt = CaselessKeyword('select') + delimitedList(Word(alphas), ',')('columns') + \
              CaselessKeyword('from') + Word(alphas + nums + '_')('table') + \
              Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))))('conditions')

insert_stmt = CaselessKeyword('insert into') + Word(alphas + nums + '_')('table') + \
              CaselessKeyword('values') + Group(delimitedList(Word(alphas + nums), ','))('values_insert')

update_stmt = CaselessKeyword('UPDATE') + Word(alphas + nums + '_')('table') + \
              CaselessKeyword('SET') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                Word('=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)), ','))('assignments') + \
              Optional(CaselessKeyword('where') + Group(delimitedList(Combine(Word(alphas) + Optional(Word(nums))) + \
                oneOf('= != < > <= >=') + (Combine(Word(alphas) + Optional(Word(nums))) | Word(nums)))))('conditions')

generate_key_stmt = CaselessKeyword('generate key') + (Word(nums) + Word(nums) + Word(nums) + Word(nums))('privileges') + \
                                                       Word(nums)('timeout')

create_user_stmt = CaselessKeyword('create user') + \
                   Word(alphas)('username') + \
                   Combine(Word(alphas) + Optional(Word(nums)))('password') + \
                   Word(alphas + '@' + alphas)('mail') + \
                   Combine(Word(alphas) + Optional(Word(nums)))('token')

login_stmt = CaselessKeyword('login') + \
              Word(alphas)('username') + \
              Combine(Word(alphas) + Optional(Word(nums)))('password')

help_stmt = CaselessKeyword('help')

logged = 0
admin = 0

# Execute the SQL command
def execute_sql(sql, filename):
    try:
        if sql.startswith('CREATE USER'):
            # check if the key expired or not if yes delete token if no add user and delete token
            results = execute_sql('SELECT token FROM tokens WHERE token = user_token', 'data/tokens.csv')
            if results:
                execute_sql('INSERT INTO users VALUES `', 'data/users.csv')
                return f'Succesfuly created a new user'
            else:
                return f'Please contact your supervisor for further details'
            # INSERT INTO users VALUES (username, password, mail, priv1, priv2, priv3, priv4)
        elif sql.startswith('LOGIN'):
            results = execute_sql('SELECT username, password FROM users WHERE username = user_username && password = user_password', 'data/users.csv')
            if results:
                return f'Succesfuly logged in'
            else:
                return f'Please try again'
            #check if the users credentials exists if yes log in if no try again
        elif sql.startswith('HELP'):
            return f'First of all \"create user <username> <password> <mail> <token>\" must be performed \n' \
                   f'in order to access the database contents <token> element is a specific key generated \n' \
                   f'by an admin or a manager in order to secure user access to the database ask your admin\n' \
                   f'for it if you don\'t have one\n' \
                   f'\n' \
                   f'After the user creation is done access your specific user by \"login <username> <password>\"\n' \
                   f'if such a user exists you will be logged in promptly otherwise you will be asked to try again\n' \
                   f'\n' \
                   f'After logging in you have some privileges such as SELECT INSERT and UPDATING tables\n' \
                   f'SELECT lets you see and filter the data as an output following this structure\n' \
                   f'\"select <columns> from <table>\" and optionaly you can add afterwards \n' \
                   f'\"where <column> <comparison> <value>\"\n' \
                   f'INSERT lets you add new rows to a table following this pattern \n' \
                   f'\"insert into <table> VALUES <values>\" \n' \
                   f'UPDATE lets you modify already existing data from a table like \n' \
                   f'\"update <table> set <columns> = <values>\" \n' \
                   f'with optional operators being the following \n' \
                   f'\"where <column> <condition> <value>\" \n'

        if logged == 0:
            return f'Please login before proceeding'

        # Parse the SQL statement
        if sql.startswith('SELECT'):
            parsed_sql = select_stmt.parseString(sql)
        elif sql.startswith('INSERT'):
            parsed_sql = insert_stmt.parseString(sql)
        elif sql.startswith('UPDATE'):
            parsed_sql = update_stmt.parseString(sql)
        elif sql.startswith('GENERATE KEY'):
            parsed_sql = generate_key_stmt.parseString(sql)
        elif sql.startswith('CREATE USER'):
            parsed_sql = create_user_stmt.parseString(sql)
        elif sql.startswith('LOGIN'):
            parsed_sql = login_stmt.parseString(sql)
        elif sql.startswith('HELP'):
            parsed_sql = help_stmt.parseString(sql)
        # Load CSV data using read_csv from pandas
        data = pd.read_csv(filename)
        if sql.startswith('SELECT'):
            # Filter data based on condition (if provided)
            if parsed_sql.conditions:
                condition_elements = parsed_sql.conditions[1]
                condition_string = ''.join(condition_elements)
                data = data.query(condition_string)
            # Select columns from data
            selected_data = data[parsed_sql.columns]
            # Return results as Pandas DataFrame
            return selected_data
        elif sql.startswith('INSERT'):
            columns_names = list(data.columns)
            # Insert new row into data
            new_rows = {col: int(val) for col, val in list(zip(columns_names, parsed_sql.values_insert))}
            # print(new_rows)
            data = data.append(new_rows, ignore_index=True)
            # Write updated data to CSV file
            data.to_csv(filename, index=False)
            return f'Inserted new row(s) into {parsed_sql.table} table.'
        elif sql.startswith('UPDATE'):
            # Update rows in data
            assignments = {}
            for assignment in parsed_sql.assignments:
                print(assignment)
            #     column, value = assignment.split('=')
            #     try:
            #         value = int(value)
            #     except ValueError:
            #         pass
            #     assignments[column.strip()] = value.strip()
            # if parsed_sql.conditions:
            #     condition_str = ' '.join(parsed_sql.conditions)
            #     data.loc[data.eval(condition_str), list(assignments.keys())] = list(assignments.values())
            # else:
            #     data[list(assignments.keys())] = list(assignments.values())
            # # Write updated data to CSV file
            # data.to_csv(filename, index=False)
            return f'Updated rows in {parsed_sql.table} table.'
        elif sql.startswith('GENERATE KEY'):
            if admin == 1:
                # Check if the request was done by an admin or above
                token = secrets.token_hex(16)
                execute_sql('INSERT INTO tokens VALUES `token`, `time.time()`', 'data/tokens.csv')
                # INSERT INTO tokens VALUES (token, priv1, priv2, priv3, priv4, timeout, ts)
                return f'Succesfuly generated new key'
            else:
                return f'Not enough privileges for this command'
    except ParseException as e:
        print(f'Error parsing SQL: {e}')


# Example usage
# results = execute_sql('INSERT INTO table VALUES 1,1,1,1,1,1,1,1,1,1,1,1', 'data/data1.csv')
# print(results)

results = execute_sql('SELECT ph FROM data', 'data/data1.csv')
print(results)

#
# results = execute_sql('UPDATE data SET ph=36, Hardness=1', 'data/data.csv')
# print(results)
