import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import {ApplyingService} from './applying.service'

export interface PeriodicElement {
  name: string
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
  selector: 'app-applying',
  templateUrl: './applying.component.html',
  styleUrls: ['./applying.component.css']
})
export class ApplyingComponent implements OnInit, OnDestroy {
  applyingData: JSON|any;
  ApplyingSubs!: Subscription;
  

  dataSource = ELEMENT_DATA; 
  selectedValue!: string;
  constructor(private emplSer : ApplyingService) { }

  ngOnInit() {
    console.log("hello")
    this.ApplyingSubs = this.emplSer
    .getApplyingPage()
    .subscribe(res => {
      this.applyingData = res;
    }
  );
  console.log(this.applyingData)
  }
  ngOnDestroy() {
    this.ApplyingSubs.unsubscribe();
  }


}
