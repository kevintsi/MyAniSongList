import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageMusicDetailComponent } from './manage-music-detail.component';

describe('ManageMusicDetailComponent', () => {
  let component: ManageMusicDetailComponent;
  let fixture: ComponentFixture<ManageMusicDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageMusicDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageMusicDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
