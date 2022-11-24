import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Observable, throwError } from 'rxjs';
// import { catchError, retry } from 'rxjs/operators';

export interface EventLogHeading {
  value: string,
  e_scopes: string[],
  e_columns: string[],
  o_scopes: string[],
  o_columns: string[],
}

@Injectable({
  providedIn: 'root'
})
export class ApplyingService {
  constructor(private http: HttpClient) { }

  getApplyingPage(): Observable<EventLogHeading[]> {
    return this.http.get<EventLogHeading[]>('http://127.0.0.1:5002/applying/default');
  }

  getEvents(logname: string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/eventLog' + logname);
  }

  getObjects(logname: string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/objects' + logname);
  }

  getSelection(regex: string, eventlogname: string, scope_column: string,
    isEventTransformation: boolean, isObjectTransformation: boolean, object_type=""): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/regex',
      JSON.stringify({
        eventlog: eventlogname,
        scope_column: scope_column,
        regex: regex,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
        object_type: object_type
      }),
      httpOptions
    );
  }

  getScopeLevels(eventlogname: string, scope_column: string, isEventTransformation: boolean,
    isObjectTransformation: boolean): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/scopelevel',
      JSON.stringify({
        eventlog: eventlogname,
        scope_column: scope_column,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
      }),
      httpOptions
    );
  }


  getAggregation(eventlogname: string, scope: string, level: number, isEventTransformation: boolean,
    isObjectTransformation: boolean, object_type: string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/aggregation',
      JSON.stringify({
        eventlogname: eventlogname,
        scope_column: scope,
        scope_level: level,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
        object_type: object_type
      }),
      httpOptions
    );
  }
}
