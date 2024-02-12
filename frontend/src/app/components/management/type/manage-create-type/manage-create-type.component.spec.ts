import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateTypeComponent } from './manage-create-type.component';

describe('ManageCreateAnimeComponent', () => {
  let component: ManageCreateTypeComponent;
  let fixture: ComponentFixture<ManageCreateTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageCreateTypeComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ManageCreateTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
