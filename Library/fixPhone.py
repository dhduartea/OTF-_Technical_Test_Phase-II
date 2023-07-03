import pandas as pd
import re

def fixPhoneNumber(df):
    """
    This function takes a dataframe with a column named "phone" and arrange the phone number to have this structure "(+XXX) XXXX XXXXXX" If the value is a np.nan, it returns a np.nan value and if the value is a string, it returns the string with the new structure.
    Args:
        df (pandas.DataFrame): Dataframe with a column named "phone".
    Returns:
        df (pandas.DataFrame): Dataframe with a new column named "phone".
    """

    # Function to arrange the phone number to have this structure "(+XXX) XXXX XXXXXX, where XXX is the country code that can be changed in the function and the rest of the number is the phone number
    def fixPhones(phone,countryCode="+44"):

        # If the value is a np.nan, it returns a np.nan value
        if pd.isna(phone):
            return phone
        # Uses regular expressions to replace the "-"" character with a empty string
        phone=re.sub(r"-","",phone)
        # Uses regular expressions to remove the first 0s from the phone number
        phone=re.sub(r"^0{1,2}(\d+)",lambda x: x.group(1),phone)
        # Uses regular expressions to add a space between the first 4 digits and the rest of the phone number
        phone=re.sub(r"(\d{4})(\d+)",lambda x: (x.group(1) + " " + x.group(2)), phone)
        # Adds the country code to the phone number
        phone="("+countryCode+") " + phone

        return phone

    df["phone"]=df["phone"].apply(fixPhones)
    
    return df