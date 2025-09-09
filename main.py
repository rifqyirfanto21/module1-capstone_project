from config.setting import RAW_DATA_PATH, OUTPUT_PATH
from scripts.extract import extract_csv
from scripts.transform import transform_data
from utils.data_profile import data_demographi

def main():
    # Extract raw csv data from input path
    raw_requirements_df = extract_csv(RAW_DATA_PATH)

    # Transform data
    transformed_requirements = transform_data(raw_requirements_df)

    # Data demographi/profiling
    requirements_demographi = data_demographi(transformed_requirements, "job_description")

    # Fact and dimensional tables
    fact_requirements = transformed_requirements[["requirement_id", "company_id", "location_id", "job_family_id", "seniority_level_id", "date_id", "time_id", "job_title", "job_description", "salary_amount", "salary_period"]]
    dim_company = transformed_requirements[["company_id", "company", "company_rating", "company_size", "company_size_min", "company_size_max", "company_type", "company_sector", "company_industry", "company_founded", "company_revenue", "company_revenue_min", "company_revenue_max"]].drop_duplicates().reset_index(drop=True)
    dim_location = transformed_requirements[["location_id", "location", "city", "state", "country", "location_type"]].drop_duplicates().reset_index(drop=True)
    dim_job_family = transformed_requirements[["job_family_id", "job_family"]].drop_duplicates().reset_index(drop=True)
    dim_seniority = transformed_requirements[["seniority_level_id", "seniority_level"]].drop_duplicates().reset_index(drop=True)
    dim_date = transformed_requirements[["date_id", "date", "day", "month", "year"]].drop_duplicates().reset_index(drop=True)
    dim_time = transformed_requirements[["time_id", "time"]].drop_duplicates().reset_index(drop=True)

    print(requirements_demographi)

if __name__ == "__main__":
    main()