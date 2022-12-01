import { Component, Inject } from '@angular/core';
import { Dialog, DIALOG_DATA } from '@angular/cdk/dialog';

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog', 'columnSelect']
})
export class EventtableComponent {
  columnsToDisplay!: string[];
  columnSelect!: string[][];
  displayedColumns: string[] = ["ocel:eid", "ocel:timestamp"]
  eventLog!: [];
  isOpen = false;

  constructor(public dialog: Dialog) { }

  showRowInformation(row: any) {
    console.log(row)
    this.dialog.open(CdkDialogDataExampleDialog, {
      minWidth: '300px',
      data: {
        animal: 'panda',
      },
    });
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
  animal: 'panda' | 'unicorn' | 'lion';
}

@Component({
  selector: 'cdk-dialog-data-example-dialog',
  templateUrl: './cdk-dialog-data-example-dialog.html',
  styleUrls: ['./eventtable.component.css'],
})
export class CdkDialogDataExampleDialog {
  constructor(@Inject(DIALOG_DATA) public data: DialogData) { }
}

