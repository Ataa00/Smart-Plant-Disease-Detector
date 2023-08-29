from plant_model import PlantDisease
from os import path


def main():
    model = PlantDisease()
    model.load_model()

    img_path = path.realpath(
        r'MachineLaearningModel\Smart_Plant_Disease_Detector\Smart Plant Disease Detector\PlantVillage2\test\Pepper__bell___Bacterial_spot\3a03526d-0bf4-4898-9f0f-8a9c31afd3eb___JR_B.Spot 3380.JPG')

    values, classes = model.predict(
        img_path, 3)

    for img_pr, img_class in zip(values.numpy()[0], classes):
        print(f'{img_class}: {(img_pr * 100):.2f}%')


if __name__ == '__main__':
    main()
