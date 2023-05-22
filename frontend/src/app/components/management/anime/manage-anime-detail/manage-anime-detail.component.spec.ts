import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageAnimeDetailComponent } from './manage-anime-detail.component';

describe('ManageAnimeDetailComponent', () => {
  let component: ManageAnimeDetailComponent;
  let fixture: ComponentFixture<ManageAnimeDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageAnimeDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageAnimeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
