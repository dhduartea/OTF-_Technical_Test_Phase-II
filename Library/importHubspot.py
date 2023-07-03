import requests
import pandas as pd


def importContacts(df,api_key):
    """
    This function imports the contacts to Hubspot from a DataFrame with the contacts and returns a message if the contacts were uploaded successfully. The loading time depends on the number of contacts, in this case, it takes around 40 seconds to upload 100 contacts to Hubspot, so if you are going to upload a great number of contacts, it is going to take a while.
    Args:
        df (pandas.DataFrame): The DataFrame with the contacts
        api_key (str): The api key of the Hubspot account
    Returns:
        str: A message if the contacts were uploaded successfully
    """
    
    #This is the url to import the contacts to Hubspot
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    #In order to avoid an error for uploading a NaN value, we fill the NaN values with "None"
    df['city'] = df['city'].fillna("None")
    #Headers of the request
    headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': 'Bearer {}'.format(api_key)
        }
    #Loop over the DataFrame
    for index, row in df.iterrows():
        #Body of the request
        body= {
            "properties": {
                "email": row['raw_email'],
                "phone": row['phone'],
                "country": row['country'],
                "city": row['city'],
                "original_create_date": row['technical_test___create_date'],
                "original_industry": row['industry'],
                "temporary_id": row['hs_object_id'],
                "address": row['address']
            }
        } 
        #Request to upload the contacts
        requests.request('POST', url, headers = headers, json = body)
    
    return "Contacts uploaded successfully"
