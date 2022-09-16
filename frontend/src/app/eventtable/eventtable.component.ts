import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-eventtable',
  templateUrl: './eventtable.component.html',
  styleUrls: ['./eventtable.component.css'],
  inputs: ['columnsToDisplay', 'eventLog']
})
export class EventtableComponent implements OnInit {
  columnsToDisplay!: string[];
  eventLog!: [];

  constructor() { }

  ngOnInit():void {
  }

}
