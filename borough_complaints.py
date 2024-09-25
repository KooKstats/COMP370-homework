import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='CLI tool to count complaints per borough for a given date range.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input CSV file')
    parser.add_argument('-s', '--start', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end', required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('-o', '--output', help='Optional output file path. If not provided, results are printed to stdout')
    return parser.parse_args()

def filter_data(df, start_date, end_date):
    # Convert relevant columns to datetime
    df['Created Date'] = pd.to_datetime(df.iloc[:, 1], errors='coerce')
    df['Closed Date'] = pd.to_datetime(df.iloc[:, 2], errors='coerce')
    
    # Filter rows based on the date range
    mask = (df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)
    df = df[mask]
    
    # Remove rows where the Closed Date is before the Created Date
    df = df[df['Closed Date'] >= df['Created Date']]
    
    return df

def count_complaints(df):
    # Group by Complaint Type (column 6) and Borough (column 26) and count
    return df.groupby([df.iloc[:, 5], df.iloc[:, 25]]).size().reset_index(name='Count')

def output_results(df, output_file=None):
    # Rename columns for output
    df.columns = ['Complaint Type', 'Borough', 'Count']
    
    # Output to CSV format
    if output_file:
        df.to_csv(output_file, index=False)
    else:
        print(df.to_csv(index=False))

def main():
    # Parse arguments
    args = parse_args()

    # Read the input CSV file without headers
    df = pd.read_csv(args.input, header=None, low_memory=False)

    # Filter data based on date range and remove invalid rows
    filtered_df = filter_data(df, args.start, args.end)

    # Count complaints by type and borough
    result_df = count_complaints(filtered_df)

    # Output results to file or stdout
    output_results(result_df, args.output)

if __name__ == '__main__':
    main()
