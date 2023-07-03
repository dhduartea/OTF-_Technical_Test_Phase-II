import pandas as pd
import re

def emailExtraction(df):
    """
    This function takes a dataframe with a column named "raw_email" and extracts the email from the string. If the value is a np.nan, it returns a np.nan value.
    Args:
        df (pandas.DataFrame): Dataframe with a column named "raw_email".
    Returns:
        df (pandas.DataFrame): Dataframe with a new column named "raw_email".
    """
    # Function to extract the email from the string
    def extractEmail(email):
        # If the value is a np.nan, it returns a np.nan value
        if pd.isna(email):
            return email
        # Uses regular expressions to extract the email where the email is between "<" and ">"
        return re.sub(r".+<(.+)>.+",lambda x: x.group(1),email)
    # Apply the function to the column "raw_email"
    df["raw_email"]=df["raw_email"].apply(extractEmail)

    return df