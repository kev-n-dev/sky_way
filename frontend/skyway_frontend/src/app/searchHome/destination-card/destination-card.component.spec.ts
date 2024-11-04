import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DestinationCardComponent } from './destination-card.component';

describe('DestinationCardComponent', () => {
  let component: DestinationCardComponent;
  let fixture: ComponentFixture<DestinationCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DestinationCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DestinationCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
