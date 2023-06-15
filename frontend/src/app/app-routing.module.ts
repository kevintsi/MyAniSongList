import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component'
import { isSignedInGuard, notSignedInGuard } from './guards/authguard.service';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { AnimeListComponent } from './components/anime/anime-list/anime-list.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ManageComponent } from './components/management/manage/manage.component';
import { AnimeDetailComponent } from './components/anime/anime-detail/anime-detail.component';
import { ArtistListComponent } from './components/artist/artist-list/artist-list.component';
import { ArtistDetailComponent } from './components/artist/artist-detail/artist-detail.component';
import { MusicListComponent } from './components/music/music-list/music-list.component';
import { MusicDetailComponent } from './components/music/music-detail/music-detail.component';


const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [notSignedInGuard] },
  { path: 'register', component: RegistrationComponent, canActivate: [notSignedInGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [isSignedInGuard] },
  {
    path: 'animes', children: [
      { path: '', component: AnimeListComponent },
      { path: ':id', component: AnimeDetailComponent }
    ]
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
      { path: ':id', component: MusicDetailComponent }
    ]
  },
  { path: 'manage', component: ManageComponent, loadChildren: () => import("./modules/management/management.module").then(m => m.ManagementModule) },

]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
