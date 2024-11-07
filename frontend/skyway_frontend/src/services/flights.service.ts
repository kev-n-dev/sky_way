import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { log } from 'node:console';

// Flight data interfaces
interface Airport {
  code: string;
  id: string;
  name: string;
}

export interface Flight {
  arrival_airport: Airport;
  arrival_time: string;
  departure_airport: Airport;
  departure_time: string;
  end_date: string;
  flight_num: string;
  id: string;
  start_date: string;
  cost: string;
  duration: string;
}

export interface FlightResponse {
  outgoing_flights: Flight[];
  returning_flights: Flight[];
}

@Injectable({
  providedIn: 'root'
})
export class FlightService {
  private apiUrl = 'http://127.0.0.1:5000/api/search_flights'; // Your API endpoint

  constructor(private http: HttpClient) { }

  // Get flight data with optional query parameters
  getFlights(queryParams?: { [key: string]: string }): Observable<FlightResponse> {
    let params = new HttpParams();
    const token = localStorage.getItem('token');  // Get token from local storage

    // Create headers object with the Authorization token if it exists
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    // Add query parameters if provided
    if (queryParams) {
      for (const key in queryParams) {
         if (queryParams[key] && key != 'return')  {
          params = params.append(key, queryParams[key]);
        }
      }
    }

    // Make the HTTP GET request with headers and query params
    return this.http.get<FlightResponse>(this.apiUrl, { headers, params });
  }
}
