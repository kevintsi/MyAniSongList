import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageLanguageDetailComponent } from './manage-language-detail.component';

describe('ManageLanguageDetailComponent', () => {
  let component: ManageLanguageDetailComponent;
  let fixture: ComponentFixture<ManageLanguageDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageLanguageDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageLanguageDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
