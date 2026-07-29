import json

path = r"d:\fare_prediction\notebooks\02_model_training.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

modified = False
for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("bike_prediction['Distance (km)']" in line for line in source):
            new_source = []
            for line in source:
                new_source.append(line)
                if "bike_prediction['Distance (km)']" in line:
                    new_source.append("bike_prediction['Estimated Duration (min)'] = 30\n")
                    modified = True
                if "# Normal conditions\n" in line:
                    new_source.append("bike_prediction['Weather Condition'] = 0        # Clear\n")
                    modified = True
            cell['source'] = new_source

if modified:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Changes reverted successfully.")
else:
    print("Cell not found.")
