# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Yuhu!
    """
)

#1. AÑADIR NOMBRE
name_on_order = st.text_input('Name')
st.write('Name:', name_on_order)


#selección datos dataframe
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#2. SELECCIÓN FRUTAS
ingredients_list = st.multiselect(
    'Choose', my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dtaframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #añadir a la tabla orders
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    #submit button
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")

st.stop()    


