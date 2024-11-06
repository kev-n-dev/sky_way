import { Component } from '@angular/core';
import { BookingCardComponent } from '../booking-card/booking-card.component';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';



// Define an interface for the flight
interface Flight {
  id: string;
  departure_city: string;
  destination_city: string;
  take_off_time: string;
  landing_time: string;
  cost: string; // Keeping as string to retain currency formatting
  duration: string; // Keeping as string for duration format
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
  selector: 'app-booking-list',
  standalone: true,
  imports: [BookingCardComponent,CommonModule],
  templateUrl: './booking-list.component.html',
  styleUrl: './booking-list.component.css'
})
export class BookingListComponent {
  constructor(private route: ActivatedRoute, private router: Router) {}


   bookings: Booking[] = [
    {
      id: 'bkg001',
      guest: {
        id: 'guest001',
        name: 'Alice Johnson'
      },
      flight: {
        id: 'flt001',
        departure_city: 'New York',
        destination_city: 'London',
        take_off_time: '2023-06-15T14:30:00',
        landing_time: '2023-06-15T22:30:00',
        cost: '$850.00',
        duration: '8h 00m'
      }
    },
    {
      id: 'bkg002',
      guest: {
        id: 'guest002',
        name: 'Bob Smith'
      },
      flight: {
        id: 'flt002',
        departure_city: 'San Francisco',
        destination_city: 'Tokyo',
        take_off_time: '2023-07-20T10:00:00',
        landing_time: '2023-07-21T13:00:00',
        cost: '$1,200.00',
        duration: '11h 00m'
      }
    },
    {
      id: 'bkg003',
      guest: {
        id: 'guest003',
        name: 'Carol Williams'
      },
      flight: {
        id: 'flt003',
        departure_city: 'Paris',
        destination_city: 'Dubai',
        take_off_time: '2023-05-05T22:15:00',
        landing_time: '2023-05-06T06:15:00',
        cost: '€650.00',
        duration: '8h 00m'
      }
    },
    {
      id: 'bkg004',
      guest: {
        id: 'guest004',
        name: 'David Brown'
      },
      flight: {
        id: 'flt004',
        departure_city: 'Sydney',
        destination_city: 'Los Angeles',
        take_off_time: '2023-08-10T15:30:00',
        landing_time: '2023-08-10T10:30:00',
        cost: 'A$1,500.00',
        duration: '13h 00m'
      }
    },
    {
      id: 'bkg005',
      guest: {
        id: 'guest005',
        name: 'Emily Davis'
      },
      flight: {
        id: 'flt005',
        departure_city: 'Berlin',
        destination_city: 'Rome',
        take_off_time: '2023-09-14T08:00:00',
        landing_time: '2023-09-14T09:45:00',
        cost: '€120.00',
        duration: '1h 45m'
      }
    }
  ];
    navigateToHome() {
    this.router.navigate(['sw/home']); // Navigate with query parameters
  }
}
