import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageArtistDetailComponent } from './manage-artist-detail.component';

describe('ManageArtistDetailComponent', () => {
  let component: ManageArtistDetailComponent;
  let fixture: ComponentFixture<ManageArtistDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageArtistDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageArtistDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
