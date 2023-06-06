import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms'
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { LoginComponent } from './components/login/login.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { httpInterceptorProviders } from './_helpers/http.interceptor';
import { AnimeListComponent } from './components/animes/anime-list/anime-list.component';
import { ManageComponent } from './components/management/manage/manage.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { AnimeDetailComponent } from './components/animes/anime-detail/anime-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    RegistrationComponent,
    LoginComponent,
    HomeComponent,
    ProfileComponent,
    AnimeListComponent,
    ManageComponent,
    AnimeDetailComponent,

  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatIconModule,
  ],
  providers: [
    httpInterceptorProviders
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
