import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component'
import { isSignedInGuard, notSignedInGuard } from './guards/authguard.service';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { AnimeListComponent } from './components/anime-list/anime-list.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ManageComponent } from './components/manage/manage.component';
import { ManageAnimeComponent } from './components/manage-anime/manage-anime.component';
import { ManageArtistComponent } from './components/manage-artist/manage-artist.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, canActivate: [notSignedInGuard] },
  { path: 'register', component: RegistrationComponent, canActivate: [notSignedInGuard] },
  { path: 'profile', component: ProfileComponent },
  { path: 'animes', component: AnimeListComponent },
  {
    path: 'manage', component: ManageComponent, children: [
      { path: 'animes', component: ManageAnimeComponent },
      { path: 'artists', component: ManageArtistComponent }
    ]
  },
  { path: '', component: HomeComponent, pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
