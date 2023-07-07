import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RankingMusicComponent } from './ranking-music.component';

describe('RankingMusicComponent', () => {
  let component: RankingMusicComponent;
  let fixture: ComponentFixture<RankingMusicComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RankingMusicComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RankingMusicComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
