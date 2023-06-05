## 執行指令：flask --app app run --debug (--debug有打才會更新) 其實打flask run就可以
## .\venv\Scripts\activate.bat

# 資料從Flask copy
from flask import Flask,render_template
import plotly.express as px
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
import urllib
from skimage import data
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from urllib.request import urlopen




app = Flask(__name__)

@app.route("/")
def index1():
    N = 50
    fig = go.Figure(data=[go.Mesh3d(x=(30*np.random.randn(N)),
                    y=(25*np.random.randn(N)),
                    z=(30*np.random.randn(N)),
                    opacity=0.5,)])

    # xaxis.backgroundcolor is used to set background color
    fig.update_layout(scene = dict(
                        xaxis = dict(
                            backgroundcolor="rgb(200, 200, 230)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",),
                        yaxis = dict(
                            backgroundcolor="rgb(230, 200,230)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white"),
                        zaxis = dict(
                            backgroundcolor="rgb(230, 230,200)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",),),
                        width=1000,
                        height=700,
                        margin=dict(
                        r=10, l=10,
                        b=100, t=10)
                    )    
    
    # N = 50
    # fig1 = go.Figure()
    # fig1.add_trace(go.Mesh3d(x=(60*np.random.randn(N)),
    #                 y=(25*np.random.randn(N)),
    #                 z=(40*np.random.randn(N)),
    #                 opacity=0.5,
    #                 color='yellow'
    #                 ))
    # fig1.add_trace(go.Mesh3d(x=(70*np.random.randn(N)),
    #                 y=(55*np.random.randn(N)),
    #                 z=(30*np.random.randn(N)),
    #                 opacity=0.5,
    #                 color='pink'
    #                 ))

    # fig1.update_layout(scene = dict(
    #                     xaxis_title='X AXIS TITLE',
    #                     yaxis_title='Y AXIS TITLE',
    #                     zaxis_title='Z AXIS TITLE'),
    #                     width=700,
    #                     margin=dict(r=20, b=10, l=10, t=10))
    
    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder) #傳出json字串給graphJSON
    return render_template('index1.jinja.html',graphJSON=graphJSON)



@app.route("/index2")
def index2():
    ## 汽泡圖
    # df = px.data.gapminder()
    # fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
    #             size="pop", color="continent",
    #                 hover_name="country", log_x=True, size_max=60)
    ## 照片
    # img = data.astronaut()
    # fig = px.imshow(img, binary_format="jepg", binary_compression_level=0)

## 3張照片
    img_path1 = "02.jpg"
    img1 = Image.open(img_path1)  # 使用PIL打開圖片
    fig1 = px.imshow(img1)
    # img2 = data.astronaut()
    # fig2 = px.imshow(img2, binary_format="jpeg", binary_compression_level=0)
    img_path2 = "04.jpg"
    img2 = Image.open(img_path2)  # 使用PIL打開圖片
    fig2 = px.imshow(img2)
    img_path3 = "03.jpg"
    img3 = Image.open(img_path3)  # 使用PIL打開圖片
    fig3 = px.imshow(img3)

    # 包含3圖表的子圖容器
    fig = make_subplots(rows=1, cols=3)
    fig.add_trace(fig1.data[0], row=1, col=1)
    fig.add_trace(fig2.data[0], row=1, col=2)
    fig.add_trace(fig3.data[0], row=1, col=3)

    fig.update_layout(height=700, width=1800,autosize=True,)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index2.jinja.html', graphJSON=graphJSON)    



@app.route("/index3")
def index3():
    df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/sunburst-coffee-flavors-complete.csv')
    df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        ids=df1.ids,
        labels=df1.labels,
        parents=df1.parents,
        domain=dict(column=0)
    ))

    fig.add_trace(go.Sunburst(
        ids=df2.ids,
        labels=df2.labels,
        parents=df2.parents,
        domain=dict(column=1),
        maxdepth=2
    ))

    fig.update_layout(
        grid= dict(columns=2, rows=1),
        margin = dict(t=0, l=0, r=0, b=0)
    )
    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder) #傳出json字串給graphJSON
    return render_template('index3.jinja.html',graphJSON=graphJSON)


@app.route("/index4")
def index4():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                    dtype={"fips": str})

    fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
                                        colorscale="Viridis", zmin=0, zmax=12,
                                        marker_opacity=0.5, marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(height=600)

    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder) #傳出json字串給graphJSON
    return render_template('index4.jinja.html',graphJSON=graphJSON)