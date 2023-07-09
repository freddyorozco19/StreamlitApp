# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 03:14:41 2023

@author: ACER
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
    {'id': "AllMetrics", 'label':"AllMetrics"},
    {'id': "ActionsData", 'label':"Extract ActionsData"},
    {'id': "PassesData", 'label':"Extract PassesData"},
    {'id': "ProMatchStats", 'label':"ProMatchStats"},
    {'id': "Dashboard", 'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message]
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
            #auxpos = "ALL"
            #positions.append(auxpos)
            possel = st.multiselect("Seleccionar posición:", positions)
            dfc = df
            #if possel == "ALL":
            #    df = dfc
            #else:
            df = df[df['Pos1'].isin(possel)]
        with rs20:
            metrics = [word for word in metrics if word != metsel]
            metsel2 = st.selectbox('Selecciona métrica auxiliar:', metrics)

        rs01, rs02, rs03, rs04 = st.columns(4)
        with rs01:
            #FILTER BY TEAMS
            teamlst = list(df['Team'].drop_duplicates())
            teamsel = st.selectbox('Seleccionar equipo:', teamlst)
            dft = df
            df = df[df['Teams'].isin(possel)]
        with rs02:
            #FILTER BY MINUTES
            maxmin = df['Minutes played'].max() + 5
            minsel = st.slider('Filtro de minutos (%):', 0, 100)
            minsel1 = (minsel*maxmin)/100
            df = df[df['Minutes played'] >= minsel1].reset_index()
            dfc = df
        with rs03:
            #FILTER BY AGE
            agesel = st.slider('Filtro de edad:', 15, 45, (15, 45), 1)   
            df = df[df['Age'] <= agesel[1]]
            df = df[df['Age'] >= agesel[0]]
        with rs04:
            #AGE FILTER
            umbralsel = st.slider("Seleccionar umbral:", 1, 100, 1) 
        submit_button_main = st.form_submit_button(label='Aceptar')
    #st.write(dfm)
    
    mainrow0, mainrow1 = st.columns(2)
    with mainrow0:
        
        fig, ax = plt.subplots(figsize = (12,12), dpi=600)
        fig.set_facecolor('#050E1E')
        ax.patch.set_facecolor('#050E1E')
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
    df = dfbackup
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
            #auxpos = "ALL"
            #positions.append(auxpos)
            posselFK = st.multiselect("Seleccionar posición:", positionsFK)
            dfc = df
            #if possel == "ALL":
            #    df = dfc
            #else:
            df = df[df['Pos1'].isin(possel)]
        submit_buttonFK = st.form_submit_button(label='Aceptar')
     
    fig, ax = plt.subplots(figsize = (12,12), dpi=600)
    fig.set_facecolor('#050E1E')
    ax.patch.set_facecolor('#050E1E')
        
    #st.markdown("<style> div { text-align: center; color: #FFFFFF } </style>", unsafe_allow_html=True)
  
    
    # I usually dump any scripts at the bottom of the page to avoid adding unwanted blank lines
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
