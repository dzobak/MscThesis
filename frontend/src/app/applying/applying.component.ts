import { ThisReceiver } from '@angular/compiler';
import { Component, OnInit, OnDestroy } from '@angular/core';
// import { TestBed } from '@angular/core/testing';
import { isEmpty, Subscription } from 'rxjs';
import { ApplyingService, EventLogHeading } from './applying.service'

export interface PeriodicElement {
  name: string
  position: number;
  events: number;
  symbol: string;
  panelOpenState: boolean;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: 'event_log1', events: 30000, symbol: 'H', panelOpenState: false },
  { position: 2, name: 'event_log2', events: 40026, symbol: 'He', panelOpenState: false },
  { position: 3, name: 'event_log3', events: 6941, symbol: 'Li', panelOpenState: false },
  { position: 4, name: 'event_log4', events: 90122, symbol: 'Be', panelOpenState: false },
  { position: 5, name: 'event_log5', events: 10811, symbol: 'B', panelOpenState: false },

];


@Component({
  selector: 'app-applying',
  templateUrl: './applying.component.html',
  styleUrls: ['./applying.component.css']
})
export class ApplyingComponent implements OnInit, OnDestroy {

  // eventz: any = [{"ocel:eid": "2.0",
  //                 "ocel:timestamp": 1634617587000,
  //                 "ocel:activity": "add item to cart",
  //                 "scope": "business/new order/add item to cart",
  //                 "scope2": null}]

  applyingData: EventLogHeading[] = [];
  eventlognames: string[] = [];
  table: [] = [];
  eventLog: [] = [];
  eventColumns!: string[];
  objects: [] = [];
  objectColumns!: string[];
  eventScopeLevels!: number[];

  ApplyingSubs!: Subscription;
  NamesSubs!: Subscription;
  EventLogSubs!: Subscription;
  ObjectsSubs!: Subscription;
  ColumnSubs!: Subscription;
  regex: string = "";

  tabgroup_disabled: Boolean = true;

  dataSource = ELEMENT_DATA;
  selectedLog!: string;
  selectedScope!: string;
  selectedScopeLevel = 0;

  selectedOEoption = "event";

  applyingDataNeeded = false;
  currentEventLogNametmp!: string

  constructor(private aplService: ApplyingService) { }

  columnsToDisplay: string[] = []
  columnSelect: string[][] = [];
  columnSelectCandidates!: any;
  selectedMethods!: any;

  ngOnInit() {
    this.NamesSubs = this.aplService
      .getEventLogNames()
      .subscribe(res => {
        this.eventlognames = res;
      }
      );
    this.ApplyingSubs = this.aplService
      .getApplyingPage()
      .subscribe(res => {
        this.applyingData = res;
        if (this.applyingDataNeeded) {
          this.loadNewEventLog(this.currentEventLogNametmp)
        }
      }
      );
  }
  ngOnDestroy() {
    this.ApplyingSubs.unsubscribe();
  }

  loadNewEventLog(value: any) {
    if (this.applyingData.length) {
      for (let log_head of this.applyingData) if (log_head.value == value) {
        this.eventColumns = log_head["e_columns"]
        this.objectColumns = log_head["o_columns"]
      };
      this.table = [];
      this.EventLogSubs = this.aplService
        .getEvents(value)
        .subscribe(res => {
          this.eventLog = JSON.parse(res);
          if (this.selectedOEoption == "event") {
            this.table = this.eventLog;
            this.columnsToDisplay = this.eventColumns;
          }
        }
        );
      this.ObjectsSubs = this.aplService
        .getObjects(value)
        .subscribe(res => {
          this.objects = JSON.parse(res);
          if (this.selectedOEoption == "object") {
            this.table = this.objects;
            this.columnsToDisplay = this.objectColumns;
          }
        }
        );
      this.getColumnAggregationFunctions()

      this.tabgroup_disabled = false;
    } else {
      this.applyingDataNeeded = true;
      this.currentEventLogNametmp = value
    }
  }

  switchEventObject(event: any) {
    if (this.selectedOEoption == "event") {
      this.table = this.eventLog;
      this.columnsToDisplay = this.eventColumns;
    } else if (this.selectedOEoption == "object") {
      this.table = this.objects;
      this.columnsToDisplay = this.objectColumns;
    }
    this.getColumnAggregationFunctions()
    // this.getScopeLevels()
  }

  selectedMethodsChanged(event: any) {
    console.log(event)
  }

  getScopeLevels(value: any) {
    this.EventLogSubs = this.aplService
      .getScopeLevels(this.selectedLog, value, this.selectedOEoption == "event", this.selectedOEoption == "object")
      .subscribe(res => {
        this.eventScopeLevels = JSON.parse(res).levels;
      }
      );
  }

  getColumnFunctionMapping(){
    let col_func_mapping = new Map<string, string>();
    for (let i = 0; i < this.columnsToDisplay.length; i++) {
        col_func_mapping.set(this.columnsToDisplay[i], this.selectedMethods[String(i)]); 
    }
    return col_func_mapping
  }

  getColumnAggregationFunctions() {
    this.ColumnSubs = this.aplService
      .getColumnFuctions(this.selectedLog, this.selectedOEoption == "event", this.selectedOEoption == "object")
      .subscribe(res => {
        this.columnSelectCandidates = JSON.parse(res);
        this.columnSelect = []
        for (let column of this.columnsToDisplay) {
          this.columnSelect.push(this.columnSelectCandidates[column]);
        }
        console.log(this.columnSelect)
        this.selectedMethods = {};
        for (let i = 0; i < this.columnSelect.length; i++) {
          this.selectedMethods[String(i)] = this.columnSelect[i][0];
        }
        console.log(this.selectedMethods)
      }
      );
  }

  sendRegex(value: string) {
    this.EventLogSubs = this.aplService
      .getSelection(value, this.selectedLog, this.selectedScope,
        this.selectedOEoption == "event", this.selectedOEoption == "object", "items")
      .subscribe(res => {
        this.table = JSON.parse(res);
      }
      );
  }

  getAggregation() {
    // missing select object type
    this.ApplyingSubs = this.aplService
      .getAggregation(this.selectedLog, this.selectedScope, this.selectedScopeLevel,
        this.selectedOEoption == "event", this.selectedOEoption == "object", this.getColumnFunctionMapping() ,"items")
      .subscribe(res => {
        this.table = JSON.parse(res);
      }
      );
  }

  getRelabelling() {
    this.ApplyingSubs = this.aplService
      .getRelabelling(this.selectedLog, this.selectedScope, [this.selectedScopeLevel],
        this.selectedOEoption == "event", this.selectedOEoption == "object", "items")
      .subscribe(res => {
        this.table = JSON.parse(res);
      }
      );
  }
}

