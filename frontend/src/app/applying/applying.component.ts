// import { ThisReceiver } from '@angular/compiler';
import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
// import { TestBed } from '@angular/core/testing';
import { isEmpty, Subscription } from 'rxjs';
import { LogDetailsService } from '../log-details/log-details.service';
import { ApplyingService, EventLogHeading } from './applying.service'
import { AggregationMapping } from '../eventtable/eventtable.component';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { numeric_input } from '../aggregation-input/aggregation-input.component';


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
  groupingKey: string = "";

  tabgroup_disabled: Boolean = true;

  selectedLog!: string;
  selectedScope!: string;
  selectedScopeLevel = 0;
  selectedOEoption = "event";

  applyingDataNeeded = false;
  currentEventLogNametmp!: string
  aggregationMapping!: AggregationMapping;

  constructor(private aplService: ApplyingService,
    private logDetService: LogDetailsService,
    public dialog: MatDialog) { }

  columnsToDisplay: string[] = []
  columnSelect: string[][] = [];
  columnSelectCandidates!: any;
  selectedMethods!: any;

  rules!: { [Key: string]: numeric_input }

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
    // console.log(this.applyingData)
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

  getLogData(logname: string) {

    this.NamesSubs = this.aplService
      .getEventLogNames()
      .subscribe(res => {
        this.eventlognames = res;
      }
      );
    this.ApplyingSubs = this.aplService
      .getLogData(logname)
      .subscribe(res => {
        for (let i = 0; i < this.applyingData.length; i++) {
          if (this.applyingData[i].value.search("@tmp") >= 0) {
            // console.log(this.applyingData[i])
            this.applyingData.splice(i, 1)
          }
        }
        this.applyingData.push(JSON.parse(res))
        this.selectedLog = logname
        this.loadNewEventLog(logname)
      }
      )
  }

  switchEventObject(event: any): void {
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
    var col_func_mapping: { [key: string]: string } = {};
    for (let i = 0; i < this.columnsToDisplay.length; i++) {
      col_func_mapping[this.columnsToDisplay[i]] = this.selectedMethods[String(i)];
    }
    // console.log( typeof col_func_mapping)
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
        this.selectedMethods = {};
        for (let i = 0; i < this.columnSelect.length; i++) {
          this.selectedMethods[String(i)] = this.columnSelect[i][0];
        }
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
    // TODO select object type
    var newfilename = this.getTempFileName()
    this.ApplyingSubs = this.aplService
      .getAggregation(this.selectedLog, newfilename, this.selectedScope, this.selectedScopeLevel, this.groupingKey,
        this.selectedOEoption == "event", this.selectedOEoption == "object", this.getColumnFunctionMapping(), "items")
      .subscribe(res => {
        this.aggregationMapping = JSON.parse(res);
        this.aggregationMapping.isEventTransformation = this.selectedOEoption == "event";
        this.aggregationMapping.isObjectTransformation = this.selectedOEoption == "object";
        this.getLogData(newfilename)
      }
      );
  }

  updateAggInput(input: numeric_input, ruleId: string) {
    this.rules[ruleId] = input;
    console.log(this.rules)
  }

  addRule() {
    if (this.rules) {
      const keys = Object.keys(this.rules).map(i => Number(i));
      const new_key = Math.max.apply(null,keys);
      console.log(new_key)
      this.rules[new_key + 1] = {
        attribute: '',
        bool: true,
        operator: '',
        compared: '',
        value: ''
      }
    } else {
      this.rules = {
        0:
        {
          attribute: '',
          bool: true,
          operator: '',
          compared: '',
          value: ''
        }
      };

    }
  }

  deleteRule(id:string){
    console.log(id)
    delete this.rules[id]
  }

  getRelabelling() {
    var newfilename = this.getTempFileName()
    this.ApplyingSubs = this.aplService
      .getRelabelling(this.selectedLog, newfilename, this.relabel,
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

  saveLog() {
    var new_name = 'new_name'
    const dialogRef = this.dialog.open(SaveDialog, {
      data: { new_name: this.selectedLog.replace('@', '') },
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      new_name = result;
      this.ApplyingSubs = this.aplService
        .saveLog(this.selectedLog, new_name)
        .subscribe(res => {
          this.getLogData(new_name)
        }
        );
    });
  }
}

export interface DialogData {
  new_name: string;
}

@Component({
  selector: 'save-dialog',
  templateUrl: './saveDialog.html',
})
export class SaveDialog {
  constructor(
    public dialogRef: MatDialogRef<SaveDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
  ) { }

  onNoClick(): void {
    this.dialogRef.close();
  }
}

