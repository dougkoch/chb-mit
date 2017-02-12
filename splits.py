import numpy as np
from patient import Patient
import random

# Generates splits within one patient (defaults to 80%/10%/10% train/val/test)
def intra_patient_split(patient_id, train_frac=0.8, val_frac=0.1):
    p = Patient(patient_id)
    seizures = p.get_seizures()
    clips = p.get_seizure_clips()

    test_frac = 1.0 - train_frac - val_frac

    n_val_seizures = max(1, int(round(val_frac * len(seizures))))
    n_test_seizures = max(1, int(round(test_frac * len(seizures))))
    n_train_seizures = len(seizures) - n_val_seizures - n_test_seizures

    return (
        # Training clips
        clips[:n_train_seizures],

        # Validation clips
        clips[n_train_seizures : n_train_seizures + n_val_seizures],
        
        # Test clips
        clips[n_train_seizures + n_val_seizures:]
    )

# Generates splits across patients
def inter_patient_split(n_train_patients, n_val_patients, n_test_patients):
    patient_ids = [id for id in range(1, 25)]
    random.shuffle(patient_ids)

    patients = [Patient(id) for id in patient_ids[:n_train_patients + n_val_patients + n_test_patients]]    

    x_train = x_val = x_test = np.zeros((0, 26))
    y_train = y_val = y_test = np.array([])

    for patient in patients[:n_train_patients]:
        x_train = np.vstack((x_train, patient.get_eeg_data()))
        y_train = np.vstack((y_train, patient.get_seizure_labels()))

    for patient in patients[n_train_patients:n_train_patients + n_val_patients]:
        x_val = np.vstack((x_val, patient.get_eeg_data()))
        y_val = np.vstack((y_val, patient.get_seizure_labels()))
    
    for patient in patients[n_train_patients + n_val_patients:]:
        x_test = np.vstack((x_test, patient.get_eeg_data()))
        y_test = np.vstack((y_test, patient.get_seizure_labels()))

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)
