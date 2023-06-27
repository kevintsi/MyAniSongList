import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from 'src/app/components/pagination/pagination.component';
import { SearchBarComponent } from 'src/app/components/search-bar/search-bar.component';

@NgModule({
    imports: [
        CommonModule
    ],
    declarations: [
        PaginationComponent,
        SearchBarComponent
    ],
    exports: [
        PaginationComponent,
        SearchBarComponent
    ]
})
export class SharedModule { }
