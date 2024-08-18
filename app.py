from dash import Dash, dcc, html, Input, Output
import pathlib
import plotly.express as px


import pandas as pd

app = Dash(__name__)

markdown_text = '''
### Green Solvents vs Efficiency

This is an app dedicated to documenting the effort of transitioning organic solar
cells towards greener solvent alternatives
For more information about green solvents selection visit this [Link](http://www.omegalabresearch.com/resources)
specifying the rules for green solvent transition.

You can hover over each point to find out more about the donor:acceptor blend,
the solvent utilized, efficiency, and toxicity (LD50). Click on the desired point to
guide you to the according reference. 

To submit a device of your own, please fill out [This Form](https://forms.gle/ATUbVjaewMWvgL5s5).
We will revise each submission and add it to this graph accordingly. 
'''
     
blackbold={'color':'black', 'font-weight': 'bold'}

server = app.server



# read from datasheet

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()
#DATA_PATH = pathlib.Path(__file__).parent.joinpath("oe-1/data").resolve()
df = pd.read_csv(DATA_PATH.joinpath("GreenSolvents_Literaturereview.csv"))

          
# Plot the Data
fig = px.scatter(df, x="LD50", y="PCE", labels={'LD50':'LD50 (mg/kg)','PCE':'PCE (%)'},
                 color="Type",symbol="Type",  hover_name="System", hover_data=["Solvent"], custom_data = ['URL'], 
                 log_x=True, size_max=60)
           
# create the layout

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map


   html.Div([
        html.Div([


      # Logo

            html.Div(
            [html.Img(src=app.get_asset_url("kaust-logo.png"))], className="app__banner" #thiis logo can be replaced for something else
            ),
    
           
            html.Div([
            dcc.Markdown(children=markdown_text)
            ]),

       # Web_link
            html.Br(),
            html.Label(['Selected Reference URL:'],style=blackbold),
            html.Pre(id='web_link', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px'}
            ),

            #Image Below URL

            html.Div(
            [html.Img(src=app.get_asset_url("omega-lab-01.png"))], className="app__banner" #thiis logo can be replaced for something else
            ),


        ], className='three columns'
        ),


        # Graph
        html.Div([
             dcc.Graph(id='Solvents', figure=fig, config={'displayModeBar': True, 'scrollZoom': True},
                style={'background':'#969998','padding-bottom':'2px', 'padding-top':'2px','padding-left':'2px','padding-right':'2px','height':'80vh'}
            ),

            #Image Below Graph
             #html.Div(
            #[html.Img(src=app.get_asset_url("kaust-logo.png"))], className="app__banner" #thiis logo can be replaced for something else
            #),


        ], className='nine columns'
        ),




    ], className='row'
    ),


], className='ten columns offset-by-one'
)


# callback for Web_link
@app.callback(
    Output('web_link', 'children'),
    [Input('Solvents', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:
         #print (clickData)
        the_link=clickData['points'][0]['customdata'][0]
        if the_link is None:
            return 'No Website Available'
        else:
            return html.A(the_link, href=the_link, target="_blank")


if __name__ == '__main__':
    app.run_server(debug=False)
