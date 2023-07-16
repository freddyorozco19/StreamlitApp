# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 03:14:41 2023
Modified on 11/07/2023 version 1.0

@author: Freddy J. Orozco R.
Powered: Win Stats LATAM
"""

import streamlit as st
import hydralit_components as hc
import datetime
import base64
import pandas as pd
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from radar_chart2 import Radar
import altair as alt

############################################################################################################################################################################################################################

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def colorlist(color1, color2, num):
    """Generate list of num colors blending from color1 to color2"""
    result = [np.array(color1), np.array(color2)]
    while len(result) < num:
        temp = [result[0]]
        for i in range(len(result)-1):
            temp.append(np.sqrt((result[i]**2+result[i+1]**2)/2))
            temp.append(result[i+1])
        result = temp
    indices = np.linspace(0, len(result)-1, num).round().astype(int)
    return [result[i] for i in indices] 


#####################################################################################################################################################

font_path = 'Resources/keymer-bold.otf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop2 = font_manager.FontProperties(fname=font_path)

font_path2 = 'Resources/BasierCircle-Italic.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path2)
prop3 = font_manager.FontProperties(fname=font_path2)

#####################################################################################################################################################


###########################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

#make it look nice from the start
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
    }
   .sidebar .sidebar-content {
        background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
# specify the primary menu definition
menu_data = [
    {'id': "AllMetrics", 'label':"Metrics"},
    {'id': "ExtractData", 'label':"Extract Data"},
    {'id': "PlayerStats", 'label':"Player Stats"},
    {'id': "SimilarityTool", 'label':"Similarity Tool"}
]
over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    login_name='Logout',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

if menu_id == "AllMetrics":
    with st.sidebar:
        with open("Resources/win.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                    <img src="data:image/png;base64,{data}" width="300">
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("""---""")    
        
        with st.form(key='form'):
            
            #Table = st.file_uploader("Choose a excel file", type = ['xlsx'], accept_multiple_files=False)
            
            Table = st.file_uploader("Cargar archivo:", type="xlsx")


            Filename = st.text_input("Nombre del Archivo:",
                                      key="filename"
                                      )   

            Matchday = st.text_input("Jornadas Disputadas:",
                                    key="matchday"
                                    )   

            Competition = st.text_input("Competición:",
                                     key="competition"
                                     )   

            Date = st.text_input("Fecha de Registro:",
                                          key="date"
                                          )   
            
            submit_button = st.form_submit_button(label='Aceptar')  
     
            
    #df = pd.read_excel(Table)

    if Table is not None:
        df = pd.read_excel(Table)
        
        
    ###
    
    df.insert(8, '90s', df['Minutes played']/90)
    df['90s'] = df['90s'].apply(lambda x: round(x, 2))
    dfinf = df[['Market value', 'Team within selected timeframe', 'Contract expires', 'Birth country', 'Passport country', 'Foot', 'Height', 'Weight', 'On loan']]
    df = df.drop(['Market value', 'Team within selected timeframe', 'Contract expires', 'Birth country', 'Passport country', 'Foot', 'Height', 'Weight', 'On loan'],axis=1)
    #####
    df.insert(11, 'Total duels', df['Duels per 90']*df['90s'])
    df.insert(14, 'Total duels won', (df['Total duels']*df['Duels won, %'])/100)
    df.insert(15, 'Duels won per 90', df['Total duels won']/df['90s'])
    df.insert(16, 'Total successful defensive actions', df['Successful defensive actions per 90']*df['90s'])
    df.insert(18, 'Total defensive duels', df['Defensive duels per 90']*df['90s'])
    df.insert(21, 'Total defensive duels won', (df['Total defensive duels']*df['Defensive duels won, %'])/100)
    df.insert(22, 'Defensive duels won per 90', df['Total defensive duels won']/df['90s'])
    df.insert(23, 'Total aerial duels', df['Aerial duels per 90']*df['90s'])
    df.insert(26, 'Total aerial duels won', (df['Total aerial duels']*df['Aerial duels won, %'])/100)
    df.insert(27, 'Aerial duels won per 90', df['Total aerial duels won']/df['90s'])
    #####
    df.insert(28, 'Total sliding tackles', df['Sliding tackles per 90']*df['90s'])
    df.insert(31, 'Total shots blocked', df['Shots blocked per 90']*df['90s'])
    df.insert(33, 'Total interceptions', df['Interceptions per 90']*df['90s'])
    df.insert(36, 'Total fouls', df['Fouls per 90']*df['90s'])
    #####
    df.insert(42, 'Total successful attacking actions', df['Successful attacking actions per 90']*df['90s'])
    df.insert(50, 'Total shots', df['Shots per 90']*df['90s'])
    df.insert(54, 'Total shots on target', (df['Total shots']*df['Shots on target, %'])/100)
    df.insert(55, 'Shots on target per 90', df['Total shots on target']/df['90s'])
    df.insert(57, 'PENxG', df['Penalties taken']*0.76)
    df.insert(58, 'Converted penalties', (df['Penalties taken']*df['Penalty conversion, %'])/100)
    df.insert(45, 'NPxG', df['xG']-df['PENxG'])
    df.insert(46, 'NPxG per 90', df['NPxG']/df['90s'])
    #####
    df.insert(62, 'Total crosses', df['Crosses per 90']*df['90s'])
    df.insert(65, 'Total crosses completed', (df['Total crosses']*df['Accurate crosses, %'])/100)
    df.insert(66, 'Crosses completed per 90', df['Total crosses completed']/df['90s'])
    df.insert(71, 'Total crosses to goalie box', df['Crosses to goalie box per 90']*df['90s'])
    #####
    df.insert(73, 'Total dribbles', df['Dribbles per 90']*df['90s'])
    df.insert(76, 'Total successful dribbles', (df['Total dribbles']*df['Successful dribbles, %'])/100)
    df.insert(77, 'Successful dribbles per 90', df['Total successful dribbles']/df['90s'])
    df.insert(78, 'Total offensive duels', df['Offensive duels per 90']*df['90s'])
    df.insert(81, 'Total offensive duels won', (df['Total offensive duels']*df['Offensive duels won, %'])/100)
    df.insert(82, 'Offensive duels won per 90', df['Total offensive duels won']/df['90s'])
    df.insert(83, 'Total touches in box', df['Touches in box per 90']*df['90s'])
    df.insert(85, 'Total progressive runs', df['Progressive runs per 90']*df['90s'])
    df.insert(87, 'Total accelerations', df['Accelerations per 90']*df['90s'])
    df.insert(89, 'Total received passes', df['Received passes per 90']*df['90s'])
    df.insert(91, 'Total received long passes', df['Received long passes per 90']*df['90s'])
    df.insert(93, 'Total fouls suffered', df['Fouls suffered per 90']*df['90s'])
    #####
    df.insert(95, 'Total passes', df['Passes per 90']*df['90s'])
    df.insert(98, 'Total passes completed', (df['Total passes']*df['Accurate passes, %'])/100)
    df.insert(99, 'Passes completed per 90', df['Total passes completed']/df['90s'])
    df.insert(100, 'Total forward passes', df['Forward passes per 90']*df['90s'])
    df.insert(103, 'Total forward passes completed', (df['Total forward passes']*df['Accurate forward passes, %'])/100)
    df.insert(104, 'Forward passes completed per 90', df['Total forward passes completed']/df['90s'])
    df.insert(105, 'Total back passes', df['Back passes per 90']*df['90s'])
    df.insert(108, 'Total back passes completed', (df['Total back passes']*df['Accurate back passes, %'])/100)
    df.insert(109, 'Back passes completed per 90', df['Total back passes completed']/df['90s'])
    df.insert(110, 'Total lateral passes', df['Lateral passes per 90']*df['90s'])
    df.insert(113, 'Total lateral passes completed', (df['Total lateral passes']*df['Accurate lateral passes, %'])/100)
    df.insert(114, 'Lateral passes completed per 90', df['Total lateral passes completed']/df['90s'])
    df.insert(115, 'Total short / medium passes', df['Short / medium passes per 90']*df['90s'])
    df.insert(118, 'Total short / medium passes completed', (df['Total short / medium passes']*df['Accurate short / medium passes, %'])/100)
    df.insert(119, 'Short / medium passes completed per 90', df['Total short / medium passes completed']/df['90s'])
    df.insert(120, 'Total long passes', df['Long passes per 90']*df['90s'])
    df.insert(123, 'Total long passes completed', (df['Total long passes']*df['Accurate long passes, %'])/100)
    df.insert(124, 'Long passes completed per 90', df['Total long passes completed']/df['90s'])
    #####
    df.insert(128, 'Total shot assists', df['Shot assists per 90']*df['90s'])
    df.insert(130, 'Total second assists', df['Second assists per 90']*df['90s'])
    df.insert(132, 'Total third assists', df['Third assists per 90']*df['90s'])
    df.insert(136, 'Total key passes', df['Key passes per 90']*df['90s'])
    df.insert(134, 'Total smart passes', df['Smart passes per 90']*df['90s'])
    df.insert(137, 'Total smart passes completed', (df['Total smart passes']*df['Accurate smart passes, %'])/100)
    df.insert(138, 'Smart passes completed per 90', df['Total smart passes completed']/df['90s'])
    df.insert(141, 'Total passes to final third', df['Passes to final third per 90']*df['90s'])
    df.insert(144, 'Total passes to final third completed', (df['Total passes to final third']*df['Accurate passes to final third, %'])/100)
    df.insert(145, 'Passes to final third completed per 90', df['Total passes to final third completed']/df['90s'])
    df.insert(146, 'Total passes to penalty area', df['Passes to final third per 90']*df['90s'])
    df.insert(149, 'Total passes to penalty area completed', (df['Total passes to penalty area']*df['Accurate passes to penalty area, %'])/100)
    df.insert(150, 'Passes to penalty area completed per 90', df['Total passes to penalty area completed']/df['90s'])
    df.insert(151, 'Total through passes', df['Through passes per 90']*df['90s'])
    df.insert(154, 'Total through passes completed', (df['Total through passes']*df['Accurate through passes, %'])/100)
    df.insert(155, 'Through passes completed per 90', df['Total through passes completed']/df['90s'])
    df.insert(156, 'Total deep completions', df['Deep completions per 90']*df['90s'])
    df.insert(158, 'Total deep completed crosses', df['Deep completed crosses per 90']*df['90s'])
    df.insert(160, 'Total progressive passes', df['Progressive passes per 90']*df['90s'])
    df.insert(163, 'Total progressive passes completed', (df['Total progressive passes']*df['Accurate progressive passes, %'])/100)
    df.insert(164, 'Progressive passes completed per 90', df['Total progressive passes completed']/df['90s'])
    
    decimals = 0    
    df['Total smart passes'] = df['Total smart passes'].apply(lambda x: round(x, decimals))
    df['Total passes to final third'] = df['Total passes to final third'].apply(lambda x: round(x, decimals))
    df['Total passes to penalty area'] = df['Total passes to penalty area'].apply(lambda x: round(x, decimals))
    df['Total through passes'] = df['Total through passes'].apply(lambda x: round(x, decimals))
    df['Total progressive passes'] = df['Total progressive passes'].apply(lambda x: round(x, decimals))
    df['Total deep completions'] = df['Total deep completions'].apply(lambda x: round(x, decimals))
    df['Total smart passes completed'] = df['Total smart passes completed'].apply(lambda x: round(x, decimals))
    df['Total passes to final third completed'] = df['Total passes to final third completed'].apply(lambda x: round(x, decimals))
    df['Total passes to penalty area completed'] = df['Total passes to penalty area completed'].apply(lambda x: round(x, decimals))
    df['Total through passes completed'] = df['Total through passes completed'].apply(lambda x: round(x, decimals))
    df['Total progressive passes completed'] = df['Total progressive passes completed'].apply(lambda x: round(x, decimals))
    df['Total deep completed crosses'] = df['Total deep completed crosses'].apply(lambda x: round(x, decimals))
    df['Total passes'] = df['Total passes'].apply(lambda x: round(x, decimals))
    df['Total forward passes'] = df['Total forward passes'].apply(lambda x: round(x, decimals))
    df['Total back passes'] = df['Total back passes'].apply(lambda x: round(x, decimals))
    df['Total lateral passes'] = df['Total lateral passes'].apply(lambda x: round(x, decimals))
    df['Total long passes'] = df['Total long passes'].apply(lambda x: round(x, decimals))
    df['Total short / medium passes'] = df['Total short / medium passes'].apply(lambda x: round(x, decimals))
    df['Total short / medium passes completed'] = df['Total short / medium passes completed'].apply(lambda x: round(x, decimals))
    df['Total passes completed'] = df['Total passes completed'].apply(lambda x: round(x, decimals))
    df['Total forward passes completed'] = df['Total forward passes completed'].apply(lambda x: round(x, decimals))
    df['Total back passes completed'] = df['Total back passes completed'].apply(lambda x: round(x, decimals))
    df['Total lateral passes completed'] = df['Total lateral passes completed'].apply(lambda x: round(x, decimals))
    df['Total long passes completed'] = df['Total long passes completed'].apply(lambda x: round(x, decimals))
    df['Total dribbles'] = df['Total dribbles'].apply(lambda x: round(x, decimals))
    df['Total duels'] = df['Total duels'].apply(lambda x: round(x, decimals))
    df['Total aerial duels'] = df['Total aerial duels'].apply(lambda x: round(x, decimals))
    df['Total successful dribbles'] = df['Total successful dribbles'].apply(lambda x: round(x, decimals))
    df['Total duels won'] = df['Total duels won'].apply(lambda x: round(x, decimals))
    df['Total aerial duels won'] = df['Total aerial duels won'].apply(lambda x: round(x, decimals))
    df['Total successful attacking actions'] = df['Total successful attacking actions'].apply(lambda x: round(x, decimals))
    df['Total offensive duels'] = df['Total offensive duels'].apply(lambda x: round(x, decimals))
    df['Total offensive duels won'] = df['Total offensive duels won'].apply(lambda x: round(x, decimals))
    df['Total touches in box'] = df['Total touches in box'].apply(lambda x: round(x, decimals))
    df['Total progressive runs'] = df['Total progressive runs'].apply(lambda x: round(x, decimals))
    df['Total accelerations'] = df['Total accelerations'].apply(lambda x: round(x, decimals))
    df['Total received passes'] = df['Total received passes'].apply(lambda x: round(x, decimals))
    df['Total received long passes'] = df['Total received long passes'].apply(lambda x: round(x, decimals))
    df['Total fouls suffered'] = df['Total fouls suffered'].apply(lambda x: round(x, decimals))
    df['Total crosses'] = df['Total crosses'].apply(lambda x: round(x, decimals))
    df['Total crosses completed'] = df['Total crosses completed'].apply(lambda x: round(x, decimals))
    df['Total shot assists'] = df['Total shot assists'].apply(lambda x: round(x, decimals))
    df['Total second assists'] = df['Total second assists'].apply(lambda x: round(x, decimals))
    df['Total third assists'] = df['Total third assists'].apply(lambda x: round(x, decimals))
    df['Total key passes'] = df['Total key passes'].apply(lambda x: round(x, decimals))
    df['Total shots'] = df['Total shots'].apply(lambda x: round(x, decimals))
    df['Total shots on target'] = df['Total shots on target'].apply(lambda x: round(x, decimals))
    df['Converted penalties'] = df['Converted penalties'].apply(lambda x: round(x, decimals))
    df['Total successful defensive actions'] = df['Total successful defensive actions'].apply(lambda x: round(x, decimals))
    df['Total defensive duels'] = df['Total defensive duels'].apply(lambda x: round(x, decimals))
    df['Total defensive duels won'] = df['Total defensive duels won'].apply(lambda x: round(x, decimals))
    df['Total fouls'] = df['Total fouls'].apply(lambda x: round(x, decimals))
    df['Total sliding tackles'] = df['Total sliding tackles'].apply(lambda x: round(x, decimals))
    df['Total shots blocked'] = df['Total shots blocked'].apply(lambda x: round(x, decimals))
    df['Total interceptions'] = df['Total interceptions'].apply(lambda x: round(x, decimals))
    
    decimals1 = 2
    df['Defensive duels won per 90'] = df['Defensive duels won per 90'].apply(lambda x: round(x, decimals1))
    df['Goal conversion, %'] = df['Goal conversion, %'].apply(lambda x: round(x, decimals1))
    df['Shots on target per 90'] = df['Shots on target per 90'].apply(lambda x: round(x, decimals1))
    df['NPxG per 90'] = df['NPxG per 90'].apply(lambda x: round(x, decimals1))
    df['Crosses completed per 90'] = df['Crosses completed per 90'].apply(lambda x: round(x, decimals1))
    df['Successful dribbles per 90'] = df['Successful dribbles per 90'].apply(lambda x: round(x, decimals1))
    df['Duels won per 90'] = df['Duels won per 90'].apply(lambda x: round(x, decimals1))
    df['Aerial duels won per 90'] = df['Aerial duels won per 90'].apply(lambda x: round(x, decimals1))
    df['Offensive duels won per 90'] = df['Offensive duels won per 90'].apply(lambda x: round(x, decimals1))
    df['Passes completed per 90'] = df['Passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Forward passes completed per 90'] = df['Forward passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Back passes completed per 90'] = df['Back passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Lateral passes completed per 90'] = df['Lateral passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Long passes completed per 90'] = df['Long passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Short / medium passes completed per 90'] = df['Short / medium passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Smart passes completed per 90'] = df['Smart passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Passes to final third completed per 90'] = df['Passes to final third completed per 90'].apply(lambda x: round(x, decimals1))
    df['Passes to penalty area completed per 90'] = df['Passes to penalty area completed per 90'].apply(lambda x: round(x, decimals1))
    df['Through passes completed per 90'] = df['Through passes completed per 90'].apply(lambda x: round(x, decimals1))
    df['Progressive passes completed per 90'] = df['Progressive passes completed per 90'].apply(lambda x: round(x, decimals1))
    
    df = df.fillna(0)

    df['Total successful defensive actions'] = df['Total successful defensive actions'].astype(np.int64)
    df['Total defensive duels'] = df['Total defensive duels'].astype(np.int64)
    df['Total defensive duels won'] = df['Total defensive duels won'].astype(np.int64)
    df['Total sliding tackles'] = df['Total sliding tackles'].astype(np.int64)
    df['Total interceptions'] = df['Total interceptions'].astype(np.int64)
    df['Total shots blocked'] = df['Total shots blocked'].astype(np.int64)
    df['Total successful attacking actions'] = df['Total successful attacking actions'].astype(np.int64)
    df['Total shots on target'] = df['Total shots on target'].astype(np.int64)
    df['Total offensive duels'] = df['Total offensive duels'].astype(np.int64)
    df['Total offensive duels won'] = df['Total offensive duels won'].astype(np.int64)
    df['Total touches in box'] = df['Total touches in box'].astype(np.int64)
    df['Goals'] = df['Goals'].astype(np.int64)
    df['Total crosses'] = df['Total crosses'].astype(np.int64)
    df['Total crosses completed'] = df['Total crosses completed'].astype(np.int64)
    df['Total crosses to goalie box'] = df['Total crosses to goalie box'].astype(np.int64)
    df['Total shot assists'] = df['Total shot assists'].astype(np.int64)
    df['Total second assists'] = df['Total second assists'].astype(np.int64)
    df['Total third assists'] = df['Total third assists'].astype(np.int64)
    df['Total smart passes'] = df['Total smart passes'].astype(np.int64)
    df['Total smart passes completed'] = df['Total smart passes completed'].astype(np.int64)
    df['Total key passes'] = df['Total key passes'].astype(np.int64)
    df['Total passes to penalty area'] = df['Total passes to penalty area'].astype(np.int64)
    df['Total passes to penalty area completed'] = df['Total passes to penalty area completed'].astype(np.int64)
    df['Total through passes'] = df['Total through passes'].astype(np.int64)
    df['Total through passes completed'] = df['Total through passes completed'].astype(np.int64)
    df['Total deep completions'] = df['Total deep completions'].astype(np.int64)
    df['Total deep completed crosses'] = df['Total deep completed crosses'].astype(np.int64)
    df['Total passes'] = df['Total passes'].astype(np.int64)
    df['Total passes completed'] = df['Total passes completed'].astype(np.int64)
    df['Total forward passes'] = df['Total forward passes'].astype(np.int64)
    df['Total forward passes completed'] = df['Total forward passes completed'].astype(np.int64)
    df['Total back passes'] = df['Total back passes'].astype(np.int64)
    df['Total back passes completed'] = df['Total back passes completed'].astype(np.int64)
    df['Total lateral passes'] = df['Total lateral passes'].astype(np.int64)
    df['Total lateral passes completed'] = df['Total lateral passes completed'].astype(np.int64)
    df['Total short / medium passes'] = df['Total short / medium passes'].astype(np.int64)
    df['Total short / medium passes completed'] = df['Total short / medium passes completed'].astype(np.int64)
    df['Total long passes'] = df['Total long passes'].astype(np.int64)
    df['Total long passes completed'] = df['Total long passes completed'].astype(np.int64)
    df['Total passes to final third'] = df['Total passes to final third'].astype(np.int64)
    df['Total passes to final third completed'] = df['Total passes to final third completed'].astype(np.int64)
    df['Total progressive passes'] = df['Total progressive passes'].astype(np.int64)
    df['Total duels'] = df['Total duels'].astype(np.int64)
    df['Total duels won'] = df['Total duels won'].astype(np.int64)
    df['Total aerial duels'] = df['Total aerial duels'].astype(np.int64)
    df['Total aerial duels won'] = df['Total aerial duels won'].astype(np.int64)
    df['Total fouls'] = df['Total fouls'].astype(np.int64)
    df['Total dribbles'] = df['Total dribbles'].astype(np.int64)
    df['Total successful dribbles'] = df['Total successful dribbles'].astype(np.int64)
    df['Total progressive runs'] = df['Total progressive runs'].astype(np.int64)
    df['Total accelerations'] = df['Total accelerations'].astype(np.int64)
    df['Total received passes'] = df['Total received passes'].astype(np.int64)
    df['Total received long passes'] = df['Total received long passes'].astype(np.int64)
    df['Total fouls suffered'] = df['Total fouls suffered'].astype(np.int64)
    df['Penalty conversion, %'] = df['Penalty conversion, %'].astype(np.float64)
    df['Age'] = df['Age'].astype(np.int64)
    df['Matches played'] = df['Matches played'].astype(np.int64)
    df['Minutes played'] = df['Minutes played'].astype(np.int64)
    
    dfaux = df[['Player', 'Team']]
    df = df.rename(columns={"Position":"Pos0"})
    dfposaux = df[['Pos0']]
    dfx = df["Pos0"].str.split(",", expand = True)
    dfx.columns = ['Pos1', 'Pos2', 'Pos3']
    
    dfx["Pos1"] = dfx["Pos1"].replace(['LDMF', 'DMF', 'RDMF'],['CEM','CEM','CEM'])
    dfx["Pos1"] = dfx["Pos1"].replace(['LCMF', 'CMF', 'RCMF', 'LCMF3', 'RCMF3'],['MED','MED','MED','MED','MED'])
    dfx["Pos1"] = dfx["Pos1"].replace(['LAMF', 'AMF', 'RAMF'],['VOL', 'MCO','VOL'])
    dfx["Pos1"] = dfx["Pos1"].replace(['RCB', 'CB', 'LCB', 'RCB3', 'LCB3', 'GK'],['DEF', 'DEF', 'DEF', 'DEF', 'DEF', 'POR'])
    dfx["Pos1"] = dfx["Pos1"].replace(['RB', 'RWB', 'LB', 'LWB', 'RB5', 'LB5'],['LAT', 'LAT', 'LAT', 'LAT', 'LAT', 'LAT'])
    dfx["Pos1"] = dfx["Pos1"].replace(['RW', 'LW'],['EXT', 'EXT'])
    dfx["Pos1"] = dfx["Pos1"].replace(['RWF', 'LWF'],['EXT', 'EXT'])
    dfx["Pos1"] = dfx["Pos1"].replace(['CF'],['DEL'])
    
    dfx["Pos2"] = dfx["Pos2"].replace(['LDMF', 'DMF', 'RDMF'],['CEM','CEM','CEM'])
    dfx["Pos2"] = dfx["Pos2"].replace(['LCMF', 'CMF', 'RCMF', 'LCMF3', 'RCMF3'],['MED','MED','MED','MED','MED'])
    dfx["Pos2"] = dfx["Pos2"].replace(['LAMF', 'AMF', 'RAMF'],['VOL', 'MCO','VOL'])
    dfx["Pos2"] = dfx["Pos2"].replace(['RCB', 'CB', 'LCB', 'RCB3', 'LCB3', 'GK'],['DEF', 'DEF', 'DEF', 'DEF', 'DEF', 'POR'])
    dfx["Pos2"] = dfx["Pos2"].replace(['RB', 'RWB', 'LB', 'LWB', 'RB5', 'LB5'],['LAT', 'LAT', 'LAT', 'LAT', 'LAT', 'LAT'])
    dfx["Pos2"] = dfx["Pos2"].replace(['RW', 'LW'],['EXT', 'EXT'])
    dfx["Pos2"] = dfx["Pos2"].replace(['RWF', 'LWF'],['EXT', 'EXT'])
    dfx["Pos2"] = dfx["Pos2"].replace(['CF'],['DEL'])
    
    #dfx = dfx.drop(['Pos3'], axis=1)
    
    dfc = df.drop(["Player", "Team", "Pos0"], axis=1)
    df = pd.concat([dfaux, dfposaux, dfinf, dfx, dfc], axis=1)
    df = df.drop(["Pos3"], axis=1)


    dfply = df['Player'].count()
    dfmaxmin = df['Minutes played'].max()
    dfagemn = round(df['Age'].mean(), 2)
    dfagemin = df['Age'].min()
    dfagemax = df['Age'].max()
    dfgoals = df['Goals'].sum()
    dfpenal = df['Penalties taken'].sum()
    df['Penalties taken'] = df['Penalties taken'].astype(float)
    df['Penalties converted'] = (df['Penalties taken']*df['Penalty conversion, %'])/100
    dfconvpen = round(df['Penalties converted'].sum())
    dfexp = df['Red cards'].sum()
    st.markdown("""---""")
    st.title("CALCULATED METRICS")
    st.write(df)
    dfbackup = df
    st.markdown("<style> div { text-align: center; color: #FFFFFF } </style>", unsafe_allow_html=True)

    but0, but1 = st.columns(2)
    with but0:
        name = Filename
        df_xlsx = to_excel(df)
        st.download_button(label='Descargar Archivo Excel',
                           data=df_xlsx,
                           file_name= ""+ name +".xlsx")

    with but1:
        df_csv = convert_df(df)
        st.download_button(label="Descargar Archivo CSV",
                           data=df_csv,
                           file_name=""+ name +".csv",
                           mime='text/csv')
    
    row0, row1, row2, row3, row4, row5, row6, row7 = st.columns(8)
    #3118657252

    with row0:
        st.metric("Jugadores", dfply)
    
    with row1:
        st.metric("Max. Minutos", dfmaxmin)
    
    with row2:
        st.metric("Edad Promedio", dfagemn)
    
    with row3:
        st.metric("Edad mínima", dfagemin)
        
    with row4:
        st.metric("Edad máxima", dfagemax)
    
    with row5:
        st.metric("Goles", dfgoals)

    with row6:
        st.metric("Goles Penales", dfconvpen)
    
    with row7:
        st.metric("Expulsiones", dfexp)
        
    css='''
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    '''
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
        
   
    
    st.markdown("""---""")
    
    st.title("RANKING")
    
    with st.form(key='formMain'):
                            
        #tablecode = st.text_area('Paste your source code')
        dfORIGINAL = df
        df['Pos1'] = df['Pos1'].fillna("OTH")
        rs00, rs10, rs20 = st.columns(3)
        with rs00:
            #SELECT METRIC
            dftra = df.transpose()            
            dftra = dftra.reset_index()            
            metrics = list(dftra['index'].drop_duplicates())
            metrics = metrics[17:]
            metsel = st.selectbox('Selecciona la métrica:', metrics)   
        with rs10:
            #SELECT POSITION OPTION
            positions = list(df['Pos1'].drop_duplicates())
            auxpos = "ALL"
            positions.append(auxpos)
            positions.sort()
            possel = st.multiselect("Seleccionar posición:", positions)
            dfcc = df
            if possel == "ALL":
                df = dfcc
            else:
                df = df[df['Pos1'].isin(possel)]
        with rs20:
            metrics = [word for word in metrics if word != metsel]
            metsel2 = st.selectbox('Selecciona métrica auxiliar:', metrics)

        rx01, rx02, rx03 = st.columns(3)
        with rx01:
            #FILTER BY TEAMS
            df = dfORIGINAL
            teamlst = list(df['Team'].drop_duplicates())
            auxteam = "ALL"
            teamlst.append(auxteam)
            teamsel = st.selectbox('Seleccionar equipo:', teamlst)
            dft = df
            if teamsel == "ALL":
                df = dft
            else:
                df = df[df['Team'] == teamsel]
        #with rx02:
            #FILTER BY LEAGUE
        
        rs01, rs02, rs03 = st.columns(3)
        with rs01:
            #FILTER BY MINUTES
            maxmin = df['Minutes played'].max() + 5
            minsel = st.slider('Filtro de minutos (%):', 0, 100)
            minsel1 = (minsel*maxmin)/100
            df = df[df['Minutes played'] >= minsel1].reset_index()
            dfc = df
        with rs02:
            #FILTER BY AGE
            agesel = st.slider('Filtro de edad:', 15, 45, (15, 45), 1)   
            df = df[df['Age'] <= agesel[1]]
            df = df[df['Age'] >= agesel[0]]
        with rs03:
            #AGE FILTER
            umbralsel = st.slider("Seleccionar umbral:", 1, 100, 1) 
        submit_button_main = st.form_submit_button(label='Aceptar')
    #st.write(dfm)
    
    mainrow0, mainrow1 = st.columns(2)
    with mainrow0:
        
        fig, ax = plt.subplots(figsize = (12,12), dpi=600)
        fig.set_facecolor('#121214')
        ax.patch.set_facecolor('#121214')
        df = df.sort_values(by=[metsel], ascending=True)
        dfZinf = df[['Player', 'Team', 'Pos0', 'Age', 'Matches played', '90s']]
        dfZ2 = df[metsel2]
        dfZ2m = max(df[metsel2])
        umbral = (umbralsel*dfZ2m)/100
        df = df[df[metsel2] >= umbral]
        dfZ = df[metsel]        
        dfZT = pd.concat([dfZinf, dfZ, dfZ2], axis=1)
        ##################################################################################################################
        Y1 = dfZ.tail(10)
        Y2 = df['Total second assists'].tail(10)
        Y3 = df['Total third assists'].tail(10)
        Z = df['Player'].tail(10).str.upper()
        colors = colorlist((1, 0, 0.3137254901960784, 0), (1, 0, 0.3137254901960784, 1), 10)
        ax.barh(Z, Y1, edgecolor=(1,1,1,0.5), lw = 1, color=colors)
        #ax.barh(Z, Y2, left = Y1, facecolor='#1C2E46', edgecolor=(1,1,1,0.5), lw = 1)
        #ax.barh(Z, Y3, left = Y2+Y1, facecolor='#404C5B', edgecolor=(1,1,1,0.5), lw = 1)
        plt.setp(ax.get_yticklabels(), fontproperties=prop2, fontsize=18, color='#FFF')
        plt.setp(ax.get_xticklabels(), fontproperties=prop2, fontsize=20, color=(1,1,1,1))
        plt.xlabel(metsel, color = 'w', fontproperties=prop2, fontsize=15, labelpad=20)
        #ax.set_xticks([0, 5, 10])
        #ax.set_xlim(0, 18)
        ax.tick_params(axis='y', which='major', pad=15)
        spines = ['top','bottom','left','right']
        for x in spines:
            if x in spines:
                ax.spines[x].set_visible(False)
        st.pyplot(fig, bbox_inches="tight", dpi=600, format="png")  
    with mainrow1:
        dfZT = dfZT.sort_values(by=[metsel], ascending=False)
        st.dataframe(dfZT.head(15), height=490)
        
    st.markdown("""---""")
    
    st.title("SCATTER PLOT")
    df = dfORIGINAL
    with st.form(key='formScatter'):
        fk01, fk02, fk03 = st.columns(3)
        with fk01:
            #SELECT METRIC
            dftransp = df.transpose()            
            dftransp = dftransp.reset_index()            
            metricsFK = list(dftransp['index'].drop_duplicates())
            metricsFK = metricsFK[15:]
            metselFK = st.selectbox('Selecciona métrica uno:', metricsFK)
        with fk02:
            #SELECT METRIC TWO
            metricsFK2 = list(dftransp['index'].drop_duplicates())
            metricsFK2 = metricsFK2[16:]
            metselFK2 = st.selectbox('Selecciona métrica dos:', metricsFK2)
        with fk03:
            #SELECT POSITION OPTION
            positionsFK = list(df['Pos1'].drop_duplicates())
            auxpos1 = "ALL"
            positionsFK.append(auxpos1)
            posselFK = st.multiselect("Seleccionar posición:", positionsFK)
            #dfc = df
            #if posselFK == "ALL":
            #    df = dfc
            #else:
            df = df[df['Pos1'].isin(posselFK)]

        fk11, fk12, fk13 = st.columns(3)
        with fk11:
            #FILTER BY MINUTES
            maxmin = df['Minutes played'].max() + 5
            minsel = st.slider('Filtro de minutos (%):', 0, 100)
            minsel1 = (minsel*maxmin)/100
            df = df[df['Minutes played'] >= minsel1].reset_index()
            dfc = df
        with fk12:
            #FILTER BY AGE
            agesel = st.slider('Filtro de edad:', 15, 45, (15, 45), 1)   
            df = df[df['Age'] <= agesel[1]]
            df = df[df['Age'] >= agesel[0]]
        with fk13:
            #FILTER BY UMBRAL
            umbralsel = st.slider("Seleccionar umbral:", 1, 100, 1)
            dfplot = df

        fk21, fk22, fk23, fk24 = st.columns(4)
        with fk21:
            #FILTER BY TEAMS
            df = dfORIGINAL
            teams = list(df['Team'].drop_duplicates())
            auxtm = "ALL"
            teams.append(auxtm)
            teamsele = st.selectbox('Seleccionar equipo:', teams)
            dft = df
            if teamsele == "ALL":
                df = dft
            else:
                df = df[df['Team'] == teamsele]
        with fk22:
            #SELECT PLAYER 1
            players = list(df['Player'].drop_duplicates())            
            playersel1 = st.selectbox('Selecciona un jugador 1:', players)
            #FILTER BY PLAYER
            dfP1 = df[df['Player'] == playersel1]
        with fk23:
            #SELECT PLAYER 2
            #players = list(df['Player'].drop_duplicates())            
            playersel2 = st.selectbox('Selecciona un jugador 2:', players)
            #FILTER BY PLAYER
            dfP2 = df[df['Player'] == playersel2]
        with fk24:
            #SELECT PLAYER 3
            #players = list(df['Player'].drop_duplicates())            
            playersel3 = st.selectbox('Selecciona un jugador 3:', players)
            #FILTER BY PLAYER
            dfP3 = df[df['Player'] == playersel3]
            
        submit_buttonFK = st.form_submit_button(label='Aceptar')
    fig, ax = plt.subplots(figsize = (12,12), dpi=600)
    fig.set_facecolor('#121214')
    ax.patch.set_facecolor('#121214')
    xsel = dfplot[metselFK]
    ysel = dfplot[metselFK2]
    zsel = dfplot['Minutes played']
    xmean = xsel.mean()
    ymean = ysel.mean()

    xsel1 = dfP1[metselFK]
    ysel1 = dfP1[metselFK2]
    zsel1 = dfP1['Minutes played']
    ksel1 = dfP1['Player'].tolist()
    xsel2 = dfP2[metselFK]
    ysel2 = dfP2[metselFK2]
    zsel2 = dfP2['Minutes played']
    ksel2 = dfP2['Player'].tolist()
    xsel3 = dfP3[metselFK]
    ysel3 = dfP3[metselFK2]
    zsel3 = dfP3['Minutes played']
    ksel3 = dfP3['Player'].tolist()
    #st.write(x)
    #st.write(y)
    #st.write(df['Goals']
    ax.scatter(xsel, ysel, s=zsel, color="#FF0046", edgecolors='#121214', alpha=0.7)

    ax.scatter(xsel1, ysel1, s=zsel1, color="#FFF", edgecolors='#121214', alpha=0.7)
    ax.scatter(xsel2, ysel2, s=zsel2, color="#FFF", edgecolors='#121214', alpha=0.7)
    ax.scatter(xsel3, ysel3, s=zsel3, color="#FFF", edgecolors='#121214', alpha=0.7)

    #for i, txt in enumerate(zzz3):
    ax.annotate(ksel1, (xsel1, ysel1+0.03), c='w', fontproperties=prop2, fontsize=9, zorder=4, ha='center', va='center')
    ax.annotate(ksel2, (xsel2, ysel2+0.03), c='w', fontproperties=prop2, fontsize=9, zorder=4, ha='center', va='center')
    ax.annotate(ksel3, (xsel3, ysel3+0.03), c='w', fontproperties=prop2, fontsize=9, zorder=4, ha='center', va='center')
        
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_color("#FFFFFF")
    plt.setp(ax.get_yticklabels(), fontproperties=prop2, fontsize=18, color='#FFF')
    plt.setp(ax.get_xticklabels(), fontproperties=prop2, fontsize=20, color=(1,1,1,1))
    plt.xlabel(metselFK, color = 'w', fontproperties=prop2, fontsize=15, labelpad=20)
    plt.ylabel(metselFK2, color = 'w', fontproperties=prop2, fontsize=15, labelpad=20)
    maxXaux = max(xsel)
    maxX = maxXaux + (0.05*maxXaux)
    maxYaux = max(ysel)
    maxY = maxYaux + (0.05*maxYaux)
    ax.set_xlim(0-(0.04*maxYaux), maxX)
    ax.set_ylim(0-(0.04*maxYaux), maxY)

    ax.vlines(xmean, -0.1, maxY, color='w', linestyle='--', alpha=0.8, zorder=3)
    ax.hlines(ymean, -0.1, maxX, color='w', linestyle='--', alpha=0.8, zorder=3)
    #st.markdown("<style> div { text-align: center; color: #FFFFFF } </style>", unsafe_allow_html=True)
    st.pyplot(fig, bbox_inches="tight", dpi=600, format="png")
    
    # I usually dump any scripts at the bottom of the page to avoid adding unwanted blank lines
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)

############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

if menu_id == "ExtractData":
    with st.sidebar:
        with open("Resources/win.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                <img src="data:image/png;base64,{data}" width="300">
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        st.markdown("""---""")    
            
        with st.form(key='form2'):
                                
            tablecode = st.text_area('Paste your source code')
            
            rs00, rs10 = st.columns(2)
            with rs00:
                Filename = st.text_input("Filename", key="filename")   
            with rs10:
                Player = st.text_input("Player:", key="player")
            rs01, rs02 = st.columns(2)
            with rs01:
                Matchday = st.text_input("Matchday:", key="matchday")
            with rs02:
                Match = st.text_input("Match:", key="match")   
            rs03, rs04 = st.columns(2)
            with rs03:
                Competition = st.text_input("Competition:", key="competition")   
            with rs04:
                Date = st.text_input("Date Game:", key="date")   
            
            VizOption = ['Actions Data', 'Passes Data', 'Shots Data', 'Dribbles Data', 'Duels Data', 'Aerial Duels Data', 
                         'Defensive Duels Data', 'Offensive Duels Data', 'Recoveries Data', 'Progressive Runs Data', 
                         'Received Passes Data']
            
            Option = st.selectbox('Query Mode:', VizOption)
                
            submit_button2 = st.form_submit_button(label='Aceptar')
            
    st.markdown("<style> div { text-align: center } </style>", unsafe_allow_html=True)
    st.markdown("""---""")
    st.title(Option.upper())
    if Option == "Shots Data":
        datos = tablecode.split('Index__shots___B7aUA">')
        datos = datos[1]
        datos = datos.split("xG")
        df = pd.DataFrame(datos, columns=["EVENT"])
        df.drop(df.tail(1).index,inplace=True)
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        dfc = df
        dfdiv = df['EVENT'].str.split("width:", expand=True)
        dfdiv.columns = ['Event', 'Coordenadas']
        dfcoord = dfdiv['Coordenadas'].str.split("<span>", expand=True)
        dfcoord.columns = ['Coord', 'xG']
        dfcoord['xG'] = dfcoord['xG'].str[44:]
        dfcoordxg = dfcoord.drop(['Coord'], axis=1)
        dfcoord = dfcoord['Coord'].str.split("%;", expand=True)
        dfcoord.columns = ['ONE', 'X1', 'Y1', 'TWO']
        dfcoord = dfcoord.drop(['ONE', 'TWO'], axis=1)
        dfcoord['X1'] = dfcoord['X1'].map(lambda x: x.lstrip('left: ').rstrip(''))
        dfcoord['Y1'] = dfcoord['Y1'].map(lambda x: x.lstrip('top: ').rstrip(''))
        dfcoor = pd.concat([dfcoordxg, dfcoord], axis=1)
        dfevent = dfdiv['Event'].str.split("Index__shot", expand=True)
        dfevent.columns = ['one', 'Status']
        dfevent = dfevent.drop(['one'], axis=1)
        dfevent = dfevent.reset_index()
        dfevent['Status'] = dfevent['Status'].str[3:-17]
        dfevent = dfevent['Status'].str.split("Index__", expand=True)
        dfevent.columns = ['one', 'Status']
        dfevent = dfevent.drop(['one'], axis=1)
        dfevent = dfevent.reset_index()
        dfevents = dfevent['Status']
        dfT = pd.concat([dfcoor, dfevents], axis=1)
        dfT['Player'] = Player
        dfT['Competition'] = Competition
        dfT['Match'] = Match
        dfT['DateGame'] = Date
        dfT['Matchday'] = Matchday
        dfT['Event'] = Option[:-5]
        dfT = dfT[["Competition", "Matchday", "DateGame", "Match", "Player", "Event", "Status", "xG", "X1", "Y1"]]
        st.write(dfT)
        but0, but1 = st.columns(2)
        with but0:
            name = Filename
            df_xlsx = to_excel(dfT)
            st.download_button(label='Descargar Archivo Excel',
                               data=df_xlsx,
                               file_name= ""+ name +".xlsx")
    
        with but1:
            df_csv = convert_df(dfT)
            st.download_button(label="Descargar Archivo CSV",
                               data=df_csv,
                               file_name=""+ name +".csv",
                               mime='text/csv')
    elif Option == "Passes Data":
        datos = tablecode.split("<g>")
        df = pd.DataFrame(datos, columns=["EVENT"])
        df.drop(df.head(1).index,inplace=True)
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        dfc = df
        df['EVENT'] = df['EVENT'].str[257:]
        dfdiv = df['EVENT'].str.split("marker-end=", expand=True)
        dfdiv.columns = ['Status', 'Coordenadas']
        dfdiv['Status'] = dfdiv['Status'].str[:-68]
        dfdiv['Coordenadas'] = dfdiv['Coordenadas'].str[25:]
        dfevent = dfdiv['Status']
        dfcoord = dfdiv['Coordenadas'].str.split("stroke-opacity", expand=True)
        dfcoord.columns = ['Other', 'Coord']
        dfcoord = dfcoord.drop(['Other'],axis=1)
        dfcoord['Coord'] = dfcoord['Coord'].str[5:-13]
        dfcoord = dfcoord['Coord'].str.split("=", expand=True)
        dfcoord.columns = ['one', 'X1', 'Y1', 'X2', 'Y2']
        dfcoord = dfcoord.drop(['one'], axis=1)
        dfcoord['X1'] = dfcoord['X1'].str[1:-4]
        dfcoord['Y1'] = dfcoord['Y1'].str[1:-4]
        dfcoord['X2'] = dfcoord['X2'].str[1:-4]
        dfcoord['Y2'] = dfcoord['Y2'].str[1:]
        dfcoordd = dfcoord['Y2'].str.split('"><', expand=True)
        dfcoordd.columns=['Y2', 'zer']
        dfcoordd = dfcoordd.drop(['zer'],axis=1)
        dfcoord = dfcoord.drop(['Y2'],axis=1)
        dfcoor = pd.concat([dfcoord, dfcoordd], axis=1)
        dfT = pd.concat([dfevent, dfcoor], axis=1)
        dfT = dfT.replace("d800ff", "Key")
        dfT = dfT.replace("0876ff", "Successful")
        dfT = dfT.replace("909090", "Unsuccessful")
        dfT['Player'] = Player
        dfT['Competition'] = Competition
        dfT['Match'] = Match
        dfT['DateGame'] = Date
        dfT['Matchday'] = Matchday
        dfT['Event'] = Option[:-5]
        dfT = dfT[["Competition", "Matchday", "DateGame", "Match", "Player", "Event", "Status", "X1", "Y1", "X2", "Y2"]]
        st.write(dfT)
        but0, but1 = st.columns(2)
        with but0:
            name = Filename
            df_xlsx = to_excel(dfT)
            st.download_button(label='Descargar Archivo Excel',
                               data=df_xlsx,
                               file_name= ""+ name +".xlsx")
    
        with but1:
            df_csv = convert_df(dfT)
            st.download_button(label="Descargar Archivo CSV",
                               data=df_csv,
                               file_name=""+ name +".csv",
                               mime='text/csv') 
        
    else:
        datos = tablecode.split("<div")
        df = pd.DataFrame([datos])
        df = pd.DataFrame(datos, columns=["EVENT"])
        df.drop(df.head(2).index,inplace=True)
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        dfc = df
        dfdiv = df['EVENT'].str.split("style=", expand=True)
        dfdiv.columns = ['Event', 'Coordenadas']
        dfdiv['Coordenadas'] = dfdiv['Coordenadas'].str[1:-22]
        dfdiv['Event'] = dfdiv['Event'].str[24:-10]
        dfcoord = dfdiv['Coordenadas'].str.split(';', expand=True)
        dfevent = dfdiv['Event'].str.split('Index_', expand=True)
        dfcoord.columns = ['X1', 'Y1', 'K'] 
        dfcoord = dfcoord.drop(['K'], axis=1)
        dfcoord['X1'] = dfcoord['X1'].str[5:-1]
        dfcoord['Y1'] = dfcoord['Y1'].str[5:]
        dfevent.columns = ["" + Option + " ID", 'Status']
        dfevent['Status'] = dfevent['Status'].str[1:]
        dfT = pd.concat([dfevent, dfcoord], axis=1)
        dfT['Y1'] = dfT['Y1'].map(lambda x: x.lstrip('').rstrip('%'))
        dfT['Player'] = Player
        dfT['Competition'] = Competition
        dfT['Match'] = Match
        dfT['DateGame'] = Date
        dfT['Matchday'] = Matchday
        dfT['Event'] = Option[:-5]
        dfT = dfT[["Competition", "Matchday", "DateGame", "Match", "Player", "Event", "Status", "X1", "Y1"]]
        st.write(dfT)
        
        but0, but1 = st.columns(2)
        with but0:
            name = Filename
            df_xlsx = to_excel(dfT)
            st.download_button(label='Descargar Archivo Excel',
                               data=df_xlsx,
                               file_name= ""+ name +".xlsx")
    
        with but1:
            df_csv = convert_df(dfT)
            st.download_button(label="Descargar Archivo CSV",
                               data=df_csv,
                               file_name=""+ name +".csv",
                               mime='text/csv')
    st.markdown("<style> div { text-align: center } </style>", unsafe_allow_html=True)
    dfT = dfT.replace("won", "Successful")
    dfT = dfT.replace("lost", "Unsuccessful")
    dfwon = dfT[dfT['Status'] == 'Successful'].reset_index()
    dflost = dfT[dfT['Status'] == 'Unsuccessful'].reset_index()
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Acciones", len(dfT))
    with r2:
        st.metric("Exitosas", len(dfwon))
    with r3:
        st.metric("Fallidas", len(dflost))
    with r4:
        dfwon4 = len(dfwon)
        dfT4 = len(dfT)
        #st.write(type(dfT))
        st.metric("Efectividad (%)", round((dfwon4*100)/dfT4))

    #st.markdown("<style> div { text-align: center; color: #FFFFFF } </style>", unsafe_allow_html=True)
    css='''
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    '''
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
###
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
if menu_id == "PlayerStats":
    with st.sidebar:
        with open("Resources/win.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                <img src="data:image/png;base64,{data}" width="300">
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        st.markdown("""---""")    

        #SELECT DATA
        Dataframe = st.file_uploader("Cargar archivo:", type="xlsx")
        if Dataframe is not None:
            df = pd.read_excel(Dataframe)

        df['Pos1'] = df['Pos1'].fillna("OTH")
        with st.form(key='form3'):

            #SELECT AGE
            agesel = st.slider('Filtro de edad:', 15, 50, (15, 50), 1)   
            #FILTER BY AGE
            df = df[df['Age'] <= agesel[1]]
            df = df[df['Age'] >= agesel[0]]
            #SELECT MINS
            minsel = st.slider('Filtro de minutos (%):', 0, 100)
            #FILTER BY MINUTES
            maxmin = df['Minutes played'].max() + 5
            minsel1 = (minsel*maxmin)/100
            df = df[df['Minutes played'] >= minsel1].reset_index()
            #SELECT POSITION OPTION
            positions = list(df['Pos1'].drop_duplicates())
            positions.append("ALL")
            positions.sort()
            seldf0 = st.selectbox("Filtrar por posición:", positions)
            #FILTER BY POSITIONS
            dftres = df
            if seldf0 == 'ALL':
                df = dftres
            else:
                df = dftres[dftres['Pos1'] == seldf0].reset_index()
                dfax = df[['Player', 'Team', 'Pos1', 'Pos2', 'Age']]
            dfccc = df
            dfcuatro = df
            #SELECT TEAM
            teams = list(df['Team'].drop_duplicates())
            teamsel1 = st.selectbox('Selecciona un equipo:', teams)
            #FILTER BY TEAMS
            df = df[df['Team'] == teamsel1]
            #SELECT PLAYER
            players = list(df['Player'].drop_duplicates())            
            playersel = st.selectbox('Selecciona un jugador:', players)
            #FILTER BY PLAYER
            df = df[df['Player'] == playersel]

            #GET AUX INFO
            dfaux = df[['Player', 'Team', 'Pos1', 'Age', '90s']]
                            
            submit_button3 = st.form_submit_button(label='Aceptar')

    


            
    st.markdown("<style> div { text-align: center } </style>", unsafe_allow_html=True)
    st.markdown("""---""")
    st.title("PLAYER STATS")
    st.write(df)
    st.markdown("""---""")
    st.title("RADAR METRICS GROUP")
    # Data Cleaning - Exploratory Data Analysis 

    #Filtrar métricas normalizadas por 90 minutos
    dfp90 = df[['90s',
                'Successful attacking actions per 90', 'Offensive duels per 90', 'Offensive duels won per 90', 'Touches in box per 90', 'Goals per 90', 'Non-penalty goals per 90', 'Head goals per 90', 'xG per 90', 'NPxG per 90', 'Shots per 90', 'Shots on target per 90', 
                'Successful defensive actions per 90', 'Defensive duels per 90', 'Defensive duels won per 90', 'Sliding tackles per 90', 'Shots blocked per 90', 'Interceptions per 90', 
                'Duels per 90', 'Duels won per 90', 'Aerial duels per 90', 'Aerial duels won per 90', 'Fouls per 90', 'Dribbles per 90', 'Successful dribbles per 90', 'Progressive runs per 90', 'Received passes per 90', 'Received long passes per 90', 'Fouls suffered per 90', 
                'Assists per 90', 'xA per 90', 'Second assists per 90', 'Third assists per 90', 'Crosses per 90', 'Crosses completed per 90', 'Crosses to goalie box per 90', 'Crosses from left flank per 90', 'Crosses from right flank per 90', 'Shot assists per 90', 'Key passes per 90', 'Smart passes per 90', 'Smart passes completed per 90', 'Passes to penalty area per 90', 'Passes to penalty area completed per 90', 'Through passes per 90', 'Through passes completed per 90', 'Deep completions per 90', 'Deep completed crosses per 90',
                'Passes per 90', 'Passes completed per 90', 'Forward passes per 90', 'Forward passes completed per 90', 'Back passes per 90', 'Back passes completed per 90', 'Lateral passes per 90', 'Lateral passes completed per 90', 'Short / medium passes per 90', 'Short / medium passes completed per 90', 'Long passes per 90', 'Long passes completed per 90', 'Passes to final third per 90', 'Passes to final third completed per 90', 'Progressive passes per 90', 'Progressive passes completed per 90',
                'Free kicks per 90', 'Direct free kicks per 90',
                'Conceded goals per 90', 'Shots against per 90', 'xG against per 90', 'Prevented goals per 90', 'Back passes received as GK per 90', 'Exits per 90', 'Aerial duels per 90.1',
                'Yellow cards per 90', 'Red cards per 90']]
    
    #Filtrar por acciones ofensivas
    dfofe = df[['Successful attacking actions per 90', 'Offensive duels per 90', 'Offensive duels won per 90', 'Touches in box per 90', 'Goals per 90', 'Non-penalty goals per 90', 'Head goals per 90', 'xG per 90', 'NPxG per 90', 'Shots per 90', 'Shots on target per 90']]
    dfofel = dfofe.columns
    dfofeccc = dfccc[['Successful attacking actions per 90', 'Offensive duels per 90', 'Offensive duels won per 90', 'Touches in box per 90', 'Goals per 90', 'Non-penalty goals per 90', 'Head goals per 90', 'xG per 90', 'NPxG per 90', 'Shots per 90', 'Shots on target per 90', ]]
    dfofelccc = dfofeccc.columns
    
    #Filtrar por acciones defensivas
    dfdef = df[['Successful defensive actions per 90', 'Defensive duels per 90', 'Defensive duels won per 90', 'Sliding tackles per 90', 'Shots blocked per 90', 'Interceptions per 90']]
    dfdefl = dfdef.columns
    dfdefccc = dfccc[['Successful defensive actions per 90', 'Defensive duels per 90', 'Defensive duels won per 90', 'Sliding tackles per 90', 'Shots blocked per 90', 'Interceptions per 90']]
    dfdeflccc = dfdefccc.columns
    
    #Filtrar por acciones de posesión
    dfpos = df[['Duels per 90', 'Duels won per 90', 'Aerial duels per 90', 'Aerial duels won per 90', 'Fouls per 90', 'Dribbles per 90', 'Successful dribbles per 90', 'Progressive runs per 90', 'Received passes per 90', 'Received long passes per 90', 'Fouls suffered per 90']]
    dfposl = dfpos.columns
    dfposccc = dfccc[['Duels per 90', 'Duels won per 90', 'Aerial duels per 90', 'Aerial duels won per 90', 'Fouls per 90', 'Dribbles per 90', 'Successful dribbles per 90', 'Progressive runs per 90', 'Received passes per 90', 'Received long passes per 90', 'Fouls suffered per 90']]
    dfposlccc = dfposccc.columns
    
    #Filtrar por acciones de generación
    dfcre = df[['Assists per 90', 'xA per 90', 'Second assists per 90', 'Third assists per 90', 'Crosses per 90', 'Crosses completed per 90', 'Crosses to goalie box per 90', 'Shot assists per 90', 'Key passes per 90', 'Smart passes per 90', 'Smart passes completed per 90', 'Passes to penalty area per 90', 'Passes to penalty area completed per 90', 'Through passes per 90', 'Through passes completed per 90', 'Deep completions per 90', 'Deep completed crosses per 90']]
    dfcrel = dfcre.columns
    dfcreccc = dfccc[['Assists per 90', 'xA per 90', 'Second assists per 90', 'Third assists per 90', 'Crosses per 90', 'Crosses completed per 90', 'Crosses to goalie box per 90', 'Shot assists per 90', 'Key passes per 90', 'Smart passes per 90', 'Smart passes completed per 90', 'Passes to penalty area per 90', 'Passes to penalty area completed per 90', 'Through passes per 90', 'Through passes completed per 90', 'Deep completions per 90', 'Deep completed crosses per 90']]
    dfcrelccc = dfcreccc.columns
    
    #Filtrar por acciones de distribución
    dfdis = df[['Passes per 90', 'Passes completed per 90', 'Forward passes per 90', 'Forward passes completed per 90', 'Back passes per 90', 'Back passes completed per 90', 'Lateral passes per 90', 'Lateral passes completed per 90', 'Short / medium passes per 90', 'Short / medium passes completed per 90', 'Long passes per 90', 'Long passes completed per 90', 'Passes to final third per 90', 'Passes to final third completed per 90', 'Progressive passes per 90', 'Progressive passes completed per 90',]]
    dfdisl = dfdis.columns
    dfdisccc = dfccc[['Passes per 90', 'Passes completed per 90', 'Forward passes per 90', 'Forward passes completed per 90', 'Back passes per 90', 'Back passes completed per 90', 'Lateral passes per 90', 'Lateral passes completed per 90', 'Short / medium passes per 90', 'Short / medium passes completed per 90', 'Long passes per 90', 'Long passes completed per 90', 'Passes to final third per 90', 'Passes to final third completed per 90', 'Progressive passes per 90', 'Progressive passes completed per 90',]]
    dfdislccc = dfdisccc.columns
    
    #Filtrar por acciones complementarias
    dfoth = df[['90s', 'Yellow cards per 90', 'Red cards per 90', 'Free kicks per 90', 'Direct free kicks per 90']]
    dfothl = dfoth.columns
    dfothccc = dfccc[['90s', 'Yellow cards per 90', 'Red cards per 90', 'Free kicks per 90', 'Direct free kicks per 90']]
    dfothlccc = dfothccc.columns
    
    
    
    df['Team'] = df['Team'].astype(str)
    #df['Pos0'] = df['Pos0'].astype(str)
    dfccc['Team'] = dfccc['Team'].astype(str)
    #dfccc['Pos0'] = dfccc['Pos0'].astype(str)    
    
    #GET AUX INFO PLAYER
    #dfaux = df[['Player', 'Team', 'Pos1', 'Age', '90s']]
    dfmins = dfaux['90s']
    dfmins = dfmins*90
    
    dfauxccc = dfccc[['Player', 'Team', 'Pos1', 'Age', '90s']]
    dfminsccc = dfauxccc['90s']
    dfminsccc = dfminsccc*90
    
    #Valores por acciones ofensivas
    valuessofe = dfofe.iloc[0,:]
    valuessofe2 = round(dfofeccc.mean(), 2)
    
    #Valores por acciones defensivas
    valuessdef = dfdef.iloc[0,:]
    valuessdef2 = round(dfdefccc.mean(), 2)
    
    #Valores por acciones de posesión
    valuesspos = dfpos.iloc[0,:]
    valuesspos2 = round(dfposccc.mean(), 2)
    
    #Valores por acciones de generación
    valuesscre = dfcre.iloc[0,:]
    valuesscre2 = round(dfcreccc.mean(), 2)
    
    #Valores por acciones de distribución
    valuessdis = dfdis.iloc[0,:]
    valuessdis2 = round(dfdisccc.mean(), 2)
    
    #Valores por acciones complementarias
    valuessoth = dfoth.iloc[0,:]
    valuessoth2 = round(dfothccc.mean(), 2)
    
    #Valores
    
    ##################################################################################################################################
    
    #dfmn = df5.mean()
    #df5.loc[-1] = round(dfmn, 2)
    
    
    #st.write(len(dfccc))
    #st.dataframe(dfccc)
    #st.write(len(df))
    #st.dataframe(df)
    
    
    
    
    ##################################################################################################################################
    ##Radar process   
    
    #Obtener valores minimos y máximos de métricas ofensivas        
    lowwofe = []
    highhofe = []
    for an in range(len(dfofeccc.columns)):
        lowwofe.append(min(dfofeccc.iloc[:,an]))
        highhofe.append(max(dfofeccc.iloc[:,an]))    
    
    #Obtener valores minimos y máximos de métricas defensivas        
    lowwdef = []
    highhdef = []
    for an in range(len(dfdefccc.columns)):
        lowwdef.append(min(dfdefccc.iloc[:,an]))
        highhdef.append(max(dfdefccc.iloc[:,an]))    
    
    #Obtener valores minimos y máximos de métricas de posesión        
    lowwpos = []
    highhpos = []
    for an in range(len(dfposccc.columns)):
        lowwpos.append(min(dfposccc.iloc[:,an]))
        highhpos.append(max(dfposccc.iloc[:,an]))    
        
    #Obtener valores minimos y máximos de métricas de generación        
    lowwcre = []
    highhcre = []
    for an in range(len(dfcreccc.columns)):
        lowwcre.append(min(dfcreccc.iloc[:,an]))
        highhcre.append(max(dfcreccc.iloc[:,an]))    
    
    #Obtener valores minimos y máximos de métricas de distribución
    lowwdis = []
    highhdis = []
    for an in range(len(dfdisccc.columns)):
        lowwdis.append(min(dfdisccc.iloc[:,an]))
        highhdis.append(max(dfdisccc.iloc[:,an]))    
    
    #Obtener valores minimos y máximos de métricas complementarias        
    lowwoth = []
    highhoth = []
    for an in range(len(dfothccc.columns)):
        lowwoth.append(min(dfothccc.iloc[:,an]))
        highhoth.append(max(dfothccc.iloc[:,an]))        
    
    
    
    rangparamofe = len(dfofelccc)
    rangparamdef = len(dfdeflccc)
    rangparampos = len(dfposlccc)
    rangparamcre = len(dfcrelccc)
    rangparamdis = len(dfdislccc)
    rangparamoth = len(dfothlccc)
    
    #Radar ofensivo
    radarofe = Radar(dfofelccc, lowwofe, highhofe,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparamofe,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    #Radar defensivo
    radardef = Radar(dfdeflccc, lowwdef, highhdef,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparamdef,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    
    #Radar de posesión
    radarpos = Radar(dfposlccc, lowwpos, highhpos,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparampos,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    #Radar de generación
    radarcre = Radar(dfcrelccc, lowwcre, highhcre,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparamcre,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    #Radar de distribución
    radardis = Radar(dfdislccc, lowwdis, highhdis,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparamdis,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    
    #Radar complementario
    radaroth = Radar(dfothlccc, lowwoth, highhoth,
                  # whether to round any of the labels to integers instead of decimal places
                  round_int=[False]*rangparamoth,
                  num_rings=4,  # the number of concentric circles (excluding center circle)
                  # if the ring_width is more than the center_circle_radius then
                  # the center circle radius will be wider than the width of the concentric circles
                  ring_width=1, center_circle_radius=1)
    
    space0, space1, space2 = st.columns((0.6, 0.6, 0.6))

    colorradar1 = "#FF0046"
    colorradar2 = "#005CBE"
    alpharradar1 = 0.5
    alpharradar2 = 0.5
    
    with space0:
        fig, ax = radarofe.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">OFFENSIVE</h1>', unsafe_allow_html=True)
    
        rings_inner = radarofe.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radarofe.draw_radar_compare(valuessofe, valuessofe2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radarofe.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1, zorder=-1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2, zorder=-1)
    
        #st.write(lowwofe)
        #st.write(highhofe)
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png")   
        
    with space1:
        fig, ax = radardef.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">DEFENSIVE</h1>', unsafe_allow_html=True)
        rings_inner = radardef.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radardef.draw_radar_compare(valuessdef, valuessdef2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radardef.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2)
    
        #st.write(lowwdef)
        #st.write(highhdef)
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png")       
        
        
    with space2:
        fig, ax = radarpos.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">POSSESION</h1>', unsafe_allow_html=True)
        rings_inner = radarpos.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radarpos.draw_radar_compare(valuesspos, valuesspos2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radarpos.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2)
    
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png") 
        #st.write(lowwpos)
        #st.write(highhpos)
    
    
    space3, space4, space5 = st.columns((0.6, 0.6, 0.6))
          
    with space3:
        fig, ax = radarcre.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">CREATION</h1>', unsafe_allow_html=True)
        rings_inner = radarcre.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radarcre.draw_radar_compare(valuesscre, valuesscre2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radarcre.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2)
    
        #st.write(lowwcre)
        #st.write(highhcre)
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png")   
        
    with space4:
        fig, ax = radardis.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">DISTRIBUTION</h1>', unsafe_allow_html=True)
        rings_inner = radardis.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radardis.draw_radar_compare(valuessdis, valuessdis2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radardis.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2)
    
        #st.write(lowwdis)
        #st.write(highhdis)
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png")       
        
        
    with space5:
        fig, ax = radaroth.setup_axis()  # format axis as a radar
        fig.set_facecolor('#050E1E')
        fig.set_dpi(600)
        st.markdown('<h1 style="font-size: 25px;">GENERAL</h1>', unsafe_allow_html=True)
        rings_inner = radaroth.draw_circles(ax=ax, facecolor=(1,1,1,0), edgecolor='#222229')  # draw circles
        radar_output = radaroth.draw_radar_compare(valuessoth, valuessoth2, ax=ax,
                                                kwargs_radar={'facecolor': colorradar1, 'alpha' : alpharradar1},
                                                kwargs_compare={'facecolor': colorradar2, 'alpha' : alpharradar2},
                                                )  # draw the radar
        radar_poly, radar_poly2, vertices, vertices2 = radar_output
        # range_labels = radar.draw_range_labels(ax=ax, fontsize=18,
        #                                        fontproperties=prop)  # draw the range labels
        param_labels = radaroth.draw_param_labels(ax=ax, fontsize=15, color=(1,1,1,0.8),
                                               fontproperties=prop2)  # draw the param labels
    
        vert = vertices.tolist()
        dfver = pd.DataFrame(vert, columns=['X', 'Y'])
        uno = dfver['X'].tolist()
        dos = dfver['Y'].tolist()
    
        ax.scatter(vertices[:, 0], vertices[:, 1], c=colorradar1, edgecolors='#050E1E', s=120, alpha=alpharradar1)
        ax.scatter(vertices2[:, 0], vertices2[:, 1], c=colorradar2, edgecolors='#050E1E', s=120, alpha=alpharradar2)
    
        #st.write(lowwoth)
        #st.write(highhoth)
    
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png") 

    #####
    fig, ax = plt.subplots(figsize = (12,1), dpi=600)
    #fig.set_visible(False)
    #ax.patch.set_visible('False')
    ax.axis('off')
    fig.patch.set_visible(False)
    ax.set_xlim(0,100)
    ax.set_ylim(0,10)
    ax.scatter(30, 5, s=600, color=colorradar1, marker='s')
    ax.scatter(70, 5, s=600, color=colorradar2, marker='s')
    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=600, format="png")
    st.markdown("""---""")        
    st.table(dfaux.style.set_precision(2)) 
    
       
    s01, s02, s03 = st.columns((0.6, 0.6, 0.6))
    with s01:
        coldfofe = list(dfofeccc.columns)
        coldfofe = pd.Series(coldfofe)
        lowwofe = pd.Series(lowwofe)
        highhofe = pd.Series(highhofe)
        valueofe = pd.Series(valuessofe.values)
        meanofe = pd.Series(valuessofe2.values)
        coldfofe = pd.concat([coldfofe, lowwofe, highhofe, valueofe, meanofe], axis=1)
        coldfofe.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfofe.style.set_precision(2))
        
    with s02:
        coldfdef = list(dfdefccc.columns)
        coldfdef = pd.Series(coldfdef)
        lowwdef = pd.Series(lowwdef)
        highhdef = pd.Series(highhdef)
        valuedef = pd.Series(valuessdef.values)
        meandef = pd.Series(valuessdef2.values)
        coldfdef = pd.concat([coldfdef, lowwdef, highhdef, valuedef, meandef], axis=1)
        coldfdef.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfdef.style.set_precision(2))
        
    with s03:
        coldfpos = list(dfposccc.columns)
        coldfpos = pd.Series(coldfpos)
        lowwpos = pd.Series(lowwpos)
        highhpos = pd.Series(highhpos)
        valuepos = pd.Series(valuesspos.values)
        meanpos = pd.Series(valuesspos2.values)
        coldfpos = pd.concat([coldfpos, lowwpos, highhpos, valuepos, meanpos], axis=1)
        coldfpos.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfpos.style.set_precision(2))
        
        
    s04, s05, s06 = st.columns((0.6, 0.6, 0.6))
        
    with s04:
        coldfcre = list(dfcreccc.columns)
        coldfcre = pd.Series(coldfcre)
        lowwcre = pd.Series(lowwcre)
        highhcre = pd.Series(highhcre)
        valuecre = pd.Series(valuesscre.values)
        meancre = pd.Series(valuesscre2.values)
        coldfcre = pd.concat([coldfcre, lowwcre, highhcre, valuecre, meancre], axis=1)
        coldfcre.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfcre.style.set_precision(2))
        
    with s05:
        coldfdis = list(dfdisccc.columns)
        coldfdis = pd.Series(coldfdis)
        lowwdis = pd.Series(lowwdis)
        highhdis = pd.Series(highhdis)
        valuedis = pd.Series(valuessdis.values)
        meandis = pd.Series(valuessdis2.values)
        coldfdis = pd.concat([coldfdis, lowwdis, highhdis, valuedis, meandis], axis=1)
        coldfdis.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfdis.style.set_precision(2))
        
    with s06:
        coldfoth = list(dfothccc.columns)
        coldfoth = pd.Series(coldfoth)
        lowwoth = pd.Series(lowwoth)
        highhoth = pd.Series(highhoth)
        valueoth = pd.Series(valuessoth.values)
        meanoth = pd.Series(valuessoth2.values)
        coldfoth = pd.concat([coldfoth, lowwoth, highhoth, valueoth, meanoth], axis=1)
        coldfoth.columns=['Métrica', 'Min', 'Max', 'Valor', 'Promedio']
        st.table(coldfoth.style.set_precision(2))

    
    st.markdown("""---""")
    st.title("CUSTOM RADAR METRICS")
    df = pd.DataFrame(
    np.random.randn(200,3),
    columns=['a', 'b', 'c']
    )
    
    c = alt.Chart(df, width=600).mark_circle().encode(
        x='a', y='b', size='c', color='c', 
        tooltip=['a', 'b', 'c'] # <--- tooltip part
    )
    
    st.altair_chart(c)
