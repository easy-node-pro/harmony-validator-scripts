import subprocess
import os

# Define the directories to check
directories = ['harmony/harmony_db_0', 'harmony0/harmony_db_0', 'harmony1/harmony_db_0', 'harmony2/harmony_db_0', 'harmony3/harmony_db_0', 'harmony4/harmony_db_0']

# Initialize a dictionary to store the results
results = {}

# Loop through the directories and run du -sh and df
for directory in directories:
    full_directory = os.path.join(os.path.expanduser('~'), directory)
    if os.path.exists(full_directory):
        try:
            # Run du -sh to get the size
            du_output = subprocess.check_output(['du', '-sh', full_directory]).decode('utf-8')
            # Extract the size from the output
            size = du_output.split('\t')[0]
            # Run df to get the free space
            df_output = subprocess.check_output(['df', '-h', full_directory]).decode('utf-8')
            # Extract the free space from the output
            free = df_output.split('\n')[1].split()[3]
            # Add the result to the dictionary
            results[directory] = {'size': size, 'free': free}
        except subprocess.CalledProcessError as e:
            # If the command fails, print an error message and continue
            print(f"Error running du -sh or df on {directory}: {e}")
    else:
        # If the directory does not exist, skip it
        continue

# Check if all directories have the same size
if len(results) > 0:
    sizes = [result['size'] for result in results.values()]
    frees = [result['free'] for result in results.values()]
    print("Directory Info: Used / Free")
    for directory, size in results.items():
        print(f"{directory}: {size['size']} / {size['free']}")
else:
    # If no directories exist, print a message
    print("No directories exist")