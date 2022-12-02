import { ThisReceiver } from '@angular/compiler';
import { Component, OnInit, OnDestroy } from '@angular/core';
// import { TestBed } from '@angular/core/testing';
import { isEmpty, Subscription } from 'rxjs';
import { LogDetailsService } from '../log-details/log-details.service';
import { ApplyingService, EventLogHeading } from './applying.service'

@Component({
  selector: 'app-applying',
  templateUrl: './applying.component.html',
  styleUrls: ['./applying.component.css']
})
export class ApplyingComponent implements OnInit, OnDestroy {

  applyingData: EventLogHeading[] = [];
  eventlognames: string[] = [];
  table: [] = [];
  eventLog: [] = [];
  eventColumns!: string[];
  objects: [] = [];
  objectColumns!: string[];
  eventScopeLevels!: number[];
  log_details!: object;

  ApplyingSubs!: Subscription;
  NamesSubs!: Subscription;
  EventLogSubs!: Subscription;
  ObjectsSubs!: Subscription;
  ColumnSubs!: Subscription;
  DetailsSubs!: Subscription;
  regex: string = "";
  relabel: string = "";

  tabgroup_disabled: Boolean = true;

  selectedLog!: string;
  selectedScope!: string;
  selectedScopeLevel = 0;

  selectedOEoption = "event";

  applyingDataNeeded = false;
  currentEventLogNametmp!: string

  constructor(private aplService: ApplyingService, private logDetService: LogDetailsService) { }

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
          this.applyingDataNeeded = false;
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
          console.log(this.table)
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
    }else{
      this.applyingDataNeeded = true;
      this.currentEventLogNametmp = value
    }
  }

  getLogData(logname: string) {
    this.ApplyingSubs = this.aplService
      .getLogData(logname)
      .subscribe(res => {
        this.applyingData.push(JSON.parse(res))
        this.selectedLog = logname
        this.loadNewEventLog(logname)
      }
      )
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

  getColumnFunctionMapping() {
    let col_func_mapping = new Map<string, string>();
    for (let i = 0; i < this.columnsToDisplay.length; i++) {
      col_func_mapping.set(this.columnsToDisplay[i], this.selectedMethods[String(i)]);
    }
    return col_func_mapping
  }

  getColumnAggregationFunctions() {
    
    this.ColumnSubs = this.aplService
      .getColumnFuctions(this.selectedLog,  this.selectedOEoption == "event", this.selectedOEoption == "object")
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
    var newfilename = this.getTempFileName()
    this.EventLogSubs = this.aplService
      .getSelection(value, this.selectedLog, newfilename, this.selectedScope,
        this.selectedOEoption == "event", this.selectedOEoption == "object", "items")
      .subscribe(res => {
        this.table = JSON.parse(res);
        this.getLogData(newfilename)
      }
      );
  }

  getAggregation() {
    // missing select object type
    var newfilename = this.getTempFileName()
    this.ApplyingSubs = this.aplService
      .getAggregation(this.selectedLog, newfilename ,this.selectedScope, this.selectedScopeLevel,
        this.selectedOEoption == "event", this.selectedOEoption == "object", this.getColumnFunctionMapping(), "items")
      .subscribe(res => {
        this.table = JSON.parse(res);

        this.getLogData(newfilename)
      }
      );
  }

  getRelabelling() {
    var newfilename = this.getTempFileName()
    this.ApplyingSubs = this.aplService
      .getRelabelling(this.selectedLog,newfilename, this.relabel,
        this.selectedOEoption == "event", this.selectedOEoption == "object", "items")
      .subscribe(res => {
        this.table = JSON.parse(res);
        this.getLogData(newfilename)
        
      }
      );
  }

  getEventDetails() {
    this.DetailsSubs = this.logDetService
      .getDetails(this.selectedLog)
      .subscribe(res => {
        this.log_details = JSON.parse(res)
        console.log(this.log_details)
      }
      );
  }

  getTempFileName() {
    if (this.selectedLog.search("@tmp") >= 0) {
      return this.selectedLog
    } else {
      return this.selectedLog + "@tmp"
    }
  }
}

