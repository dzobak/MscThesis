import { Component, ViewChild, OnInit } from '@angular/core';
import { MatModules } from '../material.module';
import { MatAccordion } from '@angular/material/expansion';
import { ApplyingService } from '../applying/applying.service'
import { Subscription } from 'rxjs';


export interface PeriodicElement {
  name: string;
  position: number;
  events: number;
  symbol: string;
  panelOpenState: boolean;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: 'event_log1', events: 30000, symbol: 'H', panelOpenState: false },
  { position: 2, name: 'event_log2', events: 40026, symbol: 'He', panelOpenState: false },
  { position: 3, name: 'event_log3', events: 6941, symbol: 'Li', panelOpenState: false },
  { position: 4, name: 'event_log4', events: 90122, symbol: 'Be', panelOpenState: false },
  { position: 5, name: 'event_log5', events: 10811, symbol: 'B', panelOpenState: false },

];

export interface LogDetails {
  name: string;
  panelOpenState: boolean;
}


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
  log_details: LogDetails[] = [];

  NamesSubs!: Subscription;
  eventlognames: string[] = [];

  constructor(private aplService: ApplyingService) { }

  ngOnInit(): void {
    this.NamesSubs = this.aplService
      .getEventLogNames()
      .subscribe(res => {
        this.eventlognames = res;
        console.log(this.eventlognames)
        for (let i in this.eventlognames) {
          this.log_details.push(
            {
              "name": this.eventlognames[i],
              "panelOpenState": false
            }
          )
        }
        console.log(this.log_details)
      }
      );
  }

  visibility(log: any) {
    log.visibility = !log.visibility;
  }


}
