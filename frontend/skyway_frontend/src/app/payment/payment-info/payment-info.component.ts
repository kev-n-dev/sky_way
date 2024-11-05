import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors, ReactiveFormsModule } from '@angular/forms';
import { PriceSummaryComponent } from '../price-summary/price-summary.component';
import { FlightDetailsComponent } from '../../flight-details/flight-details.component';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-payment-info',
  templateUrl: './payment-info.component.html',
  styleUrls: ['./payment-info.component.css'],
  imports: [ReactiveFormsModule, CommonModule, FlightDetailsComponent, PriceSummaryComponent],
  standalone: true
})
export class PaymentInfoComponent implements OnInit {
  paymentForm: FormGroup;
  bookingId!: string; // Property to store the booking ID

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router) {
    this.paymentForm = this.fb.group({
      cardholderName: ['', [Validators.required, Validators.minLength(3)]],
      cardNumber: ['', [Validators.required, Validators.pattern(/^\d{16}$/)]],
      expirationDate: ['', [Validators.required, this.expirationDateValidator]],
      cvv: ['', [Validators.required, Validators.pattern(/^\d{3}$/)]],
    });
  }

  ngOnInit(): void {
    // Retrieve booking ID from the route parameters
    this.route.params.subscribe(params => {
      this.bookingId = params['bookingId']; // Ensure 'bookingId' matches the URL parameter name
    });
  }

  expirationDateValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value;
    if (!value) return null;

    const [month, year] = value.split('/').map((v: string) => parseInt(v, 10));

    if (!month || !year) return { invalidDate: true }; // Handle cases where month/year might be invalid

    const expirationDate = new Date(Number(`20${year}`), month - 1);
    const today = new Date();

    return expirationDate < today ? { expired: true } : null;
  }

  navigateToConfirmation() {
    if (this.bookingId) {
      console.log("Navigating to confirmation with booking ID:", this.bookingId);
      this.router.navigate(['/booking/confirmation', this.bookingId]);
    } else {
      console.error("Booking ID is not defined!");
    }
  }

  onSubmit(): void {
    if (this.paymentForm.valid) {
      console.log('Payment Information:', this.paymentForm.value);
      // Navigate to confirmation page with the booking ID
      this.navigateToConfirmation();
    } else {
      console.log(this.paymentForm.errors);
    }
  }

  get formControls() {
    return this.paymentForm.controls;
  }
}
