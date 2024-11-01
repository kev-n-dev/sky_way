// flight-search.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FlightSearchService {
  constructor(private http: HttpClient) {}

  searchFlights(departure: string, arrival: string, date: string): Observable<any> {
    return this.http.get(`/api/search_flights?departure_city=${departure}&arrival_city=${arrival}&date=${date}`);
  }
}