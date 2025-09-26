import pandas as pd

# Create a sample DataFrame
data = {'col1': [1, 2], 'col2': ['A', 'B']}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Add a new row using .loc
new_row_values = [3, 'C']
df.loc[len(df)] = new_row_values

print("\nDataFrame after adding a row:")
print(df)