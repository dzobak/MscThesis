import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class EmployeesService {
  constructor(private http: HttpClient) { }

  getEmployees(): Observable<Object>{
    var emp = this.http.get('http://127.0.0.1:5002/employees');
    console.log("**")
    console.log(emp)
    return emp
  }
}
