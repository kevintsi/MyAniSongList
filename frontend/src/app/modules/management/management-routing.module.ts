import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ManageAnimeComponent } from '../../components/management/anime/manage-anime/manage-anime.component';
import { ManageAnimeDetailComponent } from '../../components/management/anime/manage-anime-detail/manage-anime-detail.component';
import { ManageCreateAnimeComponent } from '../../components/management/anime/manage-create-anime/manage-create-anime.component';
import { ManageArtistComponent } from '../../components/management/artist/manage-artist/manage-artist.component';
import { ManageCreateArtistComponent } from 'src/app/components/management/artist/manage-create-artist/manage-create-artist.component';
import { ManageArtistDetailComponent } from 'src/app/components/management/artist/manage-artist-detail/manage-artist-detail.component';
import { ManageMusicComponent } from 'src/app/components/management/music/manage-music/manage-music.component';
import { ManageCreateMusicComponent } from 'src/app/components/management/music/manage-create-music/manage-create-music.component';
import { ManageMusicDetailComponent } from 'src/app/components/management/music/manage-music-detail/manage-music-detail.component';

const routes: Routes = [
  {
    path: 'animes', children: [
      { path: '', component: ManageAnimeComponent, pathMatch: 'full' },
      { path: 'create', component: ManageCreateAnimeComponent },
      { path: ':id', component: ManageAnimeDetailComponent },
    ],
  },

  {
    path: 'artists', children: [
      { path: '', component: ManageArtistComponent, pathMatch: 'full' },
      { path: 'create', component: ManageCreateArtistComponent },
      { path: ':id', component: ManageArtistDetailComponent },
    ]
  },
  {
    path: 'musics', children: [
      { path: '', component: ManageMusicComponent, pathMatch: 'full' },
      { path: 'create', component: ManageCreateMusicComponent },
      { path: ':id', component: ManageMusicDetailComponent },
    ]
  },
  { path: '', redirectTo: 'animes', pathMatch: 'full' },
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManagementRoutingModule { }
