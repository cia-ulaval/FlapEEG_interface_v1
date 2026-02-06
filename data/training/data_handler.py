import numpy as np
import pandas as pd
import warnings

from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix as sk_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import seaborn as sns

warnings.simplefilter(action='ignore', category=FutureWarning)

NUM_EEG_CHANNELS = 16

FILES =["patient001_session1.csv", "patient002_session1.csv", "patient003_session1.csv",
        "patient004_session1.csv", "patient005_session1.csv", "patient006_session1.csv",
        "patient007_session1.csv",
        "patient001_session2.csv", "patient002_session2.csv", "patient003_session2.csv",
        "patient004_session2.csv", "patient005_session2.csv", "patient006_session2.csv",
        "patient007_session2.csv"]

STATE_MAPPING = {
    0.0: 'no blink',
    1.0: 'blink'
}

CUSTOM_PALETTE = {
    'no blink': '#007BFF',  # blue
    'blink': '#e74c3c'  # red
}

class DataHandler:
    def __init__(self)->None:
        self.dataset = None #list of dataframes for each treated csv

        self.__FILES = FILES
        self.patients = self.regroup_patients()

    def regroup_patients(self)->list:
        patients = []
        for file in self.__FILES:
            data = self.__csv_handler(file)
            patients.append(data)
        return patients

    def __csv_handler(self, csv_file):
        data = pd.read_csv(csv_file)
        num_cols = data.shape[1]
        n_channels_in_file = 16 if num_cols >= 30 else 8
        n_channels = min(n_channels_in_file, NUM_EEG_CHANNELS)
        eeg_col_indices = list(range(1, n_channels + 1)) + [-1]
        data = data.iloc[:, eeg_col_indices]
        channel_names = [f'ch{i}' for i in range(1, n_channels + 1)] + ['blink']
        data.columns = channel_names
        if n_channels < NUM_EEG_CHANNELS:
            for i in range(n_channels + 1, NUM_EEG_CHANNELS + 1):
                data[f'ch{i}'] = 0
            cols = [f'ch{i}' for i in range(1, NUM_EEG_CHANNELS + 1)] + ['blink']
            data = data[cols]
        data['blink'].replace({-44.0: 0, 44.0: 1}, inplace=True)
        data = data.iloc[:-20]
        ones_df = data[data['blink'] == 1]  # Keep all 1s
        num_ones = len(ones_df)
        zeros_df = data[data['blink'] == 0].sample(n=num_ones * 2, replace=False,
                                                   random_state=42)  # 33% blink, 66% no blink
        data = pd.concat([ones_df, zeros_df]).sort_index().reset_index(drop=True)
        return data

    def load_data(self)->list:
        self.dataset = self.regroup_patients()
        return self.dataset

def generate_trainSet(training_sample)->tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dataset = pd.DataFrame()
    for patient in training_sample:
        dataset = pd.concat([dataset, patient], ignore_index=True)
    channel_names = [f'ch{i}' for i in range(1, NUM_EEG_CHANNELS + 1)]
    data = dataset[channel_names]
    annotations = dataset[["blink"]]
    X_train, X_test, y_train, y_test = train_test_split(data, annotations.values.ravel(),
                                                        test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def performance(model, X_train, X_test, y_train, y_test)->None:
    print(f"training performance = {model.score(X_train, y_train) * 100:.3f}%")
    print(f"test performance = {model.score(X_test, y_test) * 100:.3f}%")
    return None

def confusion_matrix(model, X_test, y_test)->None:
    y_pred = model.predict(X_test)  # save predicted values
    cm = sk_confusion_matrix(y_test, y_pred)  # create confusion matrix
    cm_normalized = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]) * 100  # switch to percentages

    cmd = ConfusionMatrixDisplay(confusion_matrix=cm_normalized)  # create a display
    # Plot the confusion matrix
    plt.figure(figsize=(10, 8))  # This also defines 'fig' properly
    cmd.plot(cmap=plt.cm.Blues)
    plt.title('Confusion Matrix in percentage')
    plt.show()
    return None

def boxplot(dataset)->None:
    df = pd.concat(dataset)
    n_plot = min(4, NUM_EEG_CHANNELS)
    fig, axes = plt.subplots(1, n_plot, figsize=(4 * n_plot, 6))
    if n_plot == 1:
        axes = [axes]
    channel_names = [f'ch{i}' for i in range(1, NUM_EEG_CHANNELS + 1)]
    for i, ax in enumerate(axes):
        sns.boxplot(x='blink', y=channel_names[i], data=df, ax=ax)
        ax.set_title(f'{channel_names[i]} by state')
    plt.tight_layout()
    plt.show()
    return None

def pca_drawer(dataset)->None:
    df = pd.concat(dataset)
    features = [f'ch{i}' for i in range(1, NUM_EEG_CHANNELS + 1)]
    x = df.loc[:, features].values
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)

    principal_df = pd.DataFrame(data=principal_components,
                                columns=['Principal Component 1', 'Principal Component 2'],
                                index=df.index)

    principal_df['blink'] = df['blink']

    principal_df['blink'] = df['blink'].map(STATE_MAPPING)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='Principal Component 1',
        y='Principal Component 2',
        hue='blink',
        data=principal_df,
        palette= CUSTOM_PALETTE,
        style='blink',
        markers={'no blink': 'o', 'blink': 'X'},
        sizes={'no_blink': 300, 'blink': 400},
        alpha=0.8,
        edgecolor='w'
    )

    plt.title(f'PCA of {NUM_EEG_CHANNELS} EEG channels (Standardized)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
    return None

def pie_chart(dataset):
    df = pd.concat(dataset)
    df['blink'] = df['blink'].map(STATE_MAPPING)

    blink_counts = df['blink'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(blink_counts, labels=blink_counts.index, autopct='%1.1f%%', startangle=140,
            colors=[CUSTOM_PALETTE[label] for label in blink_counts.index])

    plt.title('Distribution of Blink and No Blink Categories')
    plt.show()

    return None

def results_evolution(results):
    training_performance, testing_performance = zip(*results)
    x = range(1, len(training_performance) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(x, training_performance, label='Model Training Performance', marker='o')
    plt.plot(x, testing_performance, label='Model Testing Performance', marker='o')

    plt.title('Model Training and Testing Performance')
    plt.xlabel('Model Iteration')
    plt.ylabel('Performance (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return None








