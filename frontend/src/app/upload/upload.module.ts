import { NgModule } from '@angular/core'
import { CommonModule } from '@angular/common'
import { UploadComponent } from './upload.component'
import { MatModules } from '../material.module'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { FlexLayoutModule } from '@angular/flex-layout'
import { HttpClientModule } from '@angular/common/http'

@NgModule({
  imports: [
    CommonModule,
    MatModules,
    FlexLayoutModule,
    HttpClientModule,
    BrowserAnimationsModule,
  ],
  declarations: [UploadComponent],
  exports: [UploadComponent],
})
export class UploadModule {}