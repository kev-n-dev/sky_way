import { Routes } from '@angular/router';
import { FlightSearchComponent } from './searchHome/flight-search/flight-search.component';
import { PassengerInfoComponent } from './booking/passenger-info/passenger-info.component';
import { SuccessComponent } from './payment/success/success.component';
import { MyTripsComponent } from './my-trips/my-trips.component';
import { HomePageComponent } from './searchHome/home-page/home-page.component';
import { FlightResultsComponent } from './booking/flight-results/flight-results.component';
import { PassengerListComponent } from './booking/passengers-list/passengers-list.component';
import { SummaryAndPaymentComponent } from './payment/summary-and-payment/summary-and-payment.component';
import { SearchPageComponent } from './searchHome/search-page/search-page.component';
import { LoginComponent } from './login/login.component';

export const routes: Routes  = [
    { path: 'sw/login', component: LoginComponent }, // Add the login route here
    { path: 'sw/home', component: HomePageComponent },
    { path: 'sw/passenger-info', component: PassengerInfoComponent },
    { path: 'sw/payment/summary/:bookingId', component: SummaryAndPaymentComponent },
    { path: 'sw/flight-search', component: SearchPageComponent },
    { path: 'sw/my-trips', component: MyTripsComponent },
    { path: 'sw/explore', component: FlightResultsComponent },
    { path: 'sw/booking/confirmation/:bookingId', component: SuccessComponent },
    { path: 'sw/booking/:flightId/:guests', component: PassengerListComponent },
     { path: '', redirectTo: 'sw/login', pathMatch: 'full' } // Default route
  ];


 

  