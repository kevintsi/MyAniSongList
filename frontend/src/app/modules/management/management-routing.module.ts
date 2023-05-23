import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ManageAnimeComponent } from '../../components/management/anime/manage-anime/manage-anime.component';
import { ManageAnimeDetailComponent } from '../../components/management/anime/manage-anime-detail/manage-anime-detail.component';
import { ManageCreateAnimeComponent } from '../../components/management/anime/manage-create-anime/manage-create-anime.component';
import { ManageArtistComponent } from '../../components/management/artist/manage-artist/manage-artist.component';
import { ManageCreateArtistComponent } from 'src/app/components/management/artist/manage-create-artist/manage-create-artist.component';
import { ManageArtistDetailComponent } from 'src/app/components/management/artist/manage-artist-detail/manage-artist-detail.component';

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
  { path: '', redirectTo: 'animes', pathMatch: 'full' },
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManagementRoutingModule { }
