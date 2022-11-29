import pm4py


class OCEL(pm4py.objects.ocel.obj.OCEL):

    def get_summary(self) -> dict:
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
