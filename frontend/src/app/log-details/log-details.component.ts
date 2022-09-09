import { Component, ViewChild ,OnInit } from '@angular/core';
import { MatModules } from '../material.module';
import {MatAccordion} from '@angular/material/expansion';


export interface PeriodicElement {
  name: string;
  position: number;
  events: number;
  symbol: string;
  panelOpenState: boolean;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'event_log1', events: 30000, symbol: 'H', panelOpenState: false},
  {position: 2, name: 'event_log2', events: 40026, symbol: 'He', panelOpenState: false},
  {position: 3, name: 'event_log3', events: 6941, symbol: 'Li', panelOpenState: false},
  {position: 4, name: 'event_log4', events: 90122, symbol: 'Be', panelOpenState: false},
  {position: 5, name: 'event_log5', events: 10811, symbol: 'B', panelOpenState: false},

];

@Component({
  selector: 'app-log-details',
  templateUrl: './log-details.component.html',
  styleUrls: ['./log-details.component.css']
})
export class LogDetailsComponent implements OnInit {
  @ViewChild(MatAccordion) accordion!: MatAccordion;

  // panelOpenState = false;
  displayedColumns: string[] = ['name', 'events'];
  dataSource = ELEMENT_DATA; 
  saveVal = true;
  
  constructor() { }

  ngOnInit(): void {
  }

  visibility(log:any){
    log.visibility = !log.visibility;
  }


}
