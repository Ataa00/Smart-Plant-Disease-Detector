from dash import dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import os

y_pred = np.load(os.path.abspath('y_test_pred.npy').replace(
    'y_test_pred.npy', "dashApp\\y_test_pred.npy"))
y_true = np.load(os.path.abspath('y_test_true.npy').replace(
    'y_test_true.npy', "dashApp\\y_test_true.npy"))

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
    fig = px.imshow(confusionMatrix, title="Confusion Matrix", text_auto=".2f", # type: ignore
                    color_continuous_scale='Greens', x=class_labels, y=class_labels, aspect="auto")
    fig.layout.height = 700  # type: ignore
    fig.layout.width = 1000  # type: ignore
    fig.layout.xaxis = dict(fixedrange=True)  # type: ignore
    fig.layout.yaxis = dict(fixedrange=True)  # type: ignore

    return fig


def plot_classification_report():
    # Get the number of correct predictions per class
    correct_pred = np.diag(confusionMatrix).tolist()


    # Get the number of incorrect predictions per class
    incorrect_pred = (np.sum(confusionMatrix, axis=0) - correct_pred).tolist()

    # Create a bar chart with grouped bars
    bar_width = 0.4  # Width of each bar
    class_indices = np.arange(len(class_labels))  # Indices for each class

    xlabel = 'Class'
    ylabel = 'Number of predictions'

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=correct_pred, x=class_labels,
                  name="Correct Prediction", marker={"color": 'green'}))
    fig.add_trace(go.Histogram(histfunc="sum", y=incorrect_pred, x=class_labels,
                  name="Incorrect Prediction", marker={"color": 'lightgreen'}))
    fig.update_layout(
        title_text='The Accuracy of the model',  # title of plot
        xaxis_title_text=xlabel,  # xaxis label
        yaxis_title_text=ylabel,  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    fig.layout.xaxis = dict(fixedrange=True)  # type: ignore
    fig.layout.yaxis = dict(fixedrange=True)  # type: ignore
    fig.layout.height = 600  # type: ignore
    fig.layout.width = 1000  # type: ignore
    return fig


def getConfusionMatrixFigure(falsk_app):
    dash_app = dash.Dash(server=falsk_app, name="About",
                         url_base_pathname="/about/")

    dash_app.layout = html.Div(
        id="container",
        style={
            "position": "absolute",
            "left": "0",
            "top": "0",
            "margin": "0",
            "padding": "0",
            "background-image": "url('../static/assests/background-leavs.jpg')",
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
                style={
                    "position": "absolute",
                    "left": "20px",
                    "top": "10px"
                },
                children=[
                    html.Img(
                        src="../static/assests/plant-logo.png",
                        alt="Your Logo"
                    )
                ]
            ),
            html.A(
                id="return",
                style={
                    "position": "absolute",
                    "right": "40px",
                    "top": "20px",
                    "font-size": "15px",
                    "padding": "10px 30px",
                    "font-size": "16px",
                    "font-weight": "bold",
                    "border-radius": "5px",
                    "border": "1px solid #1a852d",
                    "cursor": "pointer",
                    "transition": "0.8s",
                    "color": "#333",
                    "background-color": "white",
                    "z-index": "10",
                    "text-decoration": "none"
                },
                children="Home",
                href="/"
            ),
            html.H1(
                id="title",
                style={
                    "color": "white",
                    "margin-top": "10%"
                },
                children="About our model"
            ),
            html.Div(
                style={
                    "max-width": "500px",
                    "max-height": "500px",
                    "background-color": "white",
                    "padding": "20px",
                    "border-radius": "20px",
                    "margin-bottom": "20px"
                },
                children=[
                    html.P(
                        children="The Image Classifier was trained on a public dataset of plant leaves from kaggle, we used Transfer Learning and PyTorch framework to develop and finetune the model.",
                        style={
                            "font-size": "16px",
                            "color": "#333",
                            "font-weight": "bold"
                        }
                    ),
                    html.P(
                        children="The model achieved an impressive 89% accuracy on the test set, which makes our website's results very reliable.",
                        style={
                            "font-size": "16px",
                            "color": "#333",
                            "font-weight": "bold"
                        }
                    )
                ]
            ),
            html.Div(
                id="cfp",
                style={"display": "flex", "border-radius": "20px", "flex-direction": "column",
                       'margin': 'auto', "align-items": "center", "justify-content": "center"},
                children=[
                    dcc.Graph(
                        id="confusion-matrix",
                        figure=createConfustionMatrix(),
                        style={'width': '100%', 'height': '100%',
                               "border-radius": "20px"}
                    )
                ]
            ),
            html.Div(
                id="crp",
                style={"display": "flex", "border-radius": "20px", "flex-direction": "column", 'margin': 'auto',
                       "align-items": "center", "justify-content": "center", "margin-top": "10px", "margin-bottom": "50px"},
                children=[
                    dcc.Graph(
                        id="Classefication-Report",
                        figure=plot_classification_report(),
                        style={'width': '100%', 'height': '100%',
                               "border-radius": "20px"}
                    )
                ]
            )
        ]
    )

    return dash_app
