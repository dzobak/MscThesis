import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http'
import { Observable, throwError } from 'rxjs';
// import { catchError, retry } from 'rxjs/operators';

interface EventLogHeading{
  value: string,
  scopes: String[]
}

@Injectable({
  providedIn: 'root'
})
export class ApplyingService {
  constructor(private http: HttpClient) { }

  getApplyingPage(): Observable<EventLogHeading[]>{
    return this.http.get<EventLogHeading[]>('http://127.0.0.1:5002/applying/default');
  }

  getEventLog(logname:string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/eventLog'+ logname); 
  }

  getSelection(regex:string, eventlogname:string, scope:string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/regex', 
           JSON.stringify({eventlog:eventlogname, scope:scope, regex:regex}),
           httpOptions
           ); 
  }
}
