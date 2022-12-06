import pm4py
from copy import copy, deepcopy
from pm4py.objects.ocel.obj import OCEL
from enum import Enum
from pm4py.objects.ocel import constants
from typing import List


class Parameters(Enum):
    EVENT_SCOPES = 'event_scopes'
    OBJECT_SCOPES = 'object_scopes'


class OCEL_ext(OCEL):
    def __init__(self, ocel: OCEL, parameters=None):
        if parameters is None:
            parameters = ocel.parameters
        else:
            L = [parameters, ocel.parameters]
            dups = set(parameters.keys() & ocel.parameters.keys())
            parameters = {k: L[0][k] if k in dups else
                          params[k] for params in L for k in params}
        print(parameters)
        super().__init__(ocel.events, ocel.objects,
                         ocel.relations, ocel.globals, parameters)
        self.event_scope_columns = parameters[Parameters.EVENT_SCOPES] if Parameters.EVENT_SCOPES in parameters\
            else self.get_default_event_scope_columns()
        self.object_scope_columns = parameters[Parameters.OBJECT_SCOPES] if Parameters.OBJECT_SCOPES in parameters\
            else self.get_default_object_scope_columns()

    def get_dict_summary(self) -> dict:
        '''
        Gets a dictionary summary of the object-centric event log
        '''
        summary = {
            'number of events': len(self.events),
            'number of objects': len(self.objects),
            'number of activities': self.events[self.event_activity].nunique(),
            'number of object types': self.objects[self.object_type_column].nunique(),
            'events-objects relationships': len(self.relations),
            'Activities occurrences': str(self.events[self.event_activity].value_counts().to_dict()),
            'Object types occurrences (number of objects)': str(
                self.objects[self.object_type_column].value_counts().to_dict())
        }

        return summary

    def get_default_object_scope_columns(self):
        return self.get_default_scope_columns(self.objects.columns)

    def get_default_event_scope_columns(self):
        return self.get_default_scope_columns(self.events.columns)

    def get_default_scope_columns(self, columns: List[str]) -> List[str]:
        return [scope for scope in columns if 'scope' in scope]

    def __str__(self):
        return str(super().get_summary())

    def __repr__(self):
        return str(super().get_summary())

    def __copy__(self):
        return OCEL_ext(self.events, self.objects, self.relations, copy(self.globals), copy(self.parameters))

    def __deepcopy__(self, memo):
        return OCEL_ext(self.events.copy(), self.objects.copy(), self.relations.copy(), deepcopy(self.globals),
                        deepcopy(self.parameters))
