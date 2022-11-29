import pandas as pd
import re
class Selection():

    def compare_paths(self, path1, path2):
        if re.search(path2,path1):
            return True
        else:
            return False

    # "*" means any deepness of scope is allowed 
    def selection_function(self,regex :str, df: pd.DataFrame ,scope_column: str, scope_sep = "/"):
        scope = df[scope_column]
        regex = re.sub("\?"+ scope_sep,'((\\\w+|\\\s)+'+scope_sep+')?',regex)
        regex = re.sub("\*" + scope_sep,'(.*'+scope_sep+')*',regex)

        paths = scope.apply(self.compare_paths, path2=(regex))
        paths = paths[paths] #Only where values True i.e. paths match
        return df.loc[paths.index]