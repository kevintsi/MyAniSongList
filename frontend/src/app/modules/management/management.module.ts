import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ManagementRoutingModule } from './management-routing.module';
import { ManageAnimeComponent } from '../../components/management/anime/manage-anime/manage-anime.component';
import { ManageAnimeDetailComponent } from '../../components/management/anime/manage-anime-detail/manage-anime-detail.component';
import { ManageCreateAnimeComponent } from '../../components/management/anime/manage-create-anime/manage-create-anime.component';
import { ManageArtistComponent } from '../../components/management/artist/manage-artist/manage-artist.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { ManageCreateArtistComponent } from 'src/app/components/management/artist/manage-create-artist/manage-create-artist.component';
import { ManageArtistDetailComponent } from 'src/app/components/management/artist/manage-artist-detail/manage-artist-detail.component';
import { ManageMusicComponent } from 'src/app/components/management/music/manage-music/manage-music.component';
import { ManageMusicDetailComponent } from 'src/app/components/management/music/manage-music-detail/manage-music-detail.component';
import { ManageCreateMusicComponent } from 'src/app/components/management/music/manage-create-music/manage-create-music.component';
import { SharedModule } from '../shared/shared.module';
import { FormAnimeComponent } from 'src/app/components/management/anime/form-anime/form-anime.component';
import { FormMusicComponent } from 'src/app/components/management/music/form-music/form-music.component';
import { FormArtistComponent } from 'src/app/components/management/artist/form-artist/form-artist.component';

@NgModule({
  declarations: [
    ManageAnimeComponent,
    ManageAnimeDetailComponent,
    ManageCreateAnimeComponent,
    ManageArtistComponent,
    ManageCreateArtistComponent,
    ManageArtistDetailComponent,
    ManageMusicComponent,
    ManageMusicDetailComponent,
    ManageCreateMusicComponent,
    FormAnimeComponent,
    FormMusicComponent,
    FormArtistComponent,
  ],
  imports: [
    CommonModule,
    ManagementRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    SharedModule,
  ]
})
export class ManagementModule { }
