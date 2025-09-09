import pandas as pd
import numpy as np
import re
from utils.cleaning import company_case_logic, normalize_location, detect_job_family, classify_seniority, split_revenue

def transform_data(df):
    # Cleaning id column

    df = df.rename(columns={'Unnamed: 0': 'requirement_id'})

    # Cleaning company column

    df['company'] = df['company'].str.replace(r'\n.*', '', regex=True)
    df['company'] = df['company'].str.strip().str.replace(r'\s+', ' ', regex=True)
    df['company'] = df['company'].str.replace(r'[,](\s*)(?=\b(Inc|LLC|Corp|Ltd|Co)\b)', r'\1', regex=True, flags=re.IGNORECASE)
    df['company'] = df['company'].str.replace(r'\b(Inc|LLC|Corp|Ltd|Co)\b[.,]', r'\1', regex=True, flags=re.IGNORECASE)
    # we identify that there is a row that has empty value (NaN) in all columns except requirement_id, 
    # so we will drop that row
    df = df.drop(323)
    # we also identify that there are some rows that have empty value (NaN) in company column, 
    # after discussing with analyst team, we will fill those NaN with "Unknown"
    df['company'] = df['company'].fillna('Unknown')
    # apply already made function to standardize the suffix and the company name case
    df['company'] = df['company'].apply(company_case_logic)
    # we found that there are some rows that have '.Com' at the end of the company name 
    # because of our function, we will replace it with '.com'
    df['company'] = df['company'].str.replace('.Com', '.com')

    # Cleaning location column

    df[["city", "state", "country", "location_type"]] = df['location'].apply(lambda x: pd.Series(normalize_location(x)))

    # Cleaning job_title column
    df['job_family'] = df['job_title'].apply(detect_job_family)
    df['seniority_level'] = df['job_title'].apply(classify_seniority)

    # Cleaning salary_estimate column
    df["salary_amount"] = (df["salary_estimate"].str.extract(r"\$([\d,\.]+)")[0].str.replace(",", "", regex=True).astype(float))
    df["salary_period"] = df["salary_estimate"].str.extract(r"/(hr|yr)")

    # Cleaning company_size column
    # we identify that there are some rows that have store empty value which is NaN and 'Unknown' 
    # in company_size column, after discussing with analyst team, 
    # we will standardize those values into NaN to make it easier for further analysis
    df['company_size'] = df['company_size'].replace('Unknown', np.nan)
    df['company_size_min'] = df['company_size'].str.extract(r"(\d+)").astype(float)
    df['company_size_max'] = df['company_size'].str.extract(r"to (\d+)").astype(float)

    # Cleaning company_type, company_sector, and company_industry column
    # we identify that there are some rows that have store empty value which is NaN and 'Unknown' 
    # in all three columns, after discussing with analyst team, 
    # we will standardize those values into 'Unknown' to make it easier for analysis 
    # to present the data in dashboard
    df['company_type'] = df['company_type'].fillna('Unknown')
    df['company_sector'] = df['company_sector'].fillna('Unknown')
    df['company_industry'] = df['company_industry'].fillna('Unknown')

    # Cleaning company_founded column
    df['company_founded'] = df["company_founded"].astype("Int64") # changing the datatype to Int64 instead of int because there are some NaN values
    # current_year = datetime.now().year
    # invalid_future = df[df["company_founded"] > current_year]
    # there is no invalid future year

    # Cleaning company_revenue column

    df["company_revenue"] = df["company_revenue"].replace("Unknown / Non-Applicable", np.nan)
    df[["company_revenue_min", "company_revenue_max"]] = df['company_revenue'].apply(split_revenue).apply(pd.Series)

    # Cleaning dates column

    # because the format is already correct, 
    # we just need to convert it into datetime format that handles timezone (using UTC as the standard)
    df["dates"] = pd.to_datetime(df["dates"], utc=True)
    df["date"] = df["dates"].dt.date
    df["day"] = df["dates"].dt.day
    df["month"] = df["dates"].dt.month
    df["year"] = df["dates"].dt.year
    df["time"] = df["dates"].dt.time
    
    # Creating surrogate keys for potential dimensional tables

    df["company_id"] = df["company"].astype("category").cat.codes + 1
    df["location_id"] = df["location"].astype("category").cat.codes + 1
    # the reason why we dont use job_title column as the base for job_id is because the cardinality
    # of the data is too high. so we decided to left it as a descriptive column in fact table
    # and use job_family instead
    df["job_family_id"] = df["job_family"].astype("category").cat.codes + 1
    df["seniority_level_id"] = df["seniority_level"].astype("category").cat.codes + 1
    df["date_id"] = df["dates"].dt.strftime("%Y%m%d").astype(int)
    df["time_id"] = df["dates"].dt.strftime("%H%M%S").astype(int)

    return df