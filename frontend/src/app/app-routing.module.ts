import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component'
import { isSignedInGuard, notSignedInGuard } from './guards/authguard.service';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { AnimeListComponent } from './components/anime-list/anime-list.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ManageComponent } from './components/management/manage/manage.component';
import { AnimeDetailComponent } from './components/anime-detail/anime-detail.component';


const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [notSignedInGuard] },
  { path: 'register', component: RegistrationComponent, canActivate: [notSignedInGuard] },
  { path: 'profile', component: ProfileComponent },
  {
    path: 'animes', children: [
      { path: '', component: AnimeListComponent },
      { path: ':id', component: AnimeDetailComponent }
    ]
  },
  { path: 'manage', component: ManageComponent, loadChildren: () => import("./modules/management/management.module").then(m => m.ManagementModule) },

]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
