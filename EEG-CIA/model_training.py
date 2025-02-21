from sklearn.ensemble import RandomForestClassifier
from data_handler import DataHandler, generate_trainSet
data_handler = DataHandler()

class RandomForestModel:

    def __init__(self, dataset)->None:
        model = RandomForestClassifier()
        self.DATASET_LENGTH = len(dataset)
        self.LIST_OF_SETS = [i for i in range(2, self.DATASET_LENGTH + 2, 2)]
        self.models = []
        self.dataset = dataset


    def __model_training(self, X_train, y_train)->RandomForestClassifier:
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        return model

    def train_model_per_set(self)-> tuple[list, list]:
        models = []
        results = []
        for index in self.LIST_OF_SETS:

            training_sample = self.dataset[0:index]
            X_train, X_test, y_train, y_test = generate_trainSet(training_sample)
            model = self.__model_training(X_train, y_train)
            models.append(model)
            results.append((model.score(X_train, y_train) * 100, model.score(X_test, y_test) * 100))

        return models, results

