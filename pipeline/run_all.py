import os
import subprocess
import sys
import glob

def prompt_for_directory(prompt):
    directory = input(prompt).strip()
    if not directory:
        print(f"Error: {prompt} is required. Exiting.")
        sys.exit(1)
    if not os.path.isdir(directory):
        print(f"Error: Directory does not exist - {directory}")
        sys.exit(1)
    return os.path.abspath(directory)

def get_slide_files(input_dir):
    # Look for both .ndpi and .svs files
    slide_files = glob.glob(os.path.join(input_dir, "*.ndpi")) + \
                  glob.glob(os.path.join(input_dir, "*.svs"))
    if not slide_files:
        print(f"Error: No .ndpi or .svs files found in the directory: {input_dir}. Exiting.")
        sys.exit(1)
    return slide_files

def run_histoqc(input_dir, output_dir):
    print(f"Running HistoQC with input directory: {input_dir} and output directory: {output_dir}")
    
    slide_files = get_slide_files(input_dir)

    command = [
        "python", "-m", "histoqc",
        *slide_files,
        "-o", output_dir,
        "-c", "../HistoQC/histoqc/config/config_clinical.ini",
        "-n", "4", "-f"
    ]

    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running HistoQC: {e}")
        sys.exit(1)


def run_postprocess(output_dir):
    print("Running post-processing script...")
    postprocess_path = os.path.join(os.path.dirname(__file__), "postprocess.py")
    venv_python = sys.executable  # Ensures it uses the virtual environment's Python
    try:
        subprocess.run([venv_python, postprocess_path, output_dir], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running postprocess: {e}")
        sys.exit(1)
        
def main():
    input_dir = prompt_for_directory("Please enter the path to the folder containing .ndpi/.svs files: ")
    output_dir = prompt_for_directory("Please enter the path to the output folder: ")

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist. Exiting.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: Output directory {output_dir} does not exist. Exiting.")
        sys.exit(1)

    run_histoqc(input_dir, output_dir)
    run_postprocess(output_dir)

if __name__ == "__main__":
    main()
