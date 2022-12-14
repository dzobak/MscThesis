import { NgModule } from "@angular/core";
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';
import { MatTabsModule } from '@angular/material/tabs';
import { MatInputModule } from '@angular/material/input';
import { MatRadioModule } from '@angular/material/radio'
import { MatSliderModule } from '@angular/material/slider';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {MatTooltipModule} from '@angular/material/tooltip'
// import {MatLegacySliderModule} from '@angular/material/legacy-slider';


@NgModule({
    exports: [
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatToolbarModule,
        MatDialogModule,
        MatListModule,
        MatProgressBarModule,
        MatTableModule,
        MatCardModule,
        MatExpansionModule,
        MatSelectModule,
        MatTabsModule,
        MatInputModule,
        MatSliderModule,
        // MatLegacySliderModule,
        MatRadioModule,
        DragDropModule,
        MatTooltipModule,
    ]
})
export class MatModules { }