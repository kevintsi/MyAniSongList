import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component'
import { ManagerGuard, isSignedInGuard, notSignedInGuard } from './guards/auth.guard';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { ProfileEditComponent } from './components/profile-edit/profile-edit.component';
import { AnimeListComponent } from './components/anime/anime-list/anime-list.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ManageComponent } from './components/management/manage/manage.component';
import { AnimeDetailComponent } from './components/anime/anime-detail/anime-detail.component';
import { ArtistListComponent } from './components/artist/artist-list/artist-list.component';
import { ArtistDetailComponent } from './components/artist/artist-detail/artist-detail.component';
import { MusicListComponent } from './components/music/music-list/music-list.component';
import { MusicDetailComponent } from './components/music/music-detail/music-detail.component';
import { ReviewListComponent } from './components/review/review-list/review-list.component';
import { CommunityListComponent } from './components/community-list/community-list.component';
import { RankingMusicComponent } from './components/music/ranking-music/ranking-music.component';
import { FavoriteListComponent } from './components/favorite-list/favorite-list.component';
import { NotFoundComponent } from './components/not-found/not-found.component';


const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [notSignedInGuard] },
  { path: 'register', component: RegistrationComponent, canActivate: [notSignedInGuard] },
  { path: 'editProfile', component: ProfileEditComponent, canActivate: [isSignedInGuard] },
  {
    path: 'profile', children: [
      { path: ':id', component: ProfileComponent }
    ]
  },
  {
    path: 'animes', children: [
      { path: '', component: AnimeListComponent },
      { path: ':id', component: AnimeDetailComponent }
    ]
  },
  {
    path: 'favorites', component: FavoriteListComponent
  },
  {
    path: 'artists', children: [
      { path: '', component: ArtistListComponent },
      { path: ':id', component: ArtistDetailComponent }
    ]
  },
  {
    path: 'musics', children: [
      { path: '', component: MusicListComponent },
      { path: 'ranking', component: RankingMusicComponent },
      { path: ':id', component: MusicDetailComponent },
    ]
  },
  {
    path: 'reviews', children: [
      { path: ':id_music', component: ReviewListComponent },
    ]
  },
  {
    path: 'community', children: [
      { path: '', component: CommunityListComponent },
    ]
  },
  { path: 'manage', component: ManageComponent, loadChildren: () => import("./modules/management/management.module").then(m => m.ManagementModule), canActivate: [ManagerGuard] },
  { path: '**', component: NotFoundComponent }

]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
