import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { Dialog, DIALOG_DATA, DialogRef } from '@angular/cdk/dialog';
import { PatternValidator } from '@angular/forms';

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog', 'columnSelect', 'selectedMethods', 'aggregationMapping']
})
export class EventtableComponent {
  @Output()
  notify: EventEmitter<object> = new EventEmitter<object>();

  columnsToDisplay!: string[];
  columnSelect!: string[][];
  displayedColumns: string[] = ["ocel:eid", "ocel:timestamp"]
  eventLog!: [];
  selectedMethods!: any;
  aggregationMapping!: any;
  isOpen = false;
  // animal: string | undefined;

  constructor(public dialog: Dialog) { }

  methodChanged(event: any) {
    this.notify.emit(this.selectedMethods)
  }
  showRowInformation(row: any) {
    if (this.aggregationMapping) {
      const dialogRef = this.dialog.open<string>(CdkDialogOverviewExampleDialog, {
        width: '250px',
        data: { name: row["ocel:eid"], aggregationMapping: this.aggregationMapping[row["ocel:eid"]] },
      });

      dialogRef.closed.subscribe(result => {
        console.log('The dialog was closed');
        // this.animal = result;
      });
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
  aggregationMapping: object;
  name: string;
}

@Component({
  selector: 'cdk-dialog-data-example-dialog',
  templateUrl: './cdk-dialog-data-example-dialog.html',
  styleUrls: ['./eventtable.component.css'],
})
export class CdkDialogOverviewExampleDialog {
  constructor(public dialogRef: DialogRef<string>, @Inject(DIALOG_DATA) public data: DialogData) { }
}

