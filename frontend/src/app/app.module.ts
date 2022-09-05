import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { EmployeesComponent } from './employees/employees.component';
import { EmployeesService } from './employees/employees.service';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';

import { MaterialModules } from './material.module';

import {ImportComponent } from './import/import.component';
import {ApplyingComponent } from './applying/applying.component';
import {ExportComponent } from './export/export.component';


@NgModule({
  declarations: [
    AppComponent,
    EmployeesComponent,
    ImportComponent,
    ApplyingComponent,
    ExportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MaterialModules,
    FlexLayoutModule,
    BrowserAnimationsModule,
  ],
  providers: [EmployeesService],
  bootstrap: [AppComponent]
})
export class AppModule { }
