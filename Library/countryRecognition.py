import pandas as pd
import numpy as np


def recognition(df):
    """ 
    This function takes a dataframe with a column named "country" and recognizes in the value on this cell is a city or a country. If it is a city, it returns a tuple with the country and the city. If it is a country, it returns a tuple with the country and an empty string. If the country is not in the dictionary, it returns a np.nan value.
    
    Args:
        df (pandas.DataFrame): Dataframe with a column named "country".
    Returns:
        df (pandas.DataFrame): Dataframe with two new columns name "city" and "countryTuple".

    """
    # Dictionary with countries and cities(The dictionary could be replace with a database with the whole amount of countries and cities)
    citiesDict={
    "England": ["London", 
            "Winchester", 
            "Milton Keynes", 
            "Oxford", 
            "Plymouth",], 
    "Ireland": ["Waterford", 
            "Dublin", 
            "Limerick", 
            "Cork",],
    }
    # List with all the cities
    cities=[value for values in citiesDict.values() for value in values]

    # Function to recognize if the value is a city or a country and return the country or a np.nan value
    def countryDiscrimination(country):
        if country in citiesDict.keys():
            return country
        elif country in cities:
            for key, value in citiesDict.items():
                if country in value:
                    return key
        else:
            return np.nan
    # Function to recognize if the value is a city or a country and return the city or a np.nan value
    def citiesDiscrimination(city):
        if city in cities:
            return city
        else:
            return np.nan

    # Apply the function to the column "country" and create a new column named "city"
    df["city"]=df["country"].apply(citiesDiscrimination)
    # Apply the function to the column "country" and replace the values in the column "country" with the country
    df["country"]=df["country"].apply(countryDiscrimination)

    # Create a new column named "countryTuple" with a tuple with the country and the city
    df["countryTuple"]=df.apply(lambda x: tuple([x["country"], x["city"]] if x["country"]!=np.nan else np.nan), axis=1)

    return df




