import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeesComponent } from './employees/employees.component';
import { ImportComponent } from './import/import.component';

const routes: Routes = [
  {path: "employees", component: EmployeesComponent},
  {path: "import", component: ImportComponent}
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
