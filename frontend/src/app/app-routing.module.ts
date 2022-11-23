import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ImportComponent } from './import/import.component';
import { ApplyingComponent } from './applying/applying.component';
import { LogDetailsComponent } from './log-details/log-details.component';

const routes: Routes = [
  {path: "import", component: ImportComponent},
  {path: "applying", component:ApplyingComponent},
  {path: "logs", component:LogDetailsComponent},
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
