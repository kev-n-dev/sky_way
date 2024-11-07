import { Component, Input  } from '@angular/core';

@Component({
  selector: 'app-flight-details',
  standalone: true,
  imports: [],
  templateUrl: './flight-details.component.html',
  styleUrl: './flight-details.component.css'
})
export class FlightDetailsComponent {
  @Input() from: string = ''; // Default value if not provided
  @Input() to: string = ''; // Default value if not provided
  @Input() date: string = ''; // Default value if not provided
  @Input() passengers: number = 1; // Default value if not provided
   

}
