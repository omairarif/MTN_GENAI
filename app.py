import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import pymysql
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

#import ENV
load_dotenv()

#openai_api_key = os.getenv("API_KEY")
#database_url = os.getenv("DATABASE_URL")
#db_user = os.getenv("DATABASE_USER")
#db_pwd = os.getenv("DATABASE_PWD")


openai_api_key = st.secrets["API_KEY"]
database_url = st.secrets["DATABASE_URL"]
db_user = st.secrets["DATABASE_USER"]
db_pwd = st.secrets["DATABASE_PWD"]



print(db_user)
print(db_pwd)
print(database_url)

# Function to convert image to base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the logo image
logo_path = "mtn_logo.png"
logo_base64 = img_to_base64(logo_path)

# Custom CSS to create a yellow bar at the top with the logo and title
st.markdown(
    f"""
    <style>
    .title-bar {{
        background-color: #FFCC00;  /* MTN yellow */
        padding: 10px;
        display: flex;
        align-items: center;
    }}
    .title-bar img {{
        width: 50px;  /* Adjust the width of the logo as needed */
        margin-right: 10px;
    }}
    .title-bar h1 {{
        margin: 0;
        font-size: 24px;
        font-weight: bold;
        color: black;
    }}
    </style>
    <div class="title-bar">
        <img src="data:image/png;base64,{logo_base64}" alt="MTN Logo">
        <h1>MTN Analytics 2.0</h1>
    </div>
    """,
    unsafe_allow_html=True
)






# Create a text input box for the user to enter a prompt
prompt = st.text_input("Ask a question (e.g., 'Show me all customers who made a purchase in the last month')", "")

client = OpenAI(api_key=openai_api_key)
# Generate some text based on the user's input
def generate_text(prompt):
    if prompt:
        # For demonstration, we will just repeat the prompt
        # In a real application, you could call a text generation API or model here
        #return f"You entered: {prompt}. Here is some generated text based on your prompt."
        content_msg = f'''You are a data Enginner resposible for creating an SQL script against a user query. The Managment of MTN will ask a question, and based on that question generate a SQL query that will be run to get an answer. DO NOT OUTPUT ANYTHING BESIDES AN SQL QUERY. The following is the question asked by the managment: {prompt}
        And this is the table defintion:
        
  {{"column_name": "Year", "data_type": "INT", "description": "Year of the data - YYYY"}},
  {{"column_name": "voi_volte_dur", "data_type": "DOUBLE", "description": "Duration of VoLTE call made"}},
  {{"column_name": "voi_volte_cnt", "data_type": "INT", "description": "Number of VoLTE calls made"}},
  {{"column_name": "uid", "data_type": "VARCHAR(255)", "description": "Unique Customer ID"}},
  {{"column_name": "tariff_type", "data_type": "VARCHAR(255)", "description": "Price plan of subscriber"}},
  {{"column_name": "tac", "data_type": "VARCHAR(255)", "description": "First 8 digits of IMEI to identify handset"}},
  {{"column_name": "subtype_mig_exp_amt", "data_type": "DOUBLE", "description": "Wallet expiries amount for subtype migrations"}},
  {{"column_name": "status", "data_type": "VARCHAR(255)", "description": "MSISDN key status"}},
  {{"column_name": "spend_total_mtd", "data_type": "DOUBLE", "description": "Cumulative value of previous metric (spend_total_mtd)"}},
  {{"column_name": "spend_total", "data_type": "DOUBLE", "description": "Calculation of the postpaid & prepaid subscriber total spend"}},
  {{"column_name": "smartphone_ind", "data_type": "TINYINT", "description": "Smartphone indicator"}},
  {{"column_name": "sim_kit_no", "data_type": "VARCHAR(255)", "description": "SIM kit number"}},
  {{"column_name": "rge_modern_cb", "data_type": "TINYINT", "description": "Base indicator to indicate if subscriber is counted on the closing base"}},
  {{"column_name": "rec_create_date", "data_type": "DATE", "description": "Date the record was created in the table"}},
  {{"column_name": "price_plan_ob", "data_type": "VARCHAR(255)", "description": "Price plan OB"}},
  {{"column_name": "price_plan", "data_type": "VARCHAR(255)", "description": "Package code (postpaid) or service class of customer (prepaid)"}},
  {{"column_name": "payment_option", "data_type": "VARCHAR(255)", "description": "Identifies how the subscriber pays by default"}},
  {{"column_name": "opco_name", "data_type": "VARCHAR(255)", "description": "Name of Operation"}},
  {{"column_name": "opco_business_type", "data_type": "VARCHAR(255)", "description": "Type of business operation"}},
  {{"column_name": "nw_3g_ind", "data_type": "TINYINT", "description": "Handset 3G capable"}},
  {{"column_name": "nw_2g_ind", "data_type": "TINYINT", "description": "Handset 2G capable"}},
  {{"column_name": "msisdn_status", "data_type": "VARCHAR(255)", "description": "Status code reflecting the status of a customer"}},
  {{"column_name": "msisdn_key", "data_type": "BIGINT", "description": "Unique identifier for MSISDN"}},
  {{"column_name": "month", "data_type": "TINYINT", "description": "Month of the data - MM"}},
  {{"column_name": "lte_4g_ind", "data_type": "TINYINT", "description": "Handset 4G capable"}},
  {{"column_name": "loy_redeem_last_dt", "data_type": "DATE", "description": "Last date of loyalty redemption"}},
  {{"column_name": "last_activity_date", "data_type": "DATE", "description": "Last activity date for MSISDN"}},
  {{"column_name": "is_volte_prov", "data_type": "TINYINT", "description": "Indicator on whether VoLTE was configured on the MSISDN"}},
  {{"column_name": "is_volte_approved", "data_type": "VARCHAR(255)", "description": "Indicator of whether the device associated with the MSISDN is capable of making VoLTE calls"}},
  {{"column_name": "is_msisdn_base_l3d", "data_type": "TINYINT", "description": "Indicator to keep MSISDNs removed from the base for 3 more days after they are removed"}},
  {{"column_name": "is_msisdn_base", "data_type": "TINYINT", "description": "Determines if the MSISDN is part of the base and active"}},
  {{"column_name": "imsi", "data_type": "VARCHAR(255)", "description": "IMSI Number"}},
  {{"column_name": "imei", "data_type": "VARCHAR(255)", "description": "Last used IMEI number based on the event timestamp"}},
  {{"column_name": "hs_model", "data_type": "VARCHAR(255)", "description": "Handset Model"}},
  {{"column_name": "hs_make", "data_type": "VARCHAR(255)", "description": "Handset Make"}},
  {{"column_name": "grossadd_dt", "data_type": "DATE", "description": "Date the subscriber is considered 'Revenue Generating'"}},
  {{"column_name": "gprs_ind", "data_type": "TINYINT", "description": "Handset GPRS capable"}},
  {{"column_name": "eppix_original_dealer_id", "data_type": "VARCHAR(255)", "description": "Eppix activated dealer code"}},
  {{"column_name": "eppix_dealer_id", "data_type": "VARCHAR(255)", "description": "Eppix last activated/upgraded dealer code"}},
  {{"column_name": "edge_ind", "data_type": "TINYINT", "description": "Handset EDGE capable"}},
  {{"column_name": "dealer_cd_ob", "data_type": "VARCHAR(255)", "description": "Open base dealer code"}},
  {{"column_name": "dealer_cd", "data_type": "VARCHAR(255)", "description": "Identifier of the channel activating/upgrading the subscriber"}},
  {{"column_name": "deal_cd", "data_type": "VARCHAR(255)", "description": "Special deal of the contract"}},
  {{"column_name": "day", "data_type": "TINYINT", "description": "Day of the data - DD"}},
  {{"column_name": "country", "data_type": "VARCHAR(255)", "description": "Country Code of Opco"}},
  {{"column_name": "cons_type", "data_type": "VARCHAR(255)", "description": "Segmentation tagged against a customer"}},
  {{"column_name": "commissionable_activation_date", "data_type": "DATE", "description": "Commissionable activation date"}},
  {{"column_name": "churn_exp_amt", "data_type": "DOUBLE", "description": "Wallet expiries amount for subtype disconnection (churn)"}},
  {{"column_name": "channel_id", "data_type": "VARCHAR(255)", "description": "Code of the channel that sold the SIM"}},
  {{"column_name": "business_day", "data_type": "TINYINT", "description": "Business day"}},
  {{"column_name": "bts_night_site_id", "data_type": "VARCHAR(255)", "description": "Site most used during the night (5pm to 8am)"}},
  {{"column_name": "bts_night_lon", "data_type": "DOUBLE", "description": "BTS Longitude, based on night time most used by Minutes of Use (MoU)"}},
  {{"column_name": "bts_night_lat", "data_type": "DOUBLE", "description": "BTS Latitude, based on night time most used by Minutes of Use (MoU)"}},
  {{"column_name": "bts_mu_site_id", "data_type": "VARCHAR(255)", "description": "Most used cell based on usage"}},
  {{"column_name": "bts_mu_sector_ob_m", "data_type": "VARCHAR(255)", "description": "Sector as at the last day of the previous month"}},
  {{"column_name": "bts_mu_sector_ob", "data_type": "VARCHAR(255)", "description": "Sector of previous day"}},
  {{"column_name": "bts_mu_sector", "data_type": "VARCHAR(255)", "description": "Site sector"}},
  {{"column_name": "bts_mu_lon", "data_type": "DOUBLE", "description": "BTS Longitude, based on most used by Minutes of Use (MoU)"}},
  {{"column_name": "bts_mu_lat", "data_type": "DOUBLE", "description": "BTS Latitude, based on most used by Minutes of Use (MoU)"}},
  {{"column_name": "bts_first_call_site_id", "data_type": "VARCHAR(255)", "description": "Site ID of the first call location"}},
  {{"column_name": "bts_first_call_lon", "data_type": "DOUBLE", "description": "BTS Longitude of first call location"}},
  {{"column_name": "bts_first_call_lat", "data_type": "DOUBLE", "description": "BTS Latitude of first call location"}},
  {{"column_name": "bts_day_site_id", "data_type": "VARCHAR(255)", "description": "Site most used during the day (8am to 5pm)"}},
  {{"column_name": "bts_day_lon", "data_type": "DOUBLE", "description": "BTS Longitude, based on day time most used by Minutes of Use (MoU)"}},
  {{"column_name": "bts_day_lat", "data_type": "DOUBLE", "description": "BTS Latitude, based on day time most used by Minutes of Use (MoU)"}},
  {{"column_name": "bdl_pur_cvm_last_dt", "data_type": "DATE", "description": "Last date of BDL Purchase CVM"}},
  {{"column_name": "b2b_type", "data_type": "VARCHAR(255)", "description": "Identifies whether the MSISDN is B2B or B2C"}},
  {{"column_name": "airtime_da103_exp_amt", "data_type": "DOUBLE", "description": "Wallet expiries amount for DA103"}},
  {{"column_name": "airtime_da3_exp_amt", "data_type": "DOUBLE", "description": "Wallet expiries amount for DA3"}},
  {{"column_name": "adv_last_dt", "data_type": "DATE", "description": "Last date of ADV"}},
  {{"column_name": "active_data_user", "data_type": "TINYINT", "description": "Base indicator to determine if the subscriber is active or not"}},
  {{"column_name": "active_data_user_ob", "data_type": "TINYINT", "description": "Identifies if the subscriber is active based on event data at the end of the previous day"}},
  {{"column_name": "active_data_user_ob_m", "data_type": "TINYINT", "description": "Identifies if the subscriber is active based on event data at the end of the previous month"}},
  {{"column_name": "account_src", "data_type": "VARCHAR(255)", "description": "Source system used to source data"}}

  
The Table is called: Metrics
        '''
        stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",     
               "content": content_msg
              }],
        stream=True,)
        print("TEST TEST TEST TEST")
        a=""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                a= a+ str( (chunk.choices[0].delta.content))
                print(chunk.choices[0].delta.content)
        
        return a        
    else:
        return "Please enter a prompt to get started."
    
    




def query_to_dataframe(connection, query):
    try:
        with connection.cursor() as cursor:
            # Execute the SQL query
            cursor.execute(query)
            # Fetch all the rows
            result = cursor.fetchall()
            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            # Create DataFrame
            df = pd.DataFrame(result, columns=columns)
            return df
    except Exception as e:
            st.error(f"Error: {e}")
    
connection = pymysql.connect(
host=database_url,
user=db_user,
password=db_pwd,
database='sql12713295'
)



if prompt:
    generated_text = generate_text(prompt)
    print(generated_text)
    
    st.write(f"\n\n**SQL QUERY GENERATED:**")
    st.write(generated_text)
    
    
    
    print("REACHER")  
    query = generated_text
    if query.strip() != "":
            # Execute the query and get results
        df = query_to_dataframe(connection, query)
            # Display results in Streamlit table
        st.write(f"\n\n**Data Output:**")   
        st.write(df)
#else:
 #   st.warning("Please enter a SQL query.")

# Display the generated text