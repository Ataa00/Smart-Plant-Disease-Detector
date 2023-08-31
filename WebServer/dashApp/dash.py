from dash import dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import os

y_pred = np.load(os.path.abspath('y_test_pred.npy').replace('y_test_pred.npy', "dashApp\\y_test_pred.npy"))
y_true = np.load(os.path.abspath('y_test_true.npy').replace('y_test_true.npy', "dashApp\\y_test_true.npy"))

confusionMatrix = confusion_matrix(y_true, y_pred)

class_labels = [
    'Pepper bell Bacterial spot',
    'Pepper bell healthy',
    'Potato Early blight',
    'Potato Late blight',
    'Potato healthy',
    'Tomato Bacterial spot',
    'Tomato Early blight',
    'Tomato Late blight',
    'Tomato Leaf Mold',
    'Tomato Septoria leaf spot',
    'Tomato Spider mites Two spotted spider mite',
    'Tomato Target Spot'
    ]

def createConfustionMatrix():
    fig = px.imshow(confusionMatrix, title="Confusion Matrix", text_auto=".2f", color_continuous_scale='Greens', x=class_labels, y=class_labels, aspect="auto") # type: ignore
    fig.layout.height = 700
    fig.layout.width = 1000

    return fig

def plot_classification_report():
    # Get the number of correct predictions per class
    correct_pred = np.diag(confusionMatrix).tolist()
    
    # Get the number of incorrect predictions per class
    incorrect_pred = (np.sum(confusionMatrix, axis=0) - correct_pred).tolist()
    print(incorrect_pred)

    # Create a bar chart with grouped bars
    bar_width = 0.4  # Width of each bar
    class_indices = np.arange(len(class_labels))  # Indices for each class

    xlabel = 'Class'
    ylabel = 'Number of predictions'

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=correct_pred, x=class_labels, name="Correct Prediction", marker= {"color": 'green'}))
    fig.add_trace(go.Histogram(histfunc="sum", y=incorrect_pred, x=class_labels, name="Incorrect Prediction", marker= {"color": 'lightgreen'}))
    fig.update_layout(
    title_text='The Accuracy of the model', # title of plot
    xaxis_title_text=xlabel, # xaxis label
    yaxis_title_text=ylabel, # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    fig.layout.height = 600
    fig.layout.width = 1000
    return fig

def getConfusionMatrixFigure(falsk_app):
    dash_app = dash.Dash(server=falsk_app, name="About", url_base_pathname="/about/")

    dash_app.layout = html.Div(
        id="container",
        style={
            "background-image": "url('../static/assests/background-leavs.jpg')",
            "margin": "auto",
            "display": "flex",
            "flex-direction": "column",
            "width": "100%",
            "justify-content": "center",
            "align-items": "center",
            "background-repeat": "no-repeat",
            "background-size": "cover"
        },
        children=[
            html.Div(
                id="header",
                className="logo",
                children=[
                    html.Img(
                        src="../static/assests/plant-logo.png",
                        alt="Your Logo"
                    )
                ]
            ),
            html.H1(
                id="title",
                className="aboutTitle",
                children="About our model"
            )
            ,
            dcc.Graph(
            id="confusion-matrix",
            figure= createConfustionMatrix()
            ),
            dcc.Graph(
            id="Classefication-Report",
            figure= plot_classification_report()
            )
        ]
    )

    return dash_app
