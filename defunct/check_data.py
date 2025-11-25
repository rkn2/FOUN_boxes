import pandas as pd

file_path = '/Users/rebeccanapolitano/antigravityProjects/FOUN/FOUN_boxes/2023_12_8_targeted_eval.csv'
try:
    df = pd.read_csv(file_path)
    print("Columns:", df.columns.tolist())
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nShape:", df.shape)
except Exception as e:
    print(e)
