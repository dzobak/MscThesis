import { JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { EmployeesService } from './employees.service';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit, OnDestroy {
  employees: JSON|any;
  employeesSubs!: Subscription;
  constructor(private emplSer : EmployeesService) { }

  ngOnInit() {
    console.log("hello")
    this.employeesSubs = this.emplSer
    .getEmployees()
    .subscribe(res => {
      this.employees = res;
    }
  );
  }
  ngOnDestroy() {
    this.employeesSubs.unsubscribe();
  }

}
