import { NgModule } from "@angular/core";
import { MatButtonModule} from '@angular/material/button';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatDialogModule} from '@angular/material/dialog';
import {MatListModule} from '@angular/material/list';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatTableModule} from '@angular/material/table'

@NgModule({
    exports:[
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatToolbarModule,
        MatDialogModule,
        MatListModule,
        MatProgressBarModule,
        MatTableModule,
    ]
})
export class MatModules{}