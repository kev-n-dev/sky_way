import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FlightCardComponent } from '../flight-card/flight-card.component';
import { CommonModule } from '@angular/common';
import { FlightService, FlightResponse, Flight } from '../../../services/flights.service'; // Import Flight from service

@Component({
  selector: 'app-flight-results',
  standalone: true,
  imports: [FlightCardComponent, CommonModule],
  templateUrl: './flight-results.component.html',
  styleUrls: ['./flight-results.component.css']
})
export class FlightResultsComponent implements OnInit {

  flights: FlightResponse | null = null; 
  filteredFlights: Flight[] = []; // Now filteredFlights uses the same Flight type from the service
  to: string | null | undefined = null;
  from: string | null | undefined = null;
  departure_date: string | null | undefined = null;
  return_date: string = "";
  guests: number = 1;

  searched: { to: string | null | undefined; from: string | null | undefined; departure_date: string | null | undefined; guests: string | number } = {
    to: "Anywhere",
    from: "Anywhere",
    departure_date: "Any time",
    guests: 1,
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private flightService: FlightService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.to = params['to'] || null;
      this.from = params['from'] || null;
      this.departure_date = params['depart'] || null;
      this.guests = params['guests'] || 1;
      this.return_date = params['return'] || "";
      this.flightService.getFlights(params).subscribe(
        (data: FlightResponse) => {
          this.flights = data;
          console.log(data); 
          this.updateSearchedValues();
          this.filterFlights();
        },
        (error) => {
            if (error.status === 401) {
              // Redirect to login page on 401 Unauthorized error
              this.router.navigate(['/sw/login']);
            }
          console.error('Error fetching flight data:', error);

        }
      );
    });
  }

  updateSearchedValues(): void {
    const setIfValid = (value: string | null | undefined, target: any) => {
      if (value && value.trim() !== '') {
        return value;
      }
      return target;
    };

    this.searched.departure_date = setIfValid(this.departure_date, this.searched.departure_date);
    this.searched.to = setIfValid(this.to, this.searched.to);
    this.searched.from = setIfValid(this.from, this.searched.from);
    this.searched.guests = setIfValid(String(this.guests), String(this.searched.guests));
  }

  filterBy(criteria: string): void {
    if (!this.flights) return;

    switch (criteria) {
      case 'cheapest':
        this.filteredFlights = [...this.flights.outgoing_flights].sort((a, b) =>
          parseFloat(a.cost.replace('$', '')) - parseFloat(b.cost.replace('$', ''))
        );
        break;
      case 'fastest':
        this.filteredFlights = [...this.flights.outgoing_flights].sort((a, b) =>
          this.parseDuration(a.duration) - this.parseDuration(b.duration)
        );
        break;
      case 'bestValue':
        this.filteredFlights = [...this.flights.outgoing_flights].sort((a, b) => {
          const valueA = parseFloat(a.cost.replace('$', '')) / this.parseDuration(a.duration);
          const valueB = parseFloat(b.cost.replace('$', '')) / this.parseDuration(b.duration);
          return valueA - valueB;
        });
        break;
      default:
        this.filteredFlights = [...this.flights.outgoing_flights];
        break;
    }
  }

  parseDuration(duration: any): any {
    try {
      // Ensure duration is treated as a string
      const durationStr = duration.toString();
  
      return durationStr
      // Your other logic here...
    } catch (error) {
      console.error('Error parsing duration:', error);
      return null;
    }
  }
  

  filterFlights(): void {
    if (!this.flights) return;

    this.filteredFlights = this.flights.outgoing_flights;

    if (this.to) {
      this.filteredFlights = this.filteredFlights.filter(flight =>
        flight.arrival_airport.name.toLowerCase().includes(this.to!.toLowerCase())
      );
    }

    if (this.from) {
      this.filteredFlights = this.filteredFlights.filter(flight =>
        flight.departure_airport.name.toLowerCase().includes(this.from!.toLowerCase())
      );
    }

    console.log(this.filteredFlights);
  }

  navigateToHome(): void {
    this.router.navigate(['sw/home']);
  }
}
