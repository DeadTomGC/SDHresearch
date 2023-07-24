import pandas as pd

def calculate_correlations(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Drop the name column, as we only want to calculate correlations between conditions
    df = df.drop('Age', axis=1)
    df = df.drop('Gender', axis=1)
    print(df)
    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    return correlation_matrix

csv_file = 'scrubbed.csv'  # Replace with your CSV file path
correlation_matrix = calculate_correlations(csv_file)
print(correlation_matrix)
correlation_matrix.to_csv('output.csv')
