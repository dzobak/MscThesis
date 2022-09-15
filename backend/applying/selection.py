import pandas as pd
import re

def split(scope:str, sep:str):
    return scope.split(sep)

def compare_paths(path1, path2):
    print(path1)
    print(path2)
    if re.search(path2,path1):
        return True
    else:
        return False

def length(list):
    return len(list)

# "*" means any deepness of scope is allowed 
def selection_function(regex :str, df: pd.DataFrame ,scope_column: str, scope_sep = "/"):
    scope = df[scope_column]
    regex = re.sub("\?"+ scope_sep,'(\\\w+'+scope_sep+')?',regex)
    regex = re.sub("\*" + scope_sep,'(\\\w+'+scope_sep+')*',regex)

    paths = scope.apply(compare_paths, path2=(regex))
    paths = paths[paths] #Only where values True i.e. paths match
    return df.loc[paths.index]