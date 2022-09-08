import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http'
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
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {
  fileName ='';
  displayedColumns: string[] = ['name', 'events'];
  dataSource = ELEMENT_DATA;

  constructor(private http: HttpClient) {}

    onFileSelected(event:any) {

        const file:File = event.target.files[0];

        if (file) {

            this.fileName = file.name;

            const formData = new FormData();

            formData.append("thumbnail", file);

            const upload$ = this.http.post("/api/thumbnail-upload", formData);

            upload$.subscribe();
        }
    }

  ngOnInit(): void {
  }

}
