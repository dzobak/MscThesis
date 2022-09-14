import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
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

  getEventLog(logname:string): Observable<Object> {
    return this.http.get('http://127.0.0.1:5002/applying/eventLog'+ logname); 
  }
}
