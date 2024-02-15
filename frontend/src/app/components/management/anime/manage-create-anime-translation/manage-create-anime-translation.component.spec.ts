import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCreateAnimeTranslationComponent } from './manage-create-anime-translation.component';

describe('ManageCreateAnimeTranslationComponent', () => {
  let component: ManageCreateAnimeTranslationComponent;
  let fixture: ComponentFixture<ManageCreateAnimeTranslationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCreateAnimeTranslationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageCreateAnimeTranslationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
