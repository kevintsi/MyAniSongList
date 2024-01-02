import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LanguageDropDownComponent } from './language-drop-down.component';

describe('LanguageDropDownComponent', () => {
  let component: LanguageDropDownComponent;
  let fixture: ComponentFixture<LanguageDropDownComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LanguageDropDownComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LanguageDropDownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
