import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { LoginComponent } from './components/login/login.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { HomeComponent } from './components/home/home.component';
import { ProfileComponent } from './components/profile/profile.component';
import { httpInterceptorProviders } from './_helpers/http.interceptor';
import { AnimeListComponent } from './components/anime/anime-list/anime-list.component';
import { ManageComponent } from './components/management/manage/manage.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { AnimeDetailComponent } from './components/anime/anime-detail/anime-detail.component';
import { ArtistListComponent } from './components/artist/artist-list/artist-list.component';
import { ArtistDetailComponent } from './components/artist/artist-detail/artist-detail.component';
import { MusicListComponent } from './components/music/music-list/music-list.component';
import { MusicDetailComponent } from './components/music/music-detail/music-detail.component';
import { RatingStarsComponent } from './components/rating-stars/rating-stars.component';
import { ReviewShortListComponent } from './components/review/review-short-list/review-short-list.component';
import { ReviewDetailComponent } from './components/review/review-detail/review-detail.component';
import { ReviewListComponent } from './components/review/review-list/review-list.component';
import { SharedModule } from './modules/shared/shared.module';
import { CommunityListComponent } from './components/community-list/community-list.component';
import { RankingMusicComponent } from './components/music/ranking-music/ranking-music.component';
import { FavoriteListComponent } from './components/favorite-list/favorite-list.component';
import { ProfileEditComponent } from './components/profile-edit/profile-edit.component';

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
    ArtistListComponent,
    ArtistDetailComponent,
    MusicListComponent,
    MusicDetailComponent,
    RatingStarsComponent,
    ReviewShortListComponent,
    ReviewDetailComponent,
    ReviewListComponent,
    CommunityListComponent,
    RankingMusicComponent,
    FavoriteListComponent,
    ProfileEditComponent,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatIconModule,
    SharedModule,
  ],
  providers: [
    httpInterceptorProviders
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
