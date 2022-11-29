import pm4py
from copy import copy, deepcopy
from pm4py.objects.ocel.obj import OCEL

class OCEL_ext(OCEL):
    def __init__(self,ocel:OCEL):
         super().__init__(ocel.events, ocel.objects, ocel.relations, ocel.globals, ocel.parameters)

    def get_dict_summary(self) -> dict:
        """
        Gets a dictionary summary of the object-centric event log
        """
        summary = {
            "number of events": len(self.events),
            "number of objects": len(self.objects),
            "number of activities": self.events[self.event_activity].nunique(),
            "number of object types": self.objects[self.object_type_column].nunique(),
            "events-objects relationships": len(self.relations),
            "Activities occurrences": str(self.events[self.event_activity].value_counts().to_dict()),
            "Object types occurrences (number of objects)": str(
                self.objects[self.object_type_column].value_counts().to_dict())
        }

        return summary

    def __str__(self):
        return str(super().get_summary())

    def __repr__(self):
        return str(super().get_summary())

    def __copy__(self):
        return OCEL_ext(self.events, self.objects, self.relations, copy(self.globals), copy(self.parameters))

    def __deepcopy__(self, memo):
        return OCEL_ext(self.events.copy(), self.objects.copy(), self.relations.copy(), deepcopy(self.globals),
                    deepcopy(self.parameters))

