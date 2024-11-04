import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-passenger-info',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './passenger-info.component.html',
  styleUrls: ['./passenger-info.component.css']
})
export class PassengerInfoComponent {
  @Input() formGroup!: FormGroup; // Receive the formGroup input
  @Input() flightId: string = ""; // Flight ID for reference in the template
}
