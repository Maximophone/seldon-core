import json
import os

def find_notebooks(directory='.'):
    ret = []
    for filename in os.listdir(directory):
        if os.path.isdir(directory+'/'+filename) and filename[0]!='.':
            ret += find_notebooks(directory+'/'+filename)
        elif filename[-6:] == ".ipynb":
            ret.append(directory+'/'+filename)
    return ret

def load_notebook(notebook_path):
    with open(notebook_path,'r') as f:
        return json.load(f)

def save_notebook(notebook_path,notebook):
    with open(notebook_path,'w') as f:
        json.dump(notebook,f)
    
def is_clean(notebook):
    return all([cell.get("execution_count") is None for cell in notebook.get("cells")])

def clean_notebook(notebook):
    for cell in notebook.get("cells"):
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            cell["outputs"] = []

if __name__ == "__main__":

    notebook_paths = find_notebooks()
    for notebook_path in notebook_paths:
        notebook = load_notebook(notebook_path)
        if not is_clean(notebook):
            print "Cleaning: {}".format(notebook_path)
            clean_notebook(notebook)
            save_notebook(notebook_path, notebook)
            
