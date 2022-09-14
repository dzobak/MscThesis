import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
import { Observable, throwError } from 'rxjs';
// import { catchError, retry } from 'rxjs/operators';

interface EventLog{
  value: string,
  scopes: String[]
}

@Injectable({
  providedIn: 'root'
})
export class ApplyingService {
  constructor(private http: HttpClient) { }

  getApplyingPage(): Observable<EventLog[]>{
    return this.http.get<EventLog[]>('http://127.0.0.1:5002/applying/default');
  }

  getEventLog(): Observable<Object> {
    return this.http.get('http://127.0.0.1:5002/applying/eventLog'); 
  }
}
