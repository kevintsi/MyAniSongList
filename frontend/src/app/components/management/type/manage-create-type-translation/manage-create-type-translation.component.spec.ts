import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateTypeTranslationComponent } from './manage-create-type-translation.component';

describe('ManageCreateTypeTranslationComponent', () => {
  let component: ManageCreateTypeTranslationComponent;
  let fixture: ComponentFixture<ManageCreateTypeTranslationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateTypeTranslationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateTypeTranslationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
