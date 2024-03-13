import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from 'src/app/components/pagination/pagination.component';
import { SearchBarComponent } from 'src/app/components/search-bar/search-bar.component';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
    imports: [
        CommonModule,
        TranslateModule
    ],
    declarations: [
        PaginationComponent,
        SearchBarComponent
    ],
    exports: [
        PaginationComponent,
        SearchBarComponent,
        TranslateModule
    ]
})
export class SharedModule { }
