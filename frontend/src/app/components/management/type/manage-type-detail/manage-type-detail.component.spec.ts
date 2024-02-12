import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTypeDetailComponent } from './manage-type-detail.component';

describe('ManageAnimeDetailComponent', () => {
  let component: ManageTypeDetailComponent;
  let fixture: ComponentFixture<ManageTypeDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageTypeDetailComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ManageTypeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
