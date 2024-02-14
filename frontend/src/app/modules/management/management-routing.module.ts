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
import { ManageLanguageComponent } from 'src/app/components/management/language/manage-language/manage-language.component';
import { ManageCreateLanguageComponent } from 'src/app/components/management/language/manage-create-language/manage-create-language.component';
import { ManageLanguageDetailComponent } from 'src/app/components/management/language/manage-language-detail/manage-language-detail.component';
import { ManageTypeComponent } from 'src/app/components/management/type/manage-type/manage-type.component';
import { ManageCreateTypeComponent } from 'src/app/components/management/type/manage-create-type/manage-create-type.component';
import { ManageTypeDetailComponent } from 'src/app/components/management/type/manage-type-detail/manage-type-detail.component';
import { ManageCreateTypeTranslationComponent } from 'src/app/components/management/type/manage-create-type-translation/manage-create-type-translation.component';

const routes: Routes = [
  {
    path: 'languages', children: [
      { path: '', component: ManageLanguageComponent, pathMatch: 'full' },
      { path: 'create', component: ManageCreateLanguageComponent },
      { path: ':id', component: ManageLanguageDetailComponent },
    ],
  },
  {
    path: 'types', children: [
      { path: '', component: ManageTypeComponent, pathMatch: 'full' },
      { path: 'create', component: ManageCreateTypeComponent },
      {
        path: ':id', children: [
          { path: '', component: ManageTypeDetailComponent, pathMatch: 'full' },
          { path: 'createTranslation', component: ManageCreateTypeTranslationComponent }
        ]
      },

    ],
  },
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
