import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-language-drop-down',
  templateUrl: './language-drop-down.component.html',
  styleUrls: ['./language-drop-down.component.css']
})
export class LanguageDropDownComponent implements OnInit {

  @Input() languages: any[] = [];
  @Output() languageSelected = new EventEmitter<any>();

  selectedLanguage: any
  isDropdownOpen = false;

  ngOnInit(): void {
    this.selectedLanguage = localStorage.getItem("lang") ?
      JSON.parse(String(localStorage.getItem("lang"))) : { id: "fr", code: "Français" }

    localStorage.setItem("lang", JSON.stringify(this.selectedLanguage))
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  selectLanguage(lang: any) {
    this.selectedLanguage = lang;
    this.isDropdownOpen = false;
    this.languageSelected.emit(lang);
  }
}
