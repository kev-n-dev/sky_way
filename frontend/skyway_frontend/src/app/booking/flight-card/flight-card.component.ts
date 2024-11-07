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
  @Input() departure_day: string = '';
  @Input() arrival_day: string = '';
  @Input() return_date: string = '';
  
  constructor(private route: ActivatedRoute, private router: Router) {}
  ngOnInit(): void {
    // Split the departure_city and store the first part in the new property
    this.departure_city = this.departure_city.split(',')[0];
    this.destination_city = this.destination_city.split(',')[0];
  }
  
  navigateToPassengerList(guestsCount: string | number) {
    this.router.navigate(['/sw/booking/flight', this.flight_id, guestsCount], {
      queryParams: { return_date: this.return_date }
    });
  }
 
 
}
