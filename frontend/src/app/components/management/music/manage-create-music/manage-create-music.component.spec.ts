import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateMusicComponent } from './manage-create-music.component';

describe('ManageCreateMusicComponent', () => {
  let component: ManageCreateMusicComponent;
  let fixture: ComponentFixture<ManageCreateMusicComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateMusicComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateMusicComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
