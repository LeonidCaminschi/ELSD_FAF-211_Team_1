import pandas as pd
from pyparsing import CaselessKeyword, Word, alphas, nums, Optional, Combine, Group, delimitedList, ParseException

# Define the SQL syntax
select_stmt = CaselessKeyword('select') + (Word('*') | delimitedList(Word(alphas), ','))('columns') + \
              CaselessKeyword('from') + Word(alphas + nums + '_')('table') + \
              Optional(CaselessKeyword('where') + Combine(Word(alphas) + Word(nums) + Word(alphas)))('condition')

insert_stmt = CaselessKeyword('insert') + CaselessKeyword('into') + Word(alphas + nums + '_')('table') + \
              Group(delimitedList(Word(alphas), ','))('columns') + \
              CaselessKeyword('values') + Group(delimitedList(Word(alphas + nums), ','))('values')

update_stmt = CaselessKeyword('update') + Word(alphas + nums + '_')('table') + \
              CaselessKeyword('set') + delimitedList(Combine(Word(alphas) + Optional(Word(nums))), ',')('assignments') + \
              Optional(CaselessKeyword('where') + Combine(Word(alphas) + Word(nums) + Word(alphas)))('condition')

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
            if parsed_sql.condition:
                data = data.query(parsed_sql.condition)
            # Select columns from data
            selected_data = data[parsed_sql.columns]
            # Return results as Pandas DataFrame
            return selected_data
        elif sql.startswith('INSERT'):
            # Insert new row into data
            new_row = {col: val for col, val in zip(parsed_sql.columns, parsed_sql.values)}
            data = data.append(new_row, ignore_index=True)
            # Write updated data to CSV file
            data.to_csv(filename, index=False)
            return f'Inserted new row into {parsed_sql.table} table.'
        else:
            # Update rows in data
            data.loc[data.eval(parsed_sql.condition), parsed_sql.assignments] = parsed_sql.values.asList()
            # Write updated data to CSV file
            data.to_csv(filename, index=False)
            return f'Updated rows in {parsed_sql.table} table.'
    except ParseException as e:
        print(f'Error parsing SQL: {e}')

# Example usage
# results = execute_sql('INSERT INTO people (name, age, gender) VALUES (John, 35, M)', 'people.csv')
# print(results)

results = execute_sql('SELECT * FROM data', '/../data/data.csv')
print(results)

# results = execute_sql('UPDATE people SET age=36 WHERE name=John', 'people.csv')
# print(results)
