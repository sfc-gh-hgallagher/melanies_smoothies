# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Lab imported
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session() #get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       if fruit_chosen[-1] == 's':
         fruit_chosen = fruit_chosen[0:-1]
       smoothiefroot_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
       sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

