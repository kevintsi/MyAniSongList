import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateAnimeComponent } from './manage-create-anime.component';

describe('ManageCreateAnimeComponent', () => {
  let component: ManageCreateAnimeComponent;
  let fixture: ComponentFixture<ManageCreateAnimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateAnimeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateAnimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
