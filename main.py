from config.setting import RAW_DATA_PATH, OUTPUT_PATH
from scripts.extract import extract_csv

def main():
    # Extract raw csv data from input path
    raw_requirements_df = extract_csv(RAW_DATA_PATH)

if __name__ == "__main__":
    main()