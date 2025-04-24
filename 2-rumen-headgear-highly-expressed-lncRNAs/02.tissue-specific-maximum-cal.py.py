#!/bin/python

import pandas as pd

file_path = "tau-generate-output-file-v3-out-lncRNA.csv" 

df = pd.read_csv(file_path, sep="\t")

filtered_df = df[df["tau"] > 0.8]

tissue_columns = df.columns[5:]

results = filtered_df.apply(
    lambda row: {
        "name": row["name"],
        "max_fpkm": row[tissue_columns].astype(float).max(),
        "tissue": tissue_columns[row[tissue_columns].astype(float).argmax()],
    },
    axis=1,
)

print("Results:")
for result in results:
    print(f"Transcript: {result['name']}, Max FPKM: {result['max_fpkm']}, Tissue: {result['tissue']}")

