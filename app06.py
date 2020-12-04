
#importing the libraries
import pandas as pd
import webbrowser
# !pip install dash
import dash
import dash_html_components as html
from dash.dependencies import Input, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate
#for drop down
 #for graph 1st method come to create app UI
#2nd method for graph


# Declaring Global variables
# A variable declared outside a function is a global variable by default.
# Declaring Global variable
# Two types of variable local and global variable
app = dash.Dash()
project_name = None
#way to intialize dash to create object in python will create a blank webpage
# Defining My Functions
def load_data():
    dataset_name = "global_terror1.csv"
  #Concept similar to c i.e null language you are creating a variable initialising is with null so in python we use none to examplate null value
# its a global variable as diclairmed outside function
    
    global df
    df = pd.read_csv(dataset_name)
    
  
    global month_list
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }
    month_list= [{"label":key, "value":values} for key,values in month.items()]
  
    global date_list
    date_list = [x for x in range(1, 32)]
  
  
    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
  
  
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
  
  
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()
  
  
    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  
  
    global year_list
    year_list = sorted ( df['iyear'].unique().tolist()  )
  
    global year_dict
    year_dict = {str(year): str(year) for year in year_list}
    
    #chart dropdown options
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                               "Target Nationality":'natlty1_txt', 
                               "Target Type":'targtype1_txt', 
                               "Type of Attack":'attacktype1_txt', 
                               "Weapon Type":'weaptype1_txt', 
                               "Region":'region_txt', 
                               "Country Attacked":'country_txt'
                            }
                                
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
  
def open_browser():
    # Open the default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div([
    html.H1('Terrorism Analysis with Insights.', id='Main_title'),
    dcc.Tabs(id="Tabs", value="Map",children=[
        dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
            dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
                dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                ]),
            dcc.Dropdown(
                id='month-dropdown', 
                  options=month_list,
                  placeholder='Select Month',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='date-dropdown', 
                  placeholder='Select Day',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='region-dropdown', 
                  options=region_list,
                  placeholder='Select Region',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='country-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  placeholder='Select Country',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='state-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  placeholder='Select State or Province',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='city-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  placeholder='Select City',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='attacktype-dropdown', 
                  options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select Attack Type',
                  multi = True
                    ),
  
            html.H5('Select the Year', id='year_title'),
            dcc.RangeSlider(
                      id='year-slider',
                      min=min(year_list),
                      max=max(year_list),
                      value=[min(year_list),max(year_list)],
                      marks=year_dict,
                      step=None
                        ),
            html.Br()
      ]),
        dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
            dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
                dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
              dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
              html.Br(),
              html.Br(),
              dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
              html.Br(),
              html.Br(),
              html.Hr(),
              dcc.Input(id="search", placeholder="Search Filter"),
              html.Hr(),
              html.Br(),
              dcc.RangeSlider(
                      id='cyear_slider',
                      min=min(year_list),
                      max=max(year_list),
                      value=[min(year_list),max(year_list)],
                      marks=year_dict,
                      step=None
                        ),
                    html.Br()
                ]),
           ]),
    dcc.Loading(dcc.Graph(id='graph-object', figure = go.Figure()))
    ])
          
    return main_layout
  
  #Create a new call back for change eventso now mutiple callback
#we have twonames same update app ui why it is possible due to call back function and both are attached their own app call backs. but prefer always to give different name

# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'figure'),
    [
    Input("Tabs", "value"),
    Input('month-dropdown', 'value'),
    Input('date-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('state-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('attacktype-dropdown', 'value'),
    Input('year-slider', 'value'), 
    Input('cyear_slider', 'value'), 
    
    Input("Chart_Dropdown", "value"),
    Input("search", "value"),
    Input("subtabs2", "value")
    ]
    )
#when drop down is changed value is passed from def function more the inputs more will be the arguments in def
def update_app_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search, subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        #for a favicon we need to convert .png to .ico file 
# www.favicon.cc will give an option to convert file
# an ico file is 16*16 image.
#paste in assets name folder in same directory  
                       #name and age in list of list first part in x axis second in y axis 
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        
         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure
#read express plotly
    elif Tabs=="Chart":
        fig = None
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        fig = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)

    return fig

#Defining my functions
#how to calll a function write some code in main 
#call backs are called in if the function is not fired the call back will be called so put if and else condition.


@app.callback(
    Output("date-dropdown", "options"),
    [Input("month-dropdown", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option
#put up comma after every attribute or tags to create a UI using python as a language you can create a webpage. only you need to know html attributes
#if some body click the buton we have to change the title.
@app.callback(
    [Output("region-dropdown", "value"),
    Output("region-dropdown", "disabled"),
    Output("country-dropdown", "value"),
    Output("country-dropdown", "disabled")],
    [Input("subtabs", "value")]
    )
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
    # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
    # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]


# Main Function to control the Flow of your Project
def main():
    load_data()
    
    open_browser()
    
    global project_name
    project_name = "Terrorism Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
    app.run_server() # debug=True
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None
#put up comma after every attribute or tags to create a UI using python as a language you can create a webpage. only you need to know html attributes
#if some body click the buton we have to change the title.

if __name__ == '__main__':
    main()
    '''
    Clicks the button 
    what is the task to update the button this click is event and web browser has to respond it.
    so we need to make a function.
    if somebody clicks function has to be called
    named update app ui
    event                       object
    click on the button 
    wiring when press button or an event or an object== function has to be called
    so we need to check how many times somebody clicked button so there is function n_clicks its a system variable)
    so intitially value of n_clicks will be zero as it will keep check on it.
    
    Day 8 
    how to wire this control of call bags
    method in python = decorator
    use
    @app.callback()
    Input which is object on which event is happening
    Output what would be output
    Input 'button_close'  'nclicks'#how many times clicked
    Output "button_close"(object)   'children'#what should change
    from dash.dependencies import Input , Output
    #you cannot make industry without using call backs function
    '''
    
    '''
    Day 9
    agenda:
        >> graph
        Use dash and using dash how you can create graph
        2. Drop down (we can give any default value.)in drop down list there is options when we select an option graph is seen.
        3. an dark line.
        4. how to draw drop down and graph
        #import library non html components i.e dsh core components as dcc
        #there are two method two plot a graph 1st library plotly.graph_objects as go
        second libary plotly.express
        option and value for default search.
        now for a bar fraph and line graph we need to go for a call back
    '''

    '''
    Day 10
    Agwnda: 
        >> Data preparation and UI to meet client expetation
    '''
    '''
    Day 11
    Agenda
       ..Dropdown and its callback with world map
       
    '''
    '''
    Day 13
    Agenda
    ..Multicselect of dropdown and tabs introduction
    ..Solo Development
    
    '''
    
    '''
    Day 14
    India Chart tool
    
    '''
    
    

