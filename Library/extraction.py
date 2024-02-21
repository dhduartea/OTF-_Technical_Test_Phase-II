import pandas as pd
import requests


def contactExtraction(api_key):
    """This function extracts the contacts from the Hubspot API and returns a DataFrame with the contacts
    Args:
        api_key (str): The api key of the Hubspot account
    Returns:
        df (pandas.DataFrame): The DataFrame with the contacts
    """
    #Url of the request in this case, the url of the contacts
    url = 'https://api.hubapi.com/crm/v3/objects/contacts/search'
    #Headers of the request
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': 'Bearer {}'.format(api_key)
    }
    #Limit of the request in order to get through all the contacts
    limit = 100
    #Value to start the request
    after = 0 
    #List to store the DataFrames
    dfs = [] 

    #Flag to check if there are more contacts
    results,next_page=1,1

    #Properties to get from the contacts
    properties = [
        'raw_email',
        'country',
        'phone',
        'technical_test___create_date',
        'industry',
        'address',
        'hs_object_id',
    ]
    #Columns created by default to delete from the DataFrame
    delCol=['id',
        'createdAt',
        'updatedAt',
        'archived',
        'properties.createdate',
        'properties.lastmodifieddate'
    ]
    #Data of the request
    data = {
        "properties": properties,
        #Filter to get only the contacts that are allowed to collect
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "allowed_to_collect",
                        "operator": "EQ",
                        "value": "true"
                    }
                ]
            }
        ],
        #After value to get the next contacts
        "after": str(after),
        "limit": limit
    }

    #Loop over the contacts
    while results and next_page:
        

        #Request to the API
        response = requests.post(url, headers=headers, json=data)
        #Get the data from the request
        data = response.json()

        #If 'results' is in the data, get the results
        if 'results' in data:
            results = data['results']
            #Get the DataFrame from the results
            df = pd.json_normalize(results)  
            #Delete the columns that are not needed
            for col in delCol:
                del df[col]
            #Rename the columns
            for property in properties:
                df.rename(columns={'properties.'+property: property}, inplace=True)
            #Add the DataFrame to the list
            dfs.append(df)
        else:
            break
        
        #If 'paging' is in the data, get the next page
        if 'paging' in data:
            paging = data['paging']
            #Get the next page 
            next_page = paging.get('next')
            #If there is a next page, get the after value
            if next_page:
                after = next_page.get('after')
            else:
                break
        else:
            break
    #Concatenate all the DataFrames to get the final DataFrame
    df_final = pd.concat(dfs, ignore_index=True)

    #Return the final DataFrame
    return df_final
