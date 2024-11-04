import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
 
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
  
  passengerForm: FormGroup;
  selectedTab: number = 0;

  constructor(private route: ActivatedRoute, private fb: FormBuilder) {
    this.passengerForm = this.fb.group({
      passengers: this.fb.array([]) 
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.guestsCount = +params['guests'];
      this.flightId = params['flightId'];
      this.generatePassengerForms(this.guestsCount);
    });
  }

  generatePassengerForms(count: number): void {
    const passengerArray = this.passengerForm.get('passengers') as FormArray;
    for (let i = 0; i < count; i++) {
      passengerArray.push(this.fb.group({
        firstName: ['', Validators.required],
        lastName: ['', Validators.required],
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
      console.log('Data Submitted:', { passengers: this.passengerForm.value.passengers, flightId: this.flightId });
    }
  }
}
