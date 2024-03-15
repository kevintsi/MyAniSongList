import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from 'src/app/components/pagination/pagination.component';
import { SearchBarComponent } from 'src/app/components/search-bar/search-bar.component';
import { TranslateModule } from '@ngx-translate/core';
import { LoaderComponent } from 'src/app/components/loader/loader.component';

@NgModule({
    imports: [
        CommonModule,
        TranslateModule
    ],
    declarations: [
        PaginationComponent,
        SearchBarComponent,
        LoaderComponent,
    ],
    exports: [
        PaginationComponent,
        SearchBarComponent,
        LoaderComponent,
        TranslateModule
    ]
})
export class SharedModule { }
