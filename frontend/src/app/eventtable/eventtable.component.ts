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
  columnSelect!: object ;
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

  dictKeysToList(d: object){
    return Object.keys(d)
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

