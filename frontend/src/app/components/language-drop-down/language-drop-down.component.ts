import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-language-drop-down',
  templateUrl: './language-drop-down.component.html',
  styleUrls: ['./language-drop-down.component.css']
})
export class LanguageDropDownComponent {
  @Input() languages: any[] = [];
  @Output() languageSelected = new EventEmitter<any>();

  selectedLanguage: any = localStorage.getItem("lang") ?
    JSON.parse(String(localStorage.getItem("lang"))) : JSON.stringify({ id: "fr", code: "Français" })
  isDropdownOpen = false;

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  selectLanguage(lang: any) {
    this.selectedLanguage = lang;
    this.isDropdownOpen = false;
    this.languageSelected.emit(lang);
  }
}
