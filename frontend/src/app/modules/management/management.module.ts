import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ManagementRoutingModule } from './management-routing.module';
import { ManageAnimeComponent } from '../../components/management/anime/manage-anime/manage-anime.component';
import { ManageAnimeDetailComponent } from '../../components/management/anime/manage-anime-detail/manage-anime-detail.component';
import { ManageCreateAnimeComponent } from '../../components/management/anime/manage-create-anime/manage-create-anime.component';
import { ManageArtistComponent } from '../../components/management/artist/manage-artist/manage-artist.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { ManageComponent } from '../../components/management/manage/manage.component';



@NgModule({
  declarations: [
    ManageAnimeComponent,
    ManageAnimeDetailComponent,
    ManageCreateAnimeComponent,
    ManageArtistComponent
  ],
  imports: [
    CommonModule,
    ManagementRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatIconModule,
  ]
})
export class ManagementModule { }
