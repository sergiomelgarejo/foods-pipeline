import pandas as pd
from etl import *


class ETL:
    data = []
    engine = create_engine()
    df_foods = pd.DataFrame()
    df_nutrients = pd.DataFrame()

    @classmethod
    def extract(cls):
        """
        Returns a multi-dimentional array of all foods data requested to the API.
        """
        pages = get_totalpage()
        cls.data = []

        for page in range(1, 10):
        # for page in range(1, pages): #!!!! uncomment in production
            foods = get_foods_pp(page)
            cls.data.append(foods)

        return data
    
    @staticmethod
    def transform(data):
        """
        Creates two DataFrames, one for foods object and another for the nutrients object.
        Also it creates the relationship between the foods and nutrients objects by 'fdcId'.
        """
        foods = tranform_foods_list(data)

        data_foods = []
        data_nutrients = []
        data_foodnutrients = []

        for food in foods:
            ft = t_foods(food)
            data_foods.append(ft)

            nutrients = food['foodNutrients']
            for nutrient in nutrients:
                nt = t_nutrients(nutrient)
                nt['fdcId'] = ft['fdcId']
                data_nutrients.append(nt) 

            df_foodnutrients = pd.DataFrame(data=data_nutrients)
            data_foodnutrients.append(df_foodnutrients)

        df_foods = pd.DataFrame(data=data_foods)
        df_nutrients = pd.concat(data_foodnutrients, ignore_index=True)

        return df_foods, df_nutrients

    @classmethod
    def load(cls, id, schema='STG'):
        if id == 'f':
            data = cls.df_foods
            table = 'foods'
        elif id == 'n':
            data = cls.df_nutrients
            table = 'nutrients'
        else:
            raise ValueError(f'Incorrect id: {id}. id must be "f" or "n".')
            
        print('Loading data...')
        try:
            data.to_sql(table, cls.engine, schema=schema, if_exists='replace')
        except Exception as e:
            raise Exception(f'Error while loading the data into {schema}.{table}. {e}')
