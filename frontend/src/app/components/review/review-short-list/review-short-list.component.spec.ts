import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReviewShortListComponent } from './review-short-list.component';

describe('ReviewListComponent', () => {
  let component: ReviewShortListComponent;
  let fixture: ComponentFixture<ReviewShortListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReviewShortListComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ReviewShortListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
