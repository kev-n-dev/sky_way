import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

// Define the Destination interface (no decorators)
export interface Destination {
    code: string;
    name: string;
}

// Use the @Injectable() decorator with the service class
@Injectable({
    providedIn: 'root',
})
export class AirportService {
    private apiUrl = 'http://127.0.0.1:5000/api/airports'; // Your API endpoint

    constructor(private http: HttpClient) {}

    // Fetch destinations from the API
    getDestinations(): Observable<Destination[]> {
        return this.http.get<Destination[]>(this.apiUrl);
    }
}
