import pm4py
import pandas as pd
from pm4py.objects.ocel.obj import OCEL, Parameters

class Aggregation():

    def get_event_scope(self, scope, level, scope_sep="/"):
        return scope.rsplit(scope_sep)[level]

    def get_act_name(self, eid, id_act_map):
        return id_act_map[eid]

    def switch_event_scope(self, log: OCEL, level:int, scope:str):
        events = log.events
        log.events.loc[:,"ocel:activity"] = events[scope].apply(self.get_event_scope,level=level)
        id_act_map = pd.Series(events['ocel:activity'].values,index=events['ocel:eid']).to_dict()
        log.relations.loc[:,"ocel:activity"] = log.relations['ocel:eid'].apply(self.get_act_name, id_act_map=id_act_map)
        return log   

    def combine_events(self, events : pd.DataFrame, eid):
        grouped_ev = events.groupby('ocel:activity').agg({'ocel:timestamp': ['min', 'max']})
        grouped_ev = grouped_ev.rename(columns={'min': 'timestamp:start', 'max': 'timestamp:end'}) 
        grouped_ev.columns = grouped_ev.columns.get_level_values(1)
        grouped_ev["ocel:eid"] = eid
        return grouped_ev 

    def split_by_values_inbetween(self, events, k=1):
        events.withcopy = False
        events["ocel:eid"]  =  events["ocel:eid"].astype(float)
        events = events.sort_values(by="ocel:eid")
        events = events.reset_index(drop=True)
        
        curr_id = events["ocel:eid"][0] - 1
        act_mapping = {}
        act_inst = 1
        act_string = events["ocel:activity"][0] + '_' + str(act_inst)
        act_mapping[act_string] = []
        
        for i in range(len(events)):
            curr_id += 1
            if curr_id != events["ocel:eid"][i]:
                if events["ocel:eid"][i] - curr_id >= k:
                    act_inst += 1
                    act_string = events["ocel:activity"][i] + '_' + str(act_inst)
                    act_mapping[act_string] = []
                curr_id = events["ocel:eid"][i]
            
            act_mapping[act_string].append(str(curr_id))
                
        return act_mapping

    def get_event_activity_mapping(self, log: OCEL):
        acts = log.events['ocel:activity'].unique()
        mapping = {}
        for act in acts:
            events = log.events[log.events['ocel:activity']== act]
            mapping = mapping | self.split_by_values_inbetween(events, k=1)
            
        return mapping

    def get_aggregated_events(self, log, mapping):
        new_events = pd.DataFrame()
        i = 0
        same_act = pd.DataFrame()
        eid = 0.0

        rel_mapping = {}

        for act, ids in mapping.items():
            eid += 1
            same_act = log.events[
                log.events["ocel:eid"].isin(ids)
            ]
            new_event = self.combine_events(same_act, eid)
            new_events = pd.concat([new_events,new_event])
            same_act = pd.DataFrame()
            
            for ID in ids:
                rel_mapping[ID] = eid
            
        new_events.reset_index(inplace=True)
        return new_events, rel_mapping

    def assign_aggregated_relations(self, eid, rel_mapping):
        return rel_mapping[eid]

    def combine_relations(self, log):
        grouped_rel = log.relations.groupby(['ocel:eid','ocel:oid', 'ocel:activity', 'ocel:type']).agg({'ocel:timestamp': ['min', 'max']})
        grouped_rel = grouped_rel.rename(columns={'min': 'timestamp:start', 'max': 'timestamp:end'}) 
        grouped_rel.columns = grouped_rel.columns.get_level_values(1)
        grouped_rel.reset_index(inplace=True)
        return grouped_rel

    def aggregate_log(self, log, level, scope):
        log = self.switch_event_scope(log, level= level, scope=scope)
        mapping = self.get_event_activity_mapping(log)
        events, rel_mapping = self.get_aggregated_events(log, mapping)
        log.events = events
        log.relations["ocel:eid"] = log.relations["ocel:eid"].apply(self.assign_aggregated_relations,rel_mapping=rel_mapping)
        log.relations = self.combine_relations(log)
        log.parameters["EVENT_TIMESTAMP"] = "timestamp:end"
        log.event_timestamp = "timestamp:end"
        return log