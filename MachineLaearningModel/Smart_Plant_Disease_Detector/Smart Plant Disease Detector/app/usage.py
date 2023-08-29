from plant_model import PlantDisease
from os import path


def main():
    model = PlantDisease()
    model.load_model()

    img_path = path.abspath('Tomato_Sick.jpeg')

    values, classes = model.predict(
        img_path, 3)

    for img_pr, img_class in zip(values.numpy()[0], classes):
        print(f'{img_class}: {(img_pr * 100):.2f}%')


if __name__ == '__main__':
    main()
