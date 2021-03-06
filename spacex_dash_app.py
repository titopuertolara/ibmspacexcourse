# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df['label']=spacex_df['class'].apply(lambda  x: 'succesful' if x==1 else 'Failed')
spacex_df['Payload Mass (kg)']=spacex_df['Payload Mass (kg)'].apply(pd.to_numeric,errors='coerce')
launch_site=spacex_df['Launch Site'].unique().tolist()
launch_site.append('all')
#print(spacex_df['class'].head())
# Create a dash application
app = dash.Dash(__name__)
marks_={i:str(i) for i in range(0,20001,1000)}
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div( dcc.Dropdown(id='site-dropdown',value='all',options=[{'label':i,'value':i} for i in launch_site])),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',marks=marks_,min=0,max=10000,step=2500,value=[2500,5000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure'),
              [Input('site-dropdown','value')])
def render_pie(site):
	
	
	if site=='all':
		succes_df=spacex_df[spacex_df['label']=='succesful']
		g_succes_df=succes_df.groupby(['Launch Site']).count()[['label']].reset_index()
		#print(g_succes_df)
		fig = px.pie(g_succes_df, values='label', names='Launch Site')
		fig.update_layout(title='succesful launches for each launch site')
	else:
		launch_df=spacex_df[spacex_df['Launch Site']==site]
		#print(launch_df)
		grouped_df=launch_df.groupby(['label']).count()[['Launch Site']].reset_index()
		#print(grouped_df)
		fig = px.pie(grouped_df, values='Launch Site', names='label')
		fig.update_layout(title=f'succesful vs failed for {site} ')
		
	return fig
	
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart','figure'),
              [Input('site-dropdown','value'),
               Input('payload-slider','value')])
def show_scatter_plot(dvalue,svalue):
	print(svalue)
	df=spacex_df[(spacex_df['Payload Mass (kg)']>=svalue[0]) & (spacex_df['Payload Mass (kg)']<=svalue[1])]
	#print(spacex_df)
	if dvalue=='all':
		fig=px.scatter(df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
	else:
		df=df[spacex_df['Launch Site']==dvalue]
		fig=px.scatter(df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
		
	return fig
		
	

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
