'''
This code will read the canvas students gradebook from canvas
and convert it to a csv file to register students in 
runestone.academy text books
header: username,email,first_name,last_name,password,course
'''
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Input CSV file", required=True)
parser.add_argument("-p", "--password", help="course register password", required=True)
args = parser.parse_args()
COURSE_ID = 'CIS256'
PW = args.password
# Open the input CSV file
with open(args.file, 'r') as csvfile:
    # Read the CSV file using the DictReader
    reader = csv.DictReader(csvfile)

    # Modify the columns as desired
    new_data = []
    for row in reader:
        # Add a new column to the data
        newrow = {}
        lastname,firstname = row['Student'].split(',')
        newrow['username'] = lastname.strip().lower()+firstname.strip()[0].lower()
        newrow['email'] = row['SIS Login ID'].strip()+"@maricopa.edu"
        newrow['first_name'] = firstname.strip()
        newrow['last_name'] = lastname.strip()
        newrow['password'] = PW
        newrow['course'] = COURSE_ID
        new_data.append(newrow)

    # Write the modified data to a new CSV file
    with open(f'output_{args.file}', 'w') as new_csvfile:
        # Define the field names for the new CSV file
        fieldnames = ['username','email','first_name','last_name','password','course']
        writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for row in new_data:
            writer.writerow(row)


