import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';

import { MatModules } from './material.module';
import { FormsModule } from '@angular/forms';

import { ImportComponent } from './import/import.component';
import { ApplyingComponent } from './applying/applying.component';
import { ExportComponent } from './export/export.component';
import { LogDetailsComponent } from './log-details/log-details.component';
import { EventtableComponent } from './eventtable/eventtable.component';


@NgModule({
  declarations: [
    AppComponent,
    ImportComponent,
    ApplyingComponent,
    ExportComponent,
    LogDetailsComponent,
    EventtableComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FlexLayoutModule,
    FormsModule,
    MatModules,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
