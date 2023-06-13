#            Made with <3
#########################################
#        This is still in the           #
#        development stage.             #
#        Please, be patient             #
#        for a better structure.        #
#########################################
# Some feedback would be helpful. Thanks!

from LexerClass import Lexer

import pandas as pd
import os
import secrets
import time
from pyparsing import CaselessKeyword, Word, alphas, nums, Optional, Combine, Group, delimitedList, ParseException, \
    QuotedString, Suppress, oneOf

# logged = 0
# admin = 0

class Parser:
    def __init__(self):
        self.logged = 0
        self.lexer = Lexer()
        self.priv_delete = 0
        self.priv_update = 0
        self.priv_insert = 0
        self.priv_select = 0
        self.filename = None

    # Execute the SQL command
    def execute_sql(self, sql, filename):
        self.filename = filename
        try:
            # Parse the SQL statement
            if sql.startswith('SELECT'):
                parsed_sql = self.lexer.select_stmt.parseString(sql)
            elif sql.startswith('INSERT'):
                parsed_sql = self.lexer.insert_stmt.parseString(sql)
            elif sql.startswith('UPDATE'):
                parsed_sql = self.lexer.update_stmt.parseString(sql)
            elif sql.startswith('CREATE TABLE'):
                parsed_sql = self.lexer.create_table_stmt.parseString(sql)
            elif sql.startswith('DELETE TABLE'):
                parsed_sql = self.lexer.delete_table_stmt.parseString(sql)
            elif sql.startswith('GENERATE KEY'):
                parsed_sql = self.lexer.generate_key_stmt.parseString(sql)
            elif sql.startswith('CREATE USER'):
                parsed_sql = self.lexer.create_user_stmt.parseString(sql)
            elif sql.startswith('LOGIN'):
                parsed_sql = self.lexer.login_stmt.parseString(sql)
            elif sql.startswith('HELP') or sql.startswith('help'):
                parsed_sql = self.lexer.help_stmt.parseString(sql)
            elif sql.startswith('CHANGE TABLE'):
                parsed_sql = self.lexer.change_file_stmt.parseString(sql)
            # Load CSV data using read_csv from pandas
            data = pd.read_csv(self.filename)

            if sql.startswith('CREATE USER'):
                user_token = parsed_sql.token
                print(user_token)
                try:
                    # check if the key expired or not if yes delete token if no add user and delete token
                    results = self.execute_sql(f"SELECT token FROM tokens WHERE token = {user_token}", 'data/token.csv')

                except FileNotFoundError:
                    pass
                    # results = pd.DataFrame({})

                if results:
                    username = parsed_sql.username
                    password = parsed_sql.password
                    mail = parsed_sql.mail
                    token = parsed_sql.token

                    # execute_sql("INSERT INTO users VALUES ' '", 'data/user.csv')

                    df_users = pd.read_csv("data/user.csv")
                    os.remove("data/user.csv")
                    new_user = {"username": username, "password":password, "mail":mail, "token":token}
                    df_users = df_users.append(new_user, ignore_index=True)
                    df_users.to_csv("data/user.csv")

                    return f'Succesfuly created a new user'
                else:
                    return f'Please contact your supervisor for further details'
                # INSERT INTO users VALUES (username, password, mail, priv1, priv2, priv3, priv4)
            elif sql.startswith('LOGIN'):
                df_users = pd.read_csv("data/user.csv")
                df_tokens = pd.read_csv("data/token.csv")
                username = parsed_sql.username
                password = parsed_sql.password
                if df_users[(df_users['username'] == username) & (df_users['password'] == password)][['username', 'password']] is not None:
                    self.logged = 1
                    token = df_users[(df_users['username'] == username) & (df_users['password'] == password)]["token"].values[0]
                    self.priv_delete = df_tokens[(df_tokens['token'] == token)]['priv1_delete'].values[0]
                    self.priv_update = df_tokens[(df_tokens['token'] == token)]['priv2_update'].values[0]
                    self.priv_insert = df_tokens[(df_tokens['token'] == token)]['priv3_insert'].values[0]
                    self.priv_select = df_tokens[(df_tokens['token'] == token)]['priv4_select'].values[0]
                    return f'Successfully logged in with {username}'
                else:
                    return f'No such user or the password is wrong. Please try again.'
                #check if the users credentials exists if yes log in if no try again
            elif sql.startswith('HELP') or sql.startswith('help'):
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

            if self.logged == 0:
                return f'Please login before proceeding'
            if sql.startswith('SELECT'):
                if self.priv_select:
                    # Filter data based on condition (if provided)
                    try:
                        if parsed_sql.conditions:
                            condition_elements = parsed_sql.conditions[1]
                            condition_string = ''.join(condition_elements)
                            data = data.query(condition_string)
                        # Select columns from data
                        selected_data = data[parsed_sql.columns]
                        # Return results as Pandas DataFrame
                        return selected_data
                    except KeyError as e:
                        return e
                else:
                    return f"You don't have such privileges. If something is wrong, contact the administrator."
            elif sql.startswith('INSERT'):
                if self.priv_insert:
                    columns_names = list(data.columns)
                    # Insert new row into data
                    new_rows = {col: int(val) for col, val in list(zip(columns_names, parsed_sql.values_insert))}
                    # print(new_rows)
                    data = data.append(new_rows, ignore_index=True)
                    os.remove(self.filename)
                    # Write updated data to CSV file
                    data.to_csv(self.filename, index=False)
                    return f'Inserted new row(s) into {parsed_sql.table} table.'
                else:
                    return f"You don't have such privileges. If something is wrong, contact the administrator."

            elif sql.startswith('UPDATE'):
                if self.priv_update:
                    # Update rows in data
                    assignments = {}
                    start_col = 1

                    for assignment_list in parsed_sql.assignments:
                        for i in range(1, len(assignment_list)):
                            # print(i % start_col)
                            if i % start_col == 0:
                                # columns / values
                                col = assignment_list[i-1]
                                val = assignment_list[i+1]
                                start_col += 3

                                assignments[col] = val
                    # print(assignments)

                    for column, value in assignments.items():
                        try:
                            assignments[column] = int(value)
                        except ValueError:
                            try:
                                assignments[column] = float(value)
                            except ValueError:
                                pass
                            pass
                    print(assignments)

                    if parsed_sql.conditions[0] == 'WHERE':
                        conditions = {}
                        signs = {}
                        start_condition = 1

                        conditions_list = parsed_sql.conditions[1]
                        for i in range(1, len(conditions_list)-1):
                            # print(i % start_condition)
                            if i % start_condition == 0:
                                # columns / values
                                col = conditions_list[i - 1]
                                sign = conditions_list[i]
                                val = conditions_list[i + 1]
                                start_condition += 3

                                conditions[col] = val
                                signs[col] = sign

                        for column, value in conditions.items():
                            try:
                                conditions[column] = int(value)
                            except ValueError:
                                pass
                        print(conditions)

                        df_condition_str = ''
                        begin = True
                        for column, value in conditions.items():
                            if begin:
                                df_condition_str = df_condition_str + f"(data['{column}']" + signs[column] + str(value)
                                begin = False
                            else:
                                df_condition_str = df_condition_str + "&" + f"data['{column}']" + signs[column] + str(value)
                        df_condition_str = df_condition_str + ')'

                        print(df_condition_str)

                        for column, value in assignments.items():
                            data.loc[eval(df_condition_str), column] = value

                    else:
                        for column, value in assignments.items():
                            data.loc[:, column] = value

                    # Write updated data to CSV file
                    data.to_csv(self.filename, index=False)
                    return f'Updated rows in {parsed_sql.table} table.'
                else:
                    return f"You don't have such privileges. If something is wrong, contact the administrator."

            elif sql.startswith('CREATE TABLE'):
                table = parsed_sql.table
                columns = parsed_sql.columns

                empty_dict = {}
                for column in columns:
                    empty_dict[column] = []

                data = pd.DataFrame(empty_dict)

                data.to_csv(f'data/{table}.csv')
                self.filename = f'data/{table}.csv'

                return f"Table {table} was created!"

            elif sql.startswith('DELETE TABLE'):
                if self.priv_delete:
                    delete = input(f"Are you sure you want to delete the table '{self.filename}' ? [y/n] ")

                    if delete == "y":
                        os.remove(self.filename)
                        return f"{self.filename} has been deleted."
                    else:
                        return f"{self.filename} has not been deleted."
                else:
                    return f"You don't have such privileges. If something is wrong, contact the administrator."

            elif sql.startswith("CHANGE TABLE"):
                table = parsed_sql.table

                self.filename = None

                return


        except ParseException as e:
            print(f'Error parsing SimpQL: {e}')


# Example usage
# results = execute_sql('INSERT INTO table VALUES 1,1,1,1,1,1,1,1,1,1,1,1', 'data/data1.csv')
# print(results)

# results = execute_sql('SELECT ph FROM data', 'data/data1.csv')
# print(results)

#
# results = execute_sql('UPDATE data SET ph=36, Hardness=1', 'data/data.csv')
# print(results)
