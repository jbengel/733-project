`reduced.csv` (incompatible with Weka) is the Essentia csv data with outliers removed and using the top 250 informative features according to PCA. Refer to `reduce_csv.py` in the `code` folder.

`reduced2.csv` (incompatible with Weka) splits some metadata from the filenames into separate columns.

`reduced3.csv` drops some of said metadata columns - specifically song titles - to allow opening the file in Weka. Also reduces total columns down to 100 to allow for timely analysis.
