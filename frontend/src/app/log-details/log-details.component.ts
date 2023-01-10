import { Component, ViewChild, OnInit } from '@angular/core';
import { MatAccordion } from '@angular/material/expansion';
import { ApplyingService } from '../applying/applying.service'
import { Subscription } from 'rxjs';
import { LogDetailsService } from './log-details.service';
import {FormControl} from '@angular/forms';




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
  saveVal = true;
  log_details: LogDetails[] = [];

  NamesSubs!: Subscription;
  DetailSubs!: Subscription;
  eventlognames: string[] = [];
  newEventlogs: string[] = []

  // For tooltips
  showDelay = new FormControl(1000);
  hideDelay = new FormControl(500);

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
          let DetailSubs = new Subscription()
          DetailSubs = this.logDetService
            .getDetails(this.eventlognames[i])
            .subscribe(res => {
              this.log_details[j].details = JSON.parse(res)
              // console.log(this.log_details[j].details)
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

  deleteFile(name: string) {
    this.DetailSubs = this.logDetService
      .deleteFile(name)
      .subscribe(res => {
        var index = this.eventlognames.indexOf(name);
        if (index !== -1) {
          this.eventlognames.splice(index, 1);
        }
        var filtered = this.log_details.filter(function (log) { return log.name != name; });
        this.log_details = filtered
      }
      );
  }

  downloadUrl(name:string){
    window.open('http://127.0.0.1:5002/eventlogs/' + name, '_blank');
  }

}

