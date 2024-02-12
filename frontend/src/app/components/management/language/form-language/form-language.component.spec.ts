import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormLanguageComponent } from './form-language.component';

describe('FormLanguageComponent', () => {
  let component: FormLanguageComponent;
  let fixture: ComponentFixture<FormLanguageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormLanguageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormLanguageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
