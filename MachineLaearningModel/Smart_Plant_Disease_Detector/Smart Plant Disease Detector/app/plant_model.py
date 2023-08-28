import numpy as np

from PIL import Image

import torch
from torchvision import models
import os


class PlantDisease:
    def __init__(self):
        self._model = None
        self._model_path = r'D:\AI\Smart Plant Disease Detector\app\densenet121-checkpoint.pth'
        self._change_cwd_to_closest_folder()

    def _change_cwd_to_closest_folder(self):
        current_dir = os.getcwd()
        closest_dir = os.path.dirname(current_dir)
        os.chdir(closest_dir)

    def load_model(self):
        model_checkpoint = torch.load(self._model_path)
        model = models.densenet121(
            weights=models.DenseNet121_Weights.DEFAULT)

        model.classifier = model_checkpoint['classifier']
        model.load_state_dict(model_checkpoint['state_dict'])
        model.class_to_idx = model_checkpoint['mapping']
        self._model = model

    def process_image(self, image):
        ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
            returns an Numpy array
        '''
        width, height = image.size

        if width < height:
            image = image.resize((256, 256*height//width))
        else:
            image = image.resize((256*width//height, 256))

        width, height = image.size
        reduce = 224
        left = (width - reduce)/2
        top = (height - reduce)/2
        right = left + 224
        bottom = top + 224
        im = image.crop((left, top, right, bottom))

        np_image = np.array(im)/255
        np_image -= np.array([0.485, 0.456, 0.406])
        np_image /= np.array([0.229, 0.224, 0.225])

        np_image = np_image.transpose((2, 0, 1))
        return np_image

    def predict(self, image_path, topk=5):
        ''' Predict the class (or classes) of an image using a trained deep learning model.
        '''
        image = Image.open(image_path)
        image = torch.from_numpy(self.process_image(image)).type(
            torch.FloatTensor)  # type: ignore

        with torch.no_grad():
            self._model.to('cpu')

            # we're using unsqueeze to add a batch dimension so that it wpuld be compatible with the model
            self._model.eval()
            log_ps = self._model.forward(image.unsqueeze(0))

        ps = torch.exp(log_ps)
        values, indices = ps.topk(topk)

        idx_to_class = {val: key for key,
                        val in self._model.class_to_idx.items()}

        indices = indices.cpu()
        values = values.cpu()

        classes = [idx_to_class[idx] for idx in indices.numpy()[0].tolist()]

        return values, classes
