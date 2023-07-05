import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormArtistComponent } from './form-artist.component';

describe('FormArtistComponent', () => {
  let component: FormArtistComponent;
  let fixture: ComponentFixture<FormArtistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormArtistComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormArtistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
