import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LogDetailsService {

  constructor(private http: HttpClient) { }

  getDetails(eventlogname: string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/eventlogs/details',
      JSON.stringify({
        eventlog: eventlogname,
      }),
      httpOptions
    );
  }
  importFile(file:any): Observable<string>{
    const formData = new FormData();

      formData.append("log", file);
      formData.append("name", file.name.split(".jsonocel")[0]);
    

      return this.http.post<string>("http://127.0.0.1:5002/eventlogs/import", formData);
  }
  
  deleteFile(name:string): Observable<object>{
    console.log(name)
    return this.http.get<object>("http://127.0.0.1:5002/eventlogs/"+name);
  }
}
