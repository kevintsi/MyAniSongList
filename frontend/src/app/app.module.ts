import { LOCALE_ID, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { HttpClient, HttpClientModule } from '@angular/common/http';
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
import { ReviewListComponent } from './components/review/review-list/review-list.component';
import { SharedModule } from './modules/shared/shared.module';
import { CommunityListComponent } from './components/community-list/community-list.component';
import { RankingMusicComponent } from './components/music/ranking-music/ranking-music.component';
import { FavoriteListComponent } from './components/favorite-list/favorite-list.component';
import { ProfileEditComponent } from './components/profile-edit/profile-edit.component';
import { NotFoundComponent } from './components/not-found/not-found.component';
import { ToastrModule } from 'ngx-toastr';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { LanguageDropDownComponent } from './components/language-drop-down/language-drop-down.component';
import { registerLocaleData } from '@angular/common';
import localeEn from '@angular/common/locales/en';
import localeJp from '@angular/common/locales/ja';
import localeJpExtra from '@angular/common/locales/extra/ja';
import localeFr from '@angular/common/locales/fr';
import localeFrExtra from '@angular/common/locales/extra/fr';

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
    ReviewListComponent,
    CommunityListComponent,
    RankingMusicComponent,
    FavoriteListComponent,
    ProfileEditComponent,
    NotFoundComponent,
    LanguageDropDownComponent,
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
    ToastrModule.forRoot(),
    HttpClientModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateLoader),
        deps: [HttpClient]
      },
      defaultLanguage: "fr"
    }
    )
  ],
  providers: [
    httpInterceptorProviders,
    { provide: LOCALE_ID, useValue: 'fr-FR' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor() {
    registerLocaleData(localeEn, 'en');
    registerLocaleData(localeJp, 'jp', localeJpExtra);
    registerLocaleData(localeFr, 'fr', localeFrExtra);
  }

}
export function createTranslateLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, "./assets/i18n/", ".json")
}
