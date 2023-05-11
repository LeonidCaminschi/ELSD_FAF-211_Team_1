#       Made with <3
########################################
#       This is still in the
#       development stage.
#       Please, be patient
#       for a better structure.
#########################################

import pandas as pd
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

# Execute the SQL command
def execute_sql(sql, filename):
    try:
        # Parse the SQL statement
        if sql.startswith('SELECT'):
            parsed_sql = select_stmt.parseString(sql)
        elif sql.startswith('INSERT'):
            parsed_sql = insert_stmt.parseString(sql)
        else:
            parsed_sql = update_stmt.parseString(sql)
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
            return f'Inserted new row into {parsed_sql.table} table.'
        else:
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
