from plant_model import PlantDisease


def main():
    model = PlantDisease()
    model.load_model()
    print(model.predict(r'D:\AI\Smart Plant Disease Detector\PlantVillage2\test\Potato___healthy\0be9d721-82f5-42c3-b535-7494afe01dbe___RS_HL 1814.JPG', 5))


if __name__ == '__main__':
    main()
