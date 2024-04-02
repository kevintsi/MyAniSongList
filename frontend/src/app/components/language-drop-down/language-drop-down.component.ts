import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { AppLanguages, getLangFromStorage } from 'src/app/config/lang.config';
import { LANGUAGE_STORAGE_KEY } from 'src/app/config/storage.config';
import { AppLanguage } from 'src/app/interfaces/app-language.interface';

@Component({
  selector: 'app-language-drop-down',
  templateUrl: './language-drop-down.component.html',
  styleUrls: ['./language-drop-down.component.css']
})
export class LanguageDropDownComponent implements OnInit {

  @Input() languages: AppLanguage[] = []
  @Output() languageSelected = new EventEmitter<any>();

  selectedLanguage: AppLanguage = AppLanguages[0]
  isDropdownOpen = false;

  ngOnInit(): void {
    this.selectedLanguage = getLangFromStorage()
    localStorage.setItem(LANGUAGE_STORAGE_KEY, this.selectedLanguage.id)
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  selectLanguage(lang: AppLanguage) {
    this.selectedLanguage = lang;
    this.isDropdownOpen = false;
    this.languageSelected.emit(lang);
  }
}
