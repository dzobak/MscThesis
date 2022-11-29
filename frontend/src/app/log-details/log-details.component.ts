import { Component, ViewChild, OnInit } from '@angular/core';
import { MatAccordion } from '@angular/material/expansion';
import { ApplyingService } from '../applying/applying.service'
import { Subscription } from 'rxjs';
import { LogDetailsService } from './log-details.service';


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
  details: object;
}


@Component({
  selector: 'app-log-details',
  templateUrl: './log-details.component.html',
  styleUrls: ['./log-details.component.css']
})
export class LogDetailsComponent implements OnInit {
  @ViewChild(MatAccordion) accordion!: MatAccordion;
  fileName = '';
  // panelOpenState = false;
  displayedColumns: string[] = ['name', 'events'];
  dataSource = ELEMENT_DATA;
  saveVal = true;
  log_details: LogDetails[] = [];

  NamesSubs!: Subscription;
  DetailSubs!: Subscription;
  eventlognames: string[] = [];
  newEventlogs: string[] = []

  constructor(private aplService: ApplyingService, private logDetService: LogDetailsService) { }

  ngOnInit(): void {
    this.NamesSubs = this.aplService
      .getEventLogNames()
      .subscribe(res => {
        this.eventlognames = res;
        for (let i in this.eventlognames) {
          if (!this.log_details.some(e => e.name == this.eventlognames[i])) {
            this.log_details.push(
              {
                "name": this.eventlognames[i],
                "panelOpenState": false,
                "details": {}
              }
            )
          }
        }
        this.loadDetails()
      }
      );

  }

  loadDetails() {
    for (let i in this.eventlognames) {
      for (let j in this.log_details) {
        if (this.log_details[j].name == this.eventlognames[i] && !Object.keys(this.log_details[j].details).length) {
          this.DetailSubs = this.logDetService
            .getDetails(this.eventlognames[i])
            .subscribe(res => {
              this.log_details[j].details = JSON.parse(res)
            }

            );
        }
      }
    }
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.fileName = file.name;
      this.DetailSubs = this.logDetService
        .importFile(file)
        .subscribe(res => {
          this.ngOnInit()
          console.log(res)
        }
        );
  }
  }
}

