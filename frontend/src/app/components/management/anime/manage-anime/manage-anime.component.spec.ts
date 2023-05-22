import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageAnimeComponent } from './manage-anime.component';

describe('ManageAnimeComponent', () => {
  let component: ManageAnimeComponent;
  let fixture: ComponentFixture<ManageAnimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageAnimeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageAnimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
