import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormMusicComponent } from './form-music.component';

describe('FormMusicComponent', () => {
  let component: FormMusicComponent;
  let fixture: ComponentFixture<FormMusicComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormMusicComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormMusicComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
