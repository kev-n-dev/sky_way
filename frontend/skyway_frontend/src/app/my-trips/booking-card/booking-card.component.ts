import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

interface Flight {
  id: string;
  departure_city: string;
  destination_city: string;
  take_off_time: string;
  landing_time: string;
  cost: string;
  duration: string;
}

interface Guest {
  id: string;
  name: string;
}

interface Booking {
  id: string;
  guest: Guest;
  flight: Flight;
}

@Component({
  selector: 'app-booking-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './booking-card.component.html',
  styleUrls: ['./booking-card.component.css']
})
export class BookingCardComponent {
  @Input() booking!: Booking;
}
