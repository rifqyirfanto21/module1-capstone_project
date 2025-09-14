from config.setting import REQUIREMENTS_DATA_PATH, WATCHES_DATA_PATH
from scripts.extract import extract_csv
from scripts.transform import transform_data_requirements, transform_data_watches
from scripts.load import load_to_postgres
from utils.data_profile import data_demographi

def main():
    # Extract raw data_requirements csv data from input path
    raw_requirements_df = extract_csv(REQUIREMENTS_DATA_PATH)

    # Transform data
    transformed_requirements = transform_data_requirements(raw_requirements_df)

    # Data demographi/profiling
    requirements_demographi = data_demographi(transformed_requirements, "job_description")

    # Fact and dimensional tables
    fact_requirements = transformed_requirements[["requirement_id", "company_id", "location_id", "job_family_id", "seniority_level_id", "date_id", "time_id", "job_title", "job_description", "salary_amount", "salary_period"]]
    dim_company = transformed_requirements[["company_id", "company", "company_rating", "company_size", "company_size_min", "company_size_max", "company_type", "company_sector", "company_industry", "company_founded", "company_revenue", "company_revenue_min", "company_revenue_max"]].drop_duplicates(subset=["company_id"]).reset_index(drop=True)
    dim_location = transformed_requirements[["location_id", "location", "city", "state", "country", "location_type"]].drop_duplicates(subset=["location_id"]).reset_index(drop=True)
    dim_job_family = transformed_requirements[["job_family_id", "job_family"]].drop_duplicates(subset=["job_family_id"]).reset_index(drop=True)
    dim_seniority = transformed_requirements[["seniority_level_id", "seniority_level"]].drop_duplicates(subset=["seniority_level_id"]).reset_index(drop=True)
    dim_date = transformed_requirements[["date_id", "date", "day", "month", "year"]].drop_duplicates(subset=["date_id"]).reset_index(drop=True)
    dim_time = transformed_requirements[["time_id", "time"]].drop_duplicates(subset=["time_id"]).reset_index(drop=True)

    # Extract raw watches csv data from input path
    raw_watches_df = extract_csv(WATCHES_DATA_PATH)

    # Transform data
    transformed_watches = transform_data_watches(raw_watches_df)

    # Data demographi/profiling
    watches_demographi = data_demographi(transformed_watches)

    # Dimensional tables
    dim_products = transformed_watches[["product_id", "name", "brand_cleaned", "main_category", "sub_category", "image", "link", "ratings", "no_of_ratings", "actual_price", "discount_price", "currency"]].drop_duplicates(subset=["product_id"]).reset_index(drop=True)

    # Load data to database
    load_to_postgres(dim_company, "dim_company")
    load_to_postgres(dim_location, "dim_location")
    load_to_postgres(dim_job_family, "dim_job_family")
    load_to_postgres(dim_seniority, "dim_seniority")
    load_to_postgres(dim_date, "dim_date")
    load_to_postgres(dim_time, "dim_time")
    load_to_postgres(fact_requirements, "fact_requirements")
    load_to_postgres(dim_products, "dim_products")

    print(requirements_demographi)
    print(watches_demographi)

if __name__ == "__main__":
    main()