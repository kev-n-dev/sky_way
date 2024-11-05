import { Component } from '@angular/core';
 import { PaymentInfoComponent } from '../payment-info/payment-info.component';
 
@Component({
  selector: 'app-summary-and-payment',
  standalone: true,
  imports: [ PaymentInfoComponent],
  templateUrl: './summary-and-payment.component.html',
  styleUrl: './summary-and-payment.component.css'
})
export class SummaryAndPaymentComponent {
//  do call to get flight info 



}
