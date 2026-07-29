import json

path = r"d:\fare_prediction\notebooks\02_model_training.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

modified = False
for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            if "bike_prediction['Estimated Duration (min)']" in line:
                modified = True
                continue
            if "bike_prediction['Weather Condition']" in line:
                modified = True
                continue
            new_source.append(line)
        cell['source'] = new_source

if modified:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Notebook updated successfully.")
else:
    print("No changes made.")
