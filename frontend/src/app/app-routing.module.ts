import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeesComponent } from './employees/employees.component';
import { ImportComponent } from './import/import.component';
import { ApplyingComponent } from './applying/applying.component';
import { ExportComponent } from './export/export.component';

const routes: Routes = [
  {path: "employees", component: EmployeesComponent},
  {path: "import", component: ImportComponent},
  {path: "applying", component:ApplyingComponent},
  {path: "export", component:ExportComponent}
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
