import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatModules } from './material.module';
import { FormsModule } from '@angular/forms';

import { ImportComponent } from './import/import.component';
import { ApplyingComponent , SaveDialog} from './applying/applying.component';
import { LogDetailsComponent } from './log-details/log-details.component';
import { EventtableComponent } from './eventtable/eventtable.component';
import { CdkDialogOverviewExampleDialog } from './eventtable/eventtable.component';


import { OverlayModule } from '@angular/cdk/overlay';


@NgModule({
  declarations: [
    AppComponent,
    ImportComponent,
    ApplyingComponent,
    LogDetailsComponent,
    EventtableComponent,
    CdkDialogOverviewExampleDialog,
    SaveDialog,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    MatModules,
    OverlayModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
