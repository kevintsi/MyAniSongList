import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageArtistComponent } from './manage-artist.component';

describe('ManageArtistComponent', () => {
  let component: ManageArtistComponent;
  let fixture: ComponentFixture<ManageArtistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageArtistComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageArtistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
