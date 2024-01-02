import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Language } from 'src/app/models/Language';

@Component({
  selector: 'app-language-drop-down',
  templateUrl: './language-drop-down.component.html',
  styleUrls: ['./language-drop-down.component.css']
})
export class LanguageDropDownComponent {
  @Input() languages: Language[] = [];
  @Output() languageSelected = new EventEmitter<Language>();

  selectedLanguage: Language = { id: 'fr', name: 'Français' };
  isDropdownOpen = false;

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  selectLanguage(lang: Language) {
    this.selectedLanguage = lang;
    this.isDropdownOpen = false;
    this.languageSelected.emit(lang);
  }
}
