import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingService } from '../../../services/booking.service';

@Component({
  selector: 'app-passenger-list',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule], // Add your directive here
  templateUrl: './passengers-list.component.html',
  styleUrls: ['./passengers-list.component.css']
})
export class PassengerListComponent implements OnInit {
  @Input() guestsCount: number = 1;
  @Input() flightId: string = "";
  @Input() return_date: string = "";
  
  passengerForm: FormGroup;
  selectedTab: number = 0;

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private router: Router,
    private bookingService: BookingService // Inject BookingService here
  ) {
    this.passengerForm = this.fb.group({
      passengers: this.fb.array([]) 
    });
  }

  navigateToPaymentSummary(reference_number: string ) {
    this.router.navigate(['/sw/payment/summary', reference_number]);
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.guestsCount = +params['guests'];
      this.flightId = params['flightId'];
      this.generatePassengerForms(this.guestsCount);

      // Get return_date from query parameters
      this.route.queryParams.subscribe(queryParams => {
        this.return_date = queryParams['return_date']; // Make sure to define tripType in the component
      });
      
    });
  }

  generatePassengerForms(count: number): void {
    const passengerArray = this.passengerForm.get('passengers') as FormArray;
    for (let i = 0; i < count; i++) {
      passengerArray.push(this.fb.group({
        first_name: ['', Validators.required],
        last_name: ['', Validators.required],
        dob: ['', Validators.required],
        gender: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        phone: ['', Validators.required]
      }));
    }
  }

  get passengers(): FormArray {
    return this.passengerForm.get('passengers') as FormArray;
  }

  isFormValid(): boolean {
    return this.passengerForm.valid;
  }

  onSubmit(): void {
    if (this.isFormValid()) {
      // Prepare the data to send to the API
      const bookingData = {
        passengers: this.passengerForm.value.passengers,
        owner: this.passengerForm.value.passengers[0],  // Assuming the first passenger is the owner
        departing_flight: { flight_id: this.flightId },  // You may need to provide more flight details
        payment_received: false,  // Adjust this value as per your requirements
        return_date: this.return_date // Adjust this if necessary
      };

      // Call createBooking from the BookingService
      this.bookingService.createBooking(bookingData).subscribe(
        (response) => {
          console.log('Booking created:', response);
          const reference_number = response.reference_number;  // Assuming the response contains the booking ID
          this.passengerForm.reset();
          this.selectedTab = 0;
          this.navigateToPaymentSummary(reference_number);
        },
        (error) => {
          if (error.status === 401) {
            // Redirect to login page on 401 Unauthorized error
            this.router.navigate(['/sw/login']);
          }
           console.error('Error creating booking:', error);
          // Handle error gracefully (e.g., show a message to the user)
        }
      );
    }
  }
}
