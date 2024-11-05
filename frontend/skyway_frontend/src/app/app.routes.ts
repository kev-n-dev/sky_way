import { Routes } from '@angular/router';
import { FlightSearchComponent } from './searchHome/flight-search/flight-search.component';
import { PassengerInfoComponent } from './booking/passenger-info/passenger-info.component';
import { SuccessComponent } from './payment/success/success.component';
import { MyTripsComponent } from './my-trips/my-trips.component';
import { HomePageComponent } from './searchHome/home-page/home-page.component';
import { FlightResultsComponent } from './booking/flight-results/flight-results.component';
import { PassengerListComponent } from './booking/passengers-list/passengers-list.component';
import { SummaryAndPaymentComponent } from './payment/summary-and-payment/summary-and-payment.component';

export const routes: Routes  = [
    { path: 'passenger-info', component: PassengerInfoComponent },
    { path: 'payment/summary/:bookingId', component: SummaryAndPaymentComponent },
    { path: 'flight-search', component: FlightSearchComponent },
    { path: 'my-trips', component: MyTripsComponent },
    { path: 'home', component: HomePageComponent },
    { path: 'explore', component: FlightResultsComponent },
    { path: 'booking/confirmation/:bookingId', component: SuccessComponent },
    { path: 'booking/:flightId/:guests', component: PassengerListComponent },

     { path: '', redirectTo: '/home', pathMatch: 'full' } // Default route
  ];


 

  