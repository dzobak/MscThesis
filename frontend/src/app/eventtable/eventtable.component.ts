import { Component } from '@angular/core';

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog']
})
export class EventtableComponent {
  columnsToDisplay!: string[];
  displayedColumns: string[] = ["ocel:eid", "ocel:timestamp"]
  eventLog!: [];

  constructor() { }

}
