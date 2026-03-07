import pandas as pd
#save 

def save_file(_name):
    df = pd.DataFrame(_name, columns=["Category Name", "Category URL"])
    df.to_csv(f"{_name}.csv", index=False)