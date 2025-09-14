# Module 1 Data Engineering Capstone Project

**Author**: Muhammad Rifqy Irfanto
**Program**: Purwadhika Data Engineering Bootcamp  

## Project Overview
This repository contains the capstone project for the Module 1 Data Engineering Course at Purwadhika. The project is designed to mimic a professional data engineering workflow, including best practices such as code documentation, reasoning for data normalization decisions, and modular code structure. The goal is to simulate a production environment and demonstrate proficiency in building robust data pipelines.

## Table of Contents
- [Data Sources](#data-sources)
- [Database Schema](#database-schema)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Docker Usage](#docker-usage)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Project Highlights](#project-highlights)

## Data Sources
- `data/data_requirements.csv`: Contains job requirements and related company information
- `data/Watches.csv`: Contains product data for watches, including brand, category, pricing, and ratings

## Database Schema
The project implements a star schema design with PostgreSQL to store processed data:

### Requirements Dataset:
- **Fact Table:** `fact_requirements` - Core job requirements with foreign keys
- **Dimension Tables:** 
  - `dim_company` - Company information and metadata
  - `dim_location` - Geographic location data
  - `dim_job_family` - Job categories and families
  - `dim_seniority` - Seniority levels and hierarchy
  - `dim_date` - Date dimension for temporal analysis
  - `dim_time` - Time dimension for temporal analysis

### Watches Dataset:
- **Dimension Table:** `dim_products` - Product catalog with specifications

## Features
- **ETL Pipeline**: Complete Extract, Transform, Load workflow
- **Data Extraction**: Extracts raw data from CSV files for requirements and watches datasets
- **Data Transformation**: 
  - Data cleaning and normalization
  - Duplicate handling and data quality checks
  - Star schema implementation
- **Data Profiling**: enerates demographic and profiling summaries for datasets
- **Database Integration**: PostgreSQL with proper foreign key relationships
- **Production-Ready Practices**: 
  - Modular code architecture
  - Comprehensive documentation

## Project Structure
```
module1-capstone_project/
├── config/
│   └── setting.py           # Configuration variables (paths, DB connection)
├── data/
│   ├── data_requirements.csv # Raw job requirements data
│   └── Watches.csv           # Raw watches product data
├── scripts/
│   ├── db_connect.py        # Database connection helper
│   ├── extract.py           # Data extraction logic
│   ├── transform.py         # Data transformation logic
│   └── load.py              # Data loading logic
├── utils/
│   ├── cleaning.py          # Data cleaning utilities
│   └── data_profile.py      # Data profiling functions
├── main.py                  # Main pipeline orchestrator
├── requirements.txt         # Python dependencies
├── docker-compose.yaml      # Docker configuration for PostgreSQL
├── init.sql                 # Database initialization script
└── README.md                # Project documentation
```

## Technologies Used
- **Python 3.12** - Core programming language
- **PostgreSQL** - Relational database
- **Docker & Docker Compose** - Containerization
- **pandas** - Data manipulation and analysis
- **SQLAlchemy** - Database ORM
- **psycopg2** - PostgreSQL adapter

## Getting Started

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- Git

### Installation
1. **Clone the repository:**
   ```bash
   git clone [your-repo-url]
   cd module1-capstone_project
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d
   ```

5. **Configure connection settings:**
   - Edit `config/setting.py` as needed for your environment

6. **Run the ETL pipeline:**
   ```bash
   python main.py
   ```

## Docker Usage
The project uses Docker to manage the PostgreSQL database environment, ensuring consistency and portability:

```bash
# Start the database
docker-compose up -d

# View logs
docker logs postgres_db

# Stop the database
docker-compose down

# Stop and remove data (clean start)
docker-compose down -v
```

## Usage
The pipeline will:
1. Extract data from CSV files in the `data/` directory
2. Transform and clean the data to follow the star schema
3. Create fact and dimension tables for analytical queries
4. Load processed data into PostgreSQL database
5. Generate data profiling reports

## Project Highlights
- **Production-Ready Architecture**: Modular, scalable code structure
- **Data Quality Focus**: Comprehensive cleaning and validation processes  
- **Star Schema Implementation**: Optimized for analytical workloads
- **Rerunnable Pipeline**: Handles incremental and full refresh scenarios
- **Container-Based Development**: Docker ensures consistent environments
- **Comprehensive Documentation**: Detailed docstrings and engineering decision rationale

---

## Author & Acknowledgments
**Author**: Muhammad Rifqy Irfanto

This project was completed as part of the Purwadhika Data Engineering Bootcamp Module 1 capstone requirement. Special thanks to the instructors and fellow cohort members for their guidance and collaboration.

---
*If you have any questions or feedback about this project, feel free to open an issue or reach out directly.*