import subprocess
import sys

n = 20

def run_script(script_name, pass_n=False):
    try:
        # Print a message indicating which script is starting
        print(f"\nRunning: {script_name}")

        # Check if we need to pass N as an argument
        # Run the Python script as a subprocess
        # sys.executable ensures it uses the current Python interpreter
        # check=True will raise an error if the script fails
        if pass_n:
            result = subprocess.run([sys.executable, script_name, str(n)], check=True)
        else: 
            result = subprocess.run([sys.executable, script_name], check=True)

        # Print a success message after the script completes
        print(f"Finished: {script_name}\n")

    except subprocess.CalledProcessError as e:
        # Print an error message if the script fails to run successfully
        print(f"Error occurred while running {script_name}: {e}")

        # Exit the entire program with status 1 (indicates an error)
        sys.exit(1)

def main():
    # Step 1: Import data
    run_script("import_data.py")

    # Step 2: Clean data
    run_script("clean_data.py")

    # Step 3: Run polynomial ridge regression with MLflow tracking
    run_script("poly_regressor_Python_1.0.0.py", pass_n=True)

if __name__ == "__main__":
    main()