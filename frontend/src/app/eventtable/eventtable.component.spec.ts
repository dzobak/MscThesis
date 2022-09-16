import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventtableComponent } from './eventtable.component';

describe('EventtableComponent', () => {
  let component: EventtableComponent;
  let fixture: ComponentFixture<EventtableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventtableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EventtableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
