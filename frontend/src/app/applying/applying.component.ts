import { Component, OnInit, OnDestroy, ComponentFactoryResolver } from '@angular/core';
import { TestBed } from '@angular/core/testing';
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

interface EventLogHeading{
  value: string,
  scopes: String[]
}

@Component({
  selector: 'app-applying',
  templateUrl: './applying.component.html',
  styleUrls: ['./applying.component.css']
})
export class ApplyingComponent implements OnInit, OnDestroy {

  // eventz: any = [{"ocel:eid": "2.0",
  //                 "ocel:timestamp": 1634617587000,
  //                 "ocel:activity": "add item to cart",
  //                 "scope": "business/new order/add item to cart",
  //                 "scope2": null}]

  applyingData: EventLogHeading[] = [];
  eventLog: [] = [];
  scopeLevels!: number[];
  
  ApplyingSubs!: Subscription;
  EventLogSubs!: Subscription;
  regex: string = "";

  tabgroup_disabled: Boolean = true;

  dataSource = ELEMENT_DATA; 
  selectedLog!: string;
  selectedScope!: string;
  selectedScopeLevel!: number;


  constructor(private emplSer : ApplyingService) { }

  columnsToDisplay: string[] = []

  ngOnInit() {
    this.ApplyingSubs = this.emplSer
    .getApplyingPage()
    .subscribe(res => {
      this.applyingData = res;
    }
  );
  }
  ngOnDestroy() {
    this.ApplyingSubs.unsubscribe();
  }

  loadNewEventLog(value:any){
    this.EventLogSubs = this.emplSer
    .getEventLog(value)
    .subscribe(res => {
      this.eventLog = JSON.parse(res);
      this.columnsToDisplay = ["ocel:timestamp", "ocel:activity", "scope"];
    }
  );
   this.tabgroup_disabled = false;
  }

  getScopeLevels(value:any){
    this.EventLogSubs = this.emplSer
    .getScopeLevels(this.selectedLog, value)
    .subscribe(res => {
      this.scopeLevels = JSON.parse(res).levels;
    }
  );
  }

  sendRegex(value:string){
    this.EventLogSubs = this.emplSer
    .getSelection(value, this.selectedLog, this.selectedScope)
    .subscribe(res => {
      this.eventLog = JSON.parse(res);
      this.columnsToDisplay = ["ocel:timestamp", "ocel:activity", "scope"];
    }
  );
  }

  getAggregation(){
    this.ApplyingSubs = this.emplSer
    .getAggregation(this.selectedLog,this.selectedScope, this.selectedScopeLevel)
    .subscribe(res => {
      this.eventLog = JSON.parse(res);
    }
  );
  }


}
