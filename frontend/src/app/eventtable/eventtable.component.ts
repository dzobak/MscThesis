import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { Dialog, DIALOG_DATA } from '@angular/cdk/dialog';

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog', 'columnSelect', 'selectedMethods']
})
export class EventtableComponent {
  @Output()
  notify: EventEmitter<object> = new EventEmitter<object>();

  columnsToDisplay!: string[];
  columnSelect!: string[][];
  displayedColumns: string[] = ["ocel:eid", "ocel:timestamp"]
  eventLog!: [];
  selectedMethods!: any
  isOpen = false;

  constructor(public dialog: Dialog) { }
  // ngOnInit(): void {
  //   this.selectedMethods = {};
  //   for (let i = 0; i < this.columnSelect.length; i++) {
  //     this.selectedMethods[String(i)] = this.columnSelect[i][0];
  //   }
  //   console.log(this.selectedMethods)
  // }

  methodChanged(event:any){
    this.notify.emit(this.selectedMethods)
  }
  showRowInformation(row: any) {
    console.log(row)
    // this.dialog.open(CdkDialogDataExampleDialog, {
    //   minWidth: '300px',
    //   data: {
    //     animal: 'panda',
    //   },
    // });
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

