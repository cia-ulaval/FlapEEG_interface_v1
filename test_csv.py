from eeg_analysis import EEGAnalysis
import numpy as np

# Spécifie le fichier CSV contenant les données EEG
file_path = "data.csv"

# Crée une instance de EEGAnalysis pour charger et analyser les données
eeg_analyzer = EEGAnalysis(file_path)

# Vérifie que les données sont bien chargées
if eeg_analyzer.eeg is not None:
    print("Données EEG prêtes pour l'analyse !")

    # Appliquer les transformations EEG
    entropy_features = eeg_analyzer.compute_band_differential_entropy()
    higuchi_features = eeg_analyzer.compute_higuchi_fractal_dimension()
    psd_features = eeg_analyzer.compute_band_power_spectral_density()

    # Vérifier que les transformations ont bien été effectuées
    if entropy_features is not None and higuchi_features is not None and psd_features is not None:
        # Fusionner les caractéristiques EEG en un seul tableau
        eeg_features = np.concatenate((entropy_features, higuchi_features, psd_features), axis=None)

        # Sauvegarde des caractéristiques
        np.save("features/features_entropy.npy", entropy_features)
        np.save("features/features_higuchi.npy", higuchi_features)
        np.save("features/features_psd.npy", psd_features)
        np.save("features/all_features.npy", eeg_features)

        print("Caractéristiques EEG extraites et sauvegardées dans le dossier 'features/'.")

    else:
        print("Erreur lors du calcul des caractéristiques.")

else:
    print("Erreur : les données EEG ne sont pas disponibles.")
