import subprocess
import argparse
import time

def run_main_script(times, form_url, include_required):
    """
    Run main.py multiple times.
    
    :param times: Number of times to run main.py
    :param form_url: URL of the Google Form to be submitted
    :param include_required: Whether to include only required fields
    """
    for i in range(times):
        print(f"Running iteration {i+1} of {times}...")
        # Build the command to run main.py with the necessary arguments
        command = ['python', 'main.py', '--url', form_url]
        
        # If include_required is not passed, don't add the --required flag
        if include_required:
            command.append('--required')
        
        # Run the script
        subprocess.run(command)
        
        # Optional: Pause between runs
        #time.sleep(2)  # Sleep for 2 seconds before the next run (adjust as needed)
        print(f"Iteration {i+1} completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run main.py multiple times.")
    parser.add_argument('-t', '--times', type=int, required=True, help="Number of times to run main.py.")
    parser.add_argument('-u', '--url', required=True, help="Google Form URL.")
    parser.add_argument('-r', '--required', action='store_true', help="Include only required fields.")
    
    args = parser.parse_args()
    
    # Run the script for the specified number of times
    run_main_script(args.times, args.url, include_required=False)  # Set include_required to False for all fields
