import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LogDetailsComponent } from '../log-details/log-details.component';



@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {
  fileName = '';


  constructor(private http: HttpClient) { }

  onFileSelected(event: any) {

    const file: File = event.target.files[0];
    if (file) {

      this.fileName = file.name;

      const formData = new FormData();

      formData.append("log", file);
      formData.append("name", file.name.split(".jsonocel")[0]);
    

      const upload$ = this.http.post("http://127.0.0.1:5002/eventlogs/import", formData);

      upload$.subscribe(
      );
    }
  }

  ngOnInit(): void {
  }

}
