import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageLanguageComponent } from './manage-language.component';

describe('ManageLanguageComponent', () => {
  let component: ManageLanguageComponent;
  let fixture: ComponentFixture<ManageLanguageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageLanguageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageLanguageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
