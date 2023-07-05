import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormAnimeComponent } from './form-anime.component';

describe('FormAnimeComponent', () => {
  let component: FormAnimeComponent;
  let fixture: ComponentFixture<FormAnimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormAnimeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormAnimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
