import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateLanguageComponent } from './manage-create-language.component';

describe('ManageCreateLanguageComponent', () => {
  let component: ManageCreateLanguageComponent;
  let fixture: ComponentFixture<ManageCreateLanguageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateLanguageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateLanguageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
