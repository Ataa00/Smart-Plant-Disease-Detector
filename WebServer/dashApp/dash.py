from dash import dash, dcc, html
import plotly.express as px
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import os

y_pred = np.load(os.path.abspath('y_test_pred.npy').replace('y_test_pred.npy', "dashApp\\y_test_pred.npy"))
y_true = np.load(os.path.abspath('y_test_true.npy').replace('y_test_true.npy', "dashApp\\y_test_true.npy"))

confusionMatrix = confusion_matrix(y_true, y_pred)

class_labels = ['Pepper bell Bacterial spot',
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
 'Tomato Target Spot']

def createConfustionMatrix():
    fig = px.imshow(confusionMatrix, title="Confusion Matrix", text_auto=".2f", color_continuous_scale='Greens', x=class_labels, y=class_labels, aspect="auto") # type: ignore
    return fig

def plot_classification_report():
    classificationReport = classification_report(y_true, y_pred, target_names=class_labels)
    number_of_classes=len(class_labels)
    title='Classification Report'
    
    lines = classificationReport.split('\n')

    # drop initial lines
    lines = lines[2:]

    classes = []
    plotMat = []
    support = []
    class_names = []
    for line in lines[: number_of_classes]:
        t = list(filter(None, line.strip().split('  ')))
        if len(t) < 4:
            continue
        classes.append(t[0])
        v = [float(x) for x in t[1: len(t) - 1]]
        support.append(int(t[-1]))
        class_names.append(t[0])
        plotMat.append(v)

    xlabel = 'Metrics'
    ylabel = 'Classes'
    figure_width = 10
    figure_height = len(class_names) + 3
    xticklabels = ['Precision', 'Recall', 'F1-score']
    yticklabels = ['{0} ({1})'.format(class_names[idx], sup)
                   for idx, sup in enumerate(support)]

    fig = px.imshow(np.array(plotMat), labels={"x": xlabel, 'y': ylabel}, text_auto=".2f",  color_continuous_scale='Greens', x=xticklabels, y=yticklabels, aspect="auto", title=title, ) # type: ignore
    return fig

def getConfusionMatrixFigure(falsk_app):
    dash_app = dash.Dash(server=falsk_app, name="About", url_base_pathname="/about/")

    dash_app.layout = html.Div(
        children=[
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
