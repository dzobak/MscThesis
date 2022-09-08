import { Component, OnInit } from '@angular/core';
import { MatModules } from '../material.module';

export interface PeriodicElement {
  name: string;
  position: number;
  events: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'Hydrogen', events: 30000, symbol: 'H'},
  {position: 2, name: 'Helium', events: 40026, symbol: 'He'},
  {position: 3, name: 'Lithium', events: 6941, symbol: 'Li'},
  {position: 4, name: 'Beryllium', events: 90122, symbol: 'Be'},
  {position: 5, name: 'Boron', events: 10811, symbol: 'B'},

];

@Component({
  selector: 'app-log-details',
  templateUrl: './log-details.component.html',
  styleUrls: ['./log-details.component.css']
})
export class LogDetailsComponent implements OnInit {

  displayedColumns: string[] = ['name', 'events'];
  dataSource = ELEMENT_DATA;  
  constructor() { }

  ngOnInit(): void {
  }

}
