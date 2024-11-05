import { Component, Input, input } from '@angular/core';
import { DatePipe } from '@angular/common'; // Import DatePipe
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-flight-card',
  standalone: true,
  imports: [DatePipe], // Provide DatePipe in the imports array
  templateUrl: './flight-card.component.html',
  styleUrls: ['./flight-card.component.css']
})
export class FlightCardComponent {
  @Input() flight_id: string = '';
  @Input() departure_city: string = '';
  @Input() destination_city: string = '';
  @Input() take_off_time: string = '';
  @Input() cost: number | string = '';
  @Input() duration: string = '';
  @Input() landing_time: string = '';
  @Input() guests: number | string = "";
  constructor(private route: ActivatedRoute, private router: Router) {}

  navigateToPassengerList(guestsCount: string | number) {
    this.router.navigate(['/booking',this.flight_id, guestsCount]);
  }
 
  // Method to format take-off time
  getFormattedTakeOffTime(time:string): string {
    const datePipe = new DatePipe('en-US'); // Create an instance of DatePipe

    return datePipe.transform(time, 'h:mm a') || ''; // Format as '8:00 PM'
  }
}
