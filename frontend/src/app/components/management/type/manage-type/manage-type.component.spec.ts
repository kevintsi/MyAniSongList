import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTypeComponent } from './manage-type.component';

describe('ManageTypeComponent', () => {
  let component: ManageTypeComponent;
  let fixture: ComponentFixture<ManageTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageTypeComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ManageTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
