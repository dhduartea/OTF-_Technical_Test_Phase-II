
import pandas as pd
import numpy as np


df=pd.read_csv('df.csv',sep=',')

def duplicatesManage(df):
    """
    This function takes a dataframe and returns a dataframe without duplicates. The function keeps the last entry of each email and concatenates the industry column. It also keeps the first entry of the phone and address column.
    Args:
        df (pandas.DataFrame): Dataframe with the main column named "raw_email" along with the columns "industry", "phone","address" among others.
    Returns:
        dfcopy (pandas.DataFrame): Dataframe without duplicates.
    """

    dfcopy=df.copy()
    # Sort the dataframe by email and date
    dfcopy.sort_values(["raw_email","technical_test___create_date",], ascending=[True,False], inplace=True)

    # Concatenate the industry column for the values with the same email
    dfcopy['industry'] = dfcopy.groupby('raw_email')['industry'].transform(lambda x: ';'.join(np.unique(x.dropna())))

    # Add a ";" to the beginning of the string if it the string contains a ";" (it means that the string has more than one industry)
    dfcopy['industry'] = dfcopy['industry'].apply(lambda x: ";"+x if ";" in x else x)

    # Extract the first country for the values with the same email
    dfcopy['country'] = dfcopy.groupby('raw_email')['country'].transform(lambda x: list(dict.fromkeys(x.dropna()))[0])

    # Extract the first phone number for the values with the same email
    dfcopy['phone'] = dfcopy.groupby('raw_email')['phone'].transform(lambda x: list(dict.fromkeys(x.dropna()))[0])

    # Extract the first address for the values with the same email
    dfcopy['address'] = dfcopy.groupby('raw_email')['address'].transform(lambda x: list(dict.fromkeys(x.dropna()))[0])

    # Drop the duplicates keeping the first entry of each email
    dfcopy.drop_duplicates(subset=['raw_email'], keep='first', inplace=True)
    
    dfcopy.reset_index(drop=True, inplace=True)

    return dfcopy
