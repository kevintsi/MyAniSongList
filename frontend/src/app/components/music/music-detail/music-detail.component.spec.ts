import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MusicDetailComponent } from './music-detail.component';

describe('MusicDetailComponent', () => {
  let component: MusicDetailComponent;
  let fixture: ComponentFixture<MusicDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MusicDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MusicDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
