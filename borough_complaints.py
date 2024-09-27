import argparse
import csv
from collections import defaultdict
from datetime import datetime

def parse_arguments():
    # Define argument parser
    parser = argparse.ArgumentParser(description="Counts complaint types per borough in a given date range.")
    
    # Define required arguments
    parser.add_argument('-i', '--input', required=True, help="Path to the input CSV file")
    parser.add_argument('-s', '--start', required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument('-e', '--end', required=True, help="End date (YYYY-MM-DD)")
    
    # Define optional arguments
    parser.add_argument('-o', '--output', help="Path to the output CSV file (optional)")
    
    return parser.parse_args()

def process_csv(input_file, start_date, end_date):
    # Convert string dates to datetime objects for comparison
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Dictionary to hold complaint type counts per borough
    complaint_counts = defaultdict(lambda: defaultdict(int))

    # Read the CSV file
    with open(input_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

        # Indexes based on your sample data
        created_date_idx = 1
        complaint_type_idx = 6
        borough_idx = 17

        # Iterate through each row and process it
        for row in reader:
            try:
                # Parse the created date
                created_date = datetime.strptime(row[created_date_idx].split()[0], '%m/%d/%Y')
                
                # Get complaint type and borough
                complaint_type = row[complaint_type_idx]
                borough = row[borough_idx]

                # Only count complaints within the date range
                if start <= created_date <= end:
                    complaint_counts[complaint_type][borough] += 1
            except (ValueError, IndexError):
                # Handle any parsing errors (e.g., missing or improperly formatted dates)
                continue

    return complaint_counts

def output_results(complaint_counts, output_file=None):
    # Output the results in CSV format
    if output_file:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['complaint type', 'borough', 'count'])
            for complaint_type, boroughs in complaint_counts.items():
                for borough, count in boroughs.items():
                    writer.writerow([complaint_type, borough, count])
    else:
        # Print to stdout if no output file is specified
        print('complaint type, borough, count')
        for complaint_type, boroughs in complaint_counts.items():
            for borough, count in boroughs.items():
                print(f'{complaint_type}, {borough}, {count}')

def main():
    # Parse arguments
    args = parse_arguments()
    
    # Process the CSV file and get the results
    complaint_counts = process_csv(args.input, args.start, args.end)
    
    # Output results
    output_results(complaint_counts, args.output)

if __name__ == "__main__":
    main()

