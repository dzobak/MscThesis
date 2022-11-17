
def get_scope_tuple(scope):
    return tuple(scope.rsplit('/'))


def concat_dicts(series) -> dict:
    new_dict = {}
    for dict in series:
        new_dict.update(dict)
    return new_dict
