from config.setting import RAW_DATA_PATH, OUTPUT_PATH
from scripts.extract import extract_csv
from scripts.transform import transform_data

def main():
    # Extract raw csv data from input path
    raw_requirements_df = extract_csv(RAW_DATA_PATH)

    # Transform data
    transformed_requirements = transform_data(raw_requirements_df)

    print(transformed_requirements)

if __name__ == "__main__":
    main()