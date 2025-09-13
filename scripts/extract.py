import pandas as pd

# Input File Path
def extract_csv(path):
    """
    Extract data from csv file
    """
    return pd.read_csv(path)