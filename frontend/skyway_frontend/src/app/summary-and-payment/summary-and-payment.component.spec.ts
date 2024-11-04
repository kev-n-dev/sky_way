import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SummaryAndPaymentComponent } from './summary-and-payment.component';

describe('SummaryAndPaymentComponent', () => {
  let component: SummaryAndPaymentComponent;
  let fixture: ComponentFixture<SummaryAndPaymentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SummaryAndPaymentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SummaryAndPaymentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
