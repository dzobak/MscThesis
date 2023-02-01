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
  getEventLogNames(): Observable<string[]> {
    return this.http.get<string[]>('http://127.0.0.1:5002/applying/names');
  }

  getApplyingPage(): Observable<EventLogHeading[]> {
    return this.http.get<EventLogHeading[]>('http://127.0.0.1:5002/applying/default');
  }

  getEvents(logname: string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/eventLog' + logname);
  }

  getObjects(logname: string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/objects' + logname);
  }

  getLogData(logname: string): Observable<string> {
    return this.http.get<string>('http://127.0.0.1:5002/applying/logdata' + logname);
  }

  getColumnFuctions(eventlogname: string, isEventTransformation: boolean, isObjectTransformation: boolean): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/aggregation_functions',
      JSON.stringify({
        eventlogname: eventlogname,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
      }),
      httpOptions
    );
  }

  getSelection(regex: string, eventlogname: string, newLogName: string, scope_column: string,
    isEventTransformation: boolean, isObjectTransformation: boolean, object_type = ""): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/regex',
      JSON.stringify({
        eventlogname: eventlogname,
        scope_column: scope_column,
        newlogname: newLogName,
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

  // TODO: check if everything is filled out
  getAggregation(eventlogname: string, newLogName: string, scope: string, level: number, groupingKey: string, isEventTransformation: boolean,
    isObjectTransformation: boolean, columnFunctionMap: object, object_type: string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/aggregation',
      JSON.stringify({
        eventlogname: eventlogname,
        newlogname: newLogName,
        scope_column: scope,
        scope_level: level,
        grouping_key: groupingKey,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
        col_func_map: columnFunctionMap,
        object_type: object_type
      }),
      httpOptions
    );
  }


  getRelabelling(eventlogname: string, newLogName: string, relabelCommand: string, isEventTransformation: boolean,
    isObjectTransformation: boolean, object_type?: string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/relabel',
      JSON.stringify({
        eventlogname: eventlogname,
        newlogname: newLogName,
        relabel_command: relabelCommand,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
        object_type: object_type,
      }),
      httpOptions
    );
  }

  getOldRows(eventlogname: string, rows_index: object, isEventTransformation: boolean,
    isObjectTransformation: boolean): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/oldrows',
      JSON.stringify({
        eventlogname: eventlogname,
        rows_index: rows_index,
        is_event_transformation: isEventTransformation,
        is_object_transformation: isObjectTransformation,
      }),
      httpOptions
    );
  }

  saveLog(oldName: string, newName: string): Observable<string> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<string>('http://127.0.0.1:5002/applying/save',
      JSON.stringify({
        old_name: oldName,
        new_name: newName
      }),
      httpOptions
    );
  }
}
