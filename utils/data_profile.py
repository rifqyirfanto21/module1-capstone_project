def data_demographi(df, exclude_columns=None):
    """
    Generate data demographi/profiling for the given tables
    """
    # adding exclude columns parameter because some categorical columns are too long
    # for example: job_description column from data_requirements table
    if exclude_columns is None:
        exclude_columns = []

    print("Row count:", len(df))
    print("Column count:", len(df.columns))
    
    print("\nMissing values per column:")
    print(df.isna().sum())
    
    print("\nUnique values per column:")
    print(df.nunique())
    
    print("\nTop 5 most frequent values per categorical column:")
    for col in df.select_dtypes(include="object").columns:
        if col not in exclude_columns:
            print(f"\nColumn: {col}")
            print(df[col].value_counts().head(5))
