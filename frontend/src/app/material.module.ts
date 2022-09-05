import { NgModule } from "@angular/core";
import { MatButtonModule} from '@angular/material/button';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';

@NgModule({
    exports:[
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatToolbarModule
    ]
})
export class MaterialModules{}