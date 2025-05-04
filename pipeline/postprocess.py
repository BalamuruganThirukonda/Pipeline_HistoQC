import pandas as pd
import os
import sys
from io import StringIO

def main():
    if len(sys.argv) != 2:
        print("Usage: python postprocess.py <output_dir>")
        sys.exit(1)
    
    tsv_dir = sys.argv[1]

    if not os.path.isdir(tsv_dir):
        print(f"Error: The specified path is not a directory: {tsv_dir}")
        sys.exit(1)
        
    tsv_file = next((f for f in os.listdir(tsv_dir) if f.endswith(".tsv")), None)
    if not tsv_file:
        print(f"Error: No .tsv file found in the directory: {tsv_dir}. Exiting.")
        sys.exit(1)
    
    tsv_path = os.path.join(tsv_dir, tsv_file)

    with open(tsv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_line_index = next(i for i, line in enumerate(lines) if line.startswith('#dataset:filename'))
    columns = lines[header_line_index][1:].strip().split('\t')
    data_lines = lines[header_line_index + 1:]

    df = pd.read_csv(StringIO(''.join(data_lines)), sep='\t', names=columns)

    # Save to Excel
    output_excel_path = tsv_path.replace(".tsv", ".xlsx")
    df.to_excel(output_excel_path, index=False)
    print(f"Successfully converted to Excel: {output_excel_path}")

if __name__ == "__main__":
    main()
