import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateArtistComponent } from './manage-create-artist.component';

describe('ManageCreateArtistComponent', () => {
  let component: ManageCreateArtistComponent;
  let fixture: ComponentFixture<ManageCreateArtistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateArtistComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateArtistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
