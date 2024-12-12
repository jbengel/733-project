import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import numpy as np

def find_outliers3(data):
    df = data.copy()
    train_samples = df.values.tolist()

    # Fit One-Class SVM
    estimator = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma="scale")
    estimator.fit(train_samples)
    pred = estimator.predict(train_samples)

    outlier_indices = [i for i, val in enumerate(pred) if val == -1]
    return outlier_indices

# In/out
source_csv = "../data/essentia_csv/initial.csv"
output_csv = "../data/reduced.csv"

# Specific columns to retain per organizational/speculative needs
columns_to_retain = [
    "metadata.tags.file_name",
    "lowlevel.spectral_centroid.dmean",
    "lowlevel.spectral_centroid.dmean2"
]

# Load the data
data = pd.read_csv(source_csv)

# Whitelist certain columns
data_retain = data[columns_to_retain] #TODO refactor

# Filter to only numeric columns
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
numeric_columns = [col for col in numeric_columns if col not in columns_to_retain]
data_numeric = data[numeric_columns]

# Identify non-numeric columns being excluded
non_numeric_columns = [col for col in data.columns if col not in numeric_columns]
print("Non-numeric columns being excluded:")
for col in non_numeric_columns:
    print(f"- {col}")

# Drop outliers
outlier_indices = find_outliers3(data_numeric)
for i in outlier_indices:
    name = data["metadata.tags.file_name"][i]
    print(f"Dropping outlier: {name}")
l1 = len(data_numeric)
data_numeric = data_numeric.drop(index=outlier_indices).reset_index(drop=True)
data_retain = data_retain.drop(index=outlier_indices).reset_index(drop=True)
data = data.drop(index=outlier_indices).reset_index(drop=True)
l2 = len(data_numeric)
print(f"Had {l1} rows; have {l2} rows.")
print(f"Dropped {len(outlier_indices)} outliers.")
assert(len(data_numeric) == len(data_retain))

# Standardize & apply PCA
scaler = StandardScaler()
data_pca_scaled = scaler.fit_transform(data_numeric)
pca = PCA()
pca.fit(data_pca_scaled)

# Determine the top features
n_features_to_select = 250
absolute_loadings = np.abs(pca.components_).sum(axis=0)
top_features_idx = np.argsort(absolute_loadings)[-n_features_to_select:][::-1]
top_features = [numeric_columns[idx] for idx in top_features_idx]

print(f"Top {n_features_to_select} features selected based on PCA:")
for feature in top_features:
    print(f"- {feature}")

# Combine retained columns and selected PCA features
final_data = pd.concat([data_retain, data[top_features]], axis=1) #TODO refactor

# Save the final dataset
final_data.to_csv(output_csv, index=False)

print(f"Reduced dataset saved to '{output_csv}'.")

