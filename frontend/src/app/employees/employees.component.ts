import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { EmployeesService } from './employees.service';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  employees! : Object;
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
  console.log(this.employees)
  }
}
