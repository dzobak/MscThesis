import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { Dialog, DIALOG_DATA, DialogRef } from '@angular/cdk/dialog';
import { ApplyingService } from '../applying/applying.service';
import { Subscription } from 'rxjs';

export interface AggregationMapping {
  eventlogname: string,
  mapping: any,
  isEventTransformation: boolean,
  isObjectTransformation: boolean,
}

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog', 'columnSelect', 'selectedMethods', 'aggregationMapping']
})
export class EventtableComponent {
  @Output()
  notify: EventEmitter<object> = new EventEmitter<object>();
  OldEventsSubs!: Subscription;
  columnsToDisplay!: string[];
  columnSelect!: string[][];
  displayedColumns: string[] = ["ocel:eid", "ocel:timestamp"]
  eventLog!: [];
  selectedMethods!: any;
  aggregationMapping!: AggregationMapping;
  isOpen = false;
  oldRows: any[] = [];
  // animal: string | undefined;

  constructor(public dialog: Dialog, private aplService: ApplyingService) { }

  methodChanged(event: any) {
    this.notify.emit(this.selectedMethods)
  }
  showRowInformation(row: any) {
    if (this.aggregationMapping) {

      this.OldEventsSubs = this.aplService
        .getOldRows(this.aggregationMapping.eventlogname, this.aggregationMapping['mapping'][row["ocel:eid"]],
          this.aggregationMapping.isEventTransformation, this.aggregationMapping.isObjectTransformation)
        .subscribe(res => {
          console.log(res)
          this.oldRows = JSON.parse(res);
          const dialogRef = this.dialog.open<string>(CdkDialogOverviewExampleDialog, {
            minWidth: '250px',
            data: { name: row["ocel:eid"], oldRows: this.oldRows, columnsToDisplay: Object.keys(this.oldRows[0])},
          });
          dialogRef.closed.subscribe(result => {
            console.log('The dialog was closed');
            // this.animal = result;
          });
        }
        );
    }
  }



  StringToInt(i: string) {
    return parseInt(i)
  }

  getStringArray() {
    var n = this.columnsToDisplay.length;
    var array = [...Array(n).keys()].map(String);
    return array
  }

}
export interface DialogData {
  oldRows: any[];
  name: string;
  columnsToDisplay: string[];
}

@Component({
  selector: 'cdk-dialog-data-example-dialog',
  templateUrl: './cdk-dialog-data-example-dialog.html',
  styleUrls: ['./eventtable.component.css'],
})
export class CdkDialogOverviewExampleDialog {
  constructor(public dialogRef: DialogRef<string>, @Inject(DIALOG_DATA) public data: DialogData) { }
}

