import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplyingComponent } from './applying.component';

describe('ApplyingComponent', () => {
  let component: ApplyingComponent;
  let fixture: ComponentFixture<ApplyingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ApplyingComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ApplyingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
