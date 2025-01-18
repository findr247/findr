import tensorflow
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.layers import GlobalMaxPool2D
import cv2
import numpy as np
from numpy.linalg import norm
from io import BytesIO
from sklearn.neighbors import NearestNeighbors
from .models import ItemImage


class ImageFilter:
    model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model.trainable = False

    def __init__(self):
        self.model = tensorflow.keras.Sequential([
            self.model,
            GlobalMaxPool2D()
        ])
        self.model.summary()
        for image in ItemImage.objects.filter(features=None):
            print(image.image.url[1:])
            features = self.get_feature(image.image.url[1:])
            print(features)
            image.features = features.tolist()
            image.save()

    def get_feature(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        img = np.array(img)
        return self.predict_features(img)

    def predict_features(self, img):
        expand_img = np.expand_dims(img, axis=0)
        pre_img = preprocess_input(expand_img)
        result = self.model.predict(pre_img).flatten()
        normalized = result / norm(result)
        return normalized

    def nearest_neighbors(self, array, data=ItemImage.objects.all()):
        feature_list = np.array([item.features_data() for item in data])
        input_features = self.predict_features(array)

        neighbors = NearestNeighbors(n_neighbors=2, algorithm='brute', metric="euclidean")
        neighbors.fit(feature_list)

        distance, index = neighbors.kneighbors([input_features])

        print(index[0])
        return [data[int(i)] for i in index[0]]


