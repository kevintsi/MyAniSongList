import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormTypeComponent } from './form-type.component';

describe('FormTypeComponent', () => {
  let component: FormTypeComponent;
  let fixture: ComponentFixture<FormTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FormTypeComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(FormTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
