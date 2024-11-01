// booking.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookingService {
  constructor(private http: HttpClient) {}

  createBooking(bookingData: any): Observable<any> {
    return this.http.post(`/api/create_booking`, bookingData);
  }

  viewBookings(email: string, reference: string): Observable<any> {
    return this.http.get(`/api/view_bookings?email=${email}&reference_number=${reference}`);
  }
}
