import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FlightCardComponent } from '../flight-card/flight-card.component';
import { CommonModule } from '@angular/common';
import { v4 as uuid4 } from 'uuid';

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

interface Search {
  to: string | null | undefined;
  from: string | null | undefined;
  departure_date: string | null | undefined;
  guests: string | number;
}

@Component({
  selector: 'app-flight-results',
  standalone: true,
  imports: [FlightCardComponent, CommonModule],
  templateUrl: './flight-results.component.html',
  styleUrls: ['./flight-results.component.css']
})
export class FlightResultsComponent implements OnInit {
  flights: Flight[] = [ // Specify the type for flights
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "New York, NY",
      take_off_time: "2024-11-01T09:00:00",
      landing_time: "2024-11-01T10:30:00",
      cost: "$150",
      duration: "1h 30m"
    },
    {
      id: uuid4(),
      departure_city: "Washington, DC",
      destination_city: "Los Angeles, CA",
      take_off_time: "2024-11-02T14:00:00",
      landing_time: "2024-11-02T17:00:00",
      cost: "$300",
      duration: "6h"
    },
    {
      id: uuid4(),
      departure_city: "Washington, DC",
      destination_city: "Chicago, IL",
      take_off_time: "2024-11-03T11:00:00",
      landing_time: "2024-11-03T12:30:00",
      cost: "$200",
      duration: "1h 30m"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Miami, FL",
      take_off_time: "2024-11-04T08:00:00",
      landing_time: "2024-11-04T10:00:00",
      cost: "$180",
      duration: "2h"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "San Francisco, CA",
      take_off_time: "2024-11-05T13:00:00",
      landing_time: "2024-11-05T16:30:00",
      cost: "$350",
      duration: "6h 30m"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Boston, MA",
      take_off_time: "2024-11-06T07:00:00",
      landing_time: "2024-11-06T08:30:00",
      cost: "$140",
      duration: "1h 30m"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Seattle, WA",
      take_off_time: "2024-11-07T10:00:00",
      landing_time: "2024-11-07T13:00:00",
      cost: "$400",
      duration: "5h"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Tokyo, Jp",
      take_off_time: "2024-11-08T12:00:00",
      landing_time: "2024-11-08T13:30:00",
      cost: "$160",
      duration: "1h 30m"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Las Vegas, NV",
      take_off_time: "2024-11-09T15:00:00",
      landing_time: "2024-11-09T17:30:00",
      cost: "$370",
      duration: "5h 30m"
    },
    {
      id: uuid4(),

      departure_city: "Washington, DC",
      destination_city: "Paris, Fr",
      take_off_time: "2024-11-10T11:00:00",
      landing_time: "2024-11-10T13:30:00",
      cost: "$220",
      duration: "2h 30m"
    }
  ];


  filteredFlights: Flight[] = []; // Specify the type for filteredFlights
  to: string | null | undefined = null;
  from: string | null | undefined = null;
  departure_date: string | null | undefined = null;
  guests: number = 1;

  searched: Search = {
    to: "Anywhere",
    from: "Anywhere",
    departure_date: "Any time",
    guests: 1,
  };

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    // Subscribe to the query parameters
    this.route.queryParams.subscribe(params => {
      this.to = params['to'] || null; // Get the city from the query string
      this.from = params['from'] || null; // Get the city from the query string
      this.departure_date = params['depart'] || null; // Get the date from the query string
      this.guests = params['guests'] || 1; // Get the number of guests from the query string

      this.updateSearchedValues();
      this.filterFlights(); // Call the filter function
    });
  }

  updateSearchedValues() {
    const setIfValid = (value: string | null | undefined, target: any) => {
      if (value && value.trim() !== '') { // Check for empty strings
        return value; // Return new value if valid
      }
      return target; // Keep the existing value otherwise
    };

    this.searched.departure_date = setIfValid(this.departure_date, this.searched.departure_date);
    this.searched.to = setIfValid(this.to, this.searched.to);
    this.searched.from = setIfValid(this.from, this.searched.from);
    this.searched.guests = setIfValid(String(this.guests), String(this.searched.guests)); // Convert to string
  }

  filterBy(criteria: string): void {
    switch (criteria) {
      case 'cheapest':
        this.filteredFlights = [...this.flights].sort((a, b) =>
          parseFloat(a.cost.replace('$', '')) - parseFloat(b.cost.replace('$', '')))
        break;
      case 'fastest':
        this.filteredFlights = [...this.flights].sort((a, b) =>
          this.parseDuration(a.duration) - this.parseDuration(b.duration));
        break;
      case 'bestValue':
        this.filteredFlights = [...this.flights].sort((a, b) => {
          const valueA = parseFloat(a.cost.replace('$', '')) / this.parseDuration(a.duration);
          const valueB = parseFloat(b.cost.replace('$', '')) / this.parseDuration(b.duration);
          return valueA - valueB;
        });
        break;
      default:
        this.filteredFlights = [...this.flights];
        break;
    }
  }

  // Function to parse duration from "Xh Ym" to total minutes
  parseDuration(duration: string): number {
    const parts = duration.split('h').map(part => part.trim());
    const hours = parseInt(parts[0], 10) || 0;
    const minutes = parseInt(parts[1], 10) || 0;
    return hours * 60 + minutes;
  }

  // Function to filter flights based on the city
  filterFlights() {
    this.filteredFlights = this.flights; // Start with all flights

    if (this.to) {
      this.filteredFlights = this.filteredFlights.filter(flight =>
        flight.destination_city.toLowerCase().includes(this.to!.toLowerCase())
      );
    }

    if (this.from) {
      this.filteredFlights = this.filteredFlights.filter(flight =>
        flight.departure_city.toLowerCase().includes(this.from!.toLowerCase())
      );
    }
    console.log( this.filteredFlights)
  }
 

  navigateToHome() {
    this.router.navigate(['sw/home']); // Navigate with query parameters
  }
}
