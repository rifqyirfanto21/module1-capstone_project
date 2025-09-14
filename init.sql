CREATE TABLE dim_company (
    company_id INT PRIMARY KEY,
    company VARCHAR(255),
    company_rating FLOAT,
    company_size VARCHAR(50),
    company_size_min FLOAT,
    company_size_max FLOAT,
    company_type VARCHAR(100),
    company_sector VARCHAR(100),
    company_industry VARCHAR(255),
    company_founded INT,
    company_revenue VARCHAR(100),
    company_revenue_min FLOAT,
    company_revenue_max FLOAT
);

CREATE TABLE dim_location (
    location_id INT PRIMARY KEY,
    location VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    location_type VARCHAR(50)
);

CREATE TABLE dim_job_family (
    job_family_id INT PRIMARY KEY,
    job_family VARCHAR(100)
);

CREATE TABLE dim_seniority (
    seniority_level_id INT PRIMARY KEY,
    seniority_level VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT
);

CREATE TABLE dim_time (
    time_id INT PRIMARY KEY,
    time TIME,
    UNIQUE (time)
);


CREATE TABLE fact_requirements (
    requirement_id INT PRIMARY KEY,
    company_id INT,
    location_id INT,
    job_family_id INT,
    seniority_level_id INT,
    date_id INT,
    time_id INT,
    job_title VARCHAR(255),
    job_description TEXT,
    salary_amount FLOAT,
    salary_period VARCHAR(50),
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
    CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    CONSTRAINT fk_job_family FOREIGN KEY (job_family_id) REFERENCES dim_job_family(job_family_id),
    CONSTRAINT fk_seniority FOREIGN KEY (seniority_level_id) REFERENCES dim_seniority(seniority_level_id),
    CONSTRAINT fk_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    CONSTRAINT fk_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    brand_cleaned VARCHAR(100),
    main_category VARCHAR(100),
    sub_category VARCHAR(100),
    image TEXT,
    link TEXT,
    ratings FLOAT,
    no_of_ratings INT,
    actual_price FLOAT,
    discount_price FLOAT,
    currency VARCHAR(10)
)