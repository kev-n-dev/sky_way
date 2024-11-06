import { Component } from '@angular/core';
import { BookingListComponent } from "./booking-list/booking-list.component";

@Component({
  selector: 'app-my-trips',
  standalone: true,
  imports: [BookingListComponent],
  templateUrl: './my-trips.component.html',
  styleUrl: './my-trips.component.css'
})
export class MyTripsComponent {

}
