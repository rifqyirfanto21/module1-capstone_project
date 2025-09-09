import re
import numpy as np
import pandas as pd

# Function to standardize variation of suffix commonly found in company names
def standardize_suffix(suffix):
    """
    Standardizing the suffix commonly found in company names
    for company column cleaning
    """
    suffix_mapping = {
        'INC': 'Inc', 'inc': 'Inc', 'Inc': 'Inc',
        'LLC': 'LLC', 'llc': 'LLC', 'Llc': 'LLC', 
        'CORP': 'Corp', 'corp': 'Corp', 'Corp': 'Corp',
        'LTD': 'Ltd', 'ltd': 'Ltd', 'Ltd': 'Ltd',
        'CO': 'Co', 'co': 'Co', 'Co': 'Co'
        }
    return suffix_mapping.get(suffix, suffix)

# Function to check the suffix case and the company name case
def company_case_logic(name):
    """
    Handles the suffix and the company name case checking,
    for company column cleaning
    """
    # The reason why we separating the content between name, suffix, 
    # and possible content after suffix is because i found some rows that have content after the suffix. 
    # to preserve that, we will separate it first

    suffix_match = re.search(r'^(.*?)\b(Inc|LLC|Corp|Ltd|Co)\b(.*)$', name, flags=re.IGNORECASE)
    if suffix_match:
        base_name = suffix_match.group(1).strip()
        original_suffix = suffix_match.group(2)
        content_after = suffix_match.group(3).strip()
        standardized_suffix = standardize_suffix(original_suffix)
        
        if base_name.isupper():
            base_name = base_name.title()
        elif base_name.islower():
            base_name = base_name.title()
        
        # after checking one by one, we reconstruct the company name
        result = f"{base_name} {standardized_suffix}"
        if content_after:
            result += f" {content_after}"
        return result
    else:
        if name.isupper():
            return name.title()
        elif name.islower():
            return name.title()
        else:
            return name
        
# Abbreviation mapping for US states
state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

# Function to normalize raw location into a more structured format
def normalize_location(loc):
    """
    Handles normalizing location into city, state, country, and location type
    """
    if "," in loc:  # City, ST format
        city, state_code = loc.split(",", 1)
        return city.strip(), state_code.strip(), "United States", "City"
    elif loc == "Remote":
        return None, None, None, "Remote"
    elif loc == "United States":
        return None, None, "United States", "Country"
    elif loc in state_abbrev:
        return None, state_abbrev[loc], "United States", "State"
    else:
        return None, None, None, "Unknown"

# Function to classify job titles into predefined job families
def detect_job_family(title):
    """
    Handles detecting job family from job title using keyword matching. 
    """
    # After discussing with analyst team, 
    # we agreed to classify those titles into these families for easier analysis

    title = title.lower()
    if "analyst" in title or "analytics" in title or "visualization" in title:
        return "Data Analyst"

    if "science" in title or "scientist" in title:
        return "Data Scientist"

    if "software" in title and "engineer" in title:
        return "Software Engineer"

    if "data center" in title or "infrastructure" in title or "network" in title or "systems" in title or "system" in title or "configuration" in title:
        return "Infrastructure Engineer"

    if "data" in title and "engineer" in title:
        return "Data Engineer"

    return "Other"

def classify_seniority(title):
    """
    Classify job seniority level from job title using keyword matching. 
    I'm using regex here to make sure keyword like 'i' is not matched with a whole word
    """
    title = title.lower()
    if re.search(r"\bmanager\b", title) or re.search(r"\bmgr\b", title):
        return "Manager"
    elif re.search(r"\bprincipal\b", title) or re.search(r"\biv\b", title, re.IGNORECASE) or re.search(r"level\s*4", title):
        return "Principal"
    elif re.search(r"\bstaff\b", title):
        return "Staff"
    elif re.search(r"\bsr\b", title) or re.search(r"\bsenior\b", title) or re.search(r"\biii\b", title, re.IGNORECASE) or re.search(r"level\s*3", title):
        return "Senior"
    elif re.search(r"\blead\b", title):
        return "Lead"
    elif re.search(r"\bassociate\b", title) or re.search(r"\bassoc\b", title):
        return "Associate"
    elif re.search(r"\bjunior\b", title) or re.search(r"\bintern\b", title) or re.search(r"\bi\b", title, re.IGNORECASE) or re.search(r"level\s*1", title):
        return "Junior"
    elif re.search(r"\bmid\b", title) or re.search(r"\bii\b", title, re.IGNORECASE) or re.search(r"level\s*2", title):
        return "Mid"
    else:
        return "Mid"

def split_revenue(val):
    """
    Splitting company revenue column into min and max revenue with numeric format for easier analysis
    """

    if not isinstance(val, str) or pd.isna(val):
        return (np.nan, np.nan)

    nums = re.findall(r"\d+\.?\d*", val)
    nums = [float(n) for n in nums]

    if "Less than" in val:
        return (0, nums[0]*1_000_000)
    elif "billion" in val:
        nums = [n*1_000_000_000 for n in nums]
    elif "million" in val:
        nums = [n*1_000_000 for n in nums]
    
    if len(nums) == 1:
        return (nums[0], np.nan)
    elif len(nums) == 2:
        return (nums[0], nums[1])
    else:
        return (np.nan, np.nan)