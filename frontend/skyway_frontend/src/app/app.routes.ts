import { Routes } from '@angular/router';
import { FlightSearchComponent } from './searchHome/flight-search/flight-search.component';
import { PassengerInfoComponent } from './passenger-info/passenger-info.component';
import { SummaryComponent } from './summary/summary.component';
import { SuccessComponent } from './success/success.component';
import { MyTripsComponent } from './my-trips/my-trips.component';
import { HomePageComponent } from './searchHome/home-page/home-page.component';
import { FlightResultsComponent } from './flight-results/flight-results.component';
import { PassengerListComponent } from './passengers-list/passengers-list.component';

export const routes: Routes  = [
    { path: 'passenger-info', component: PassengerInfoComponent },
    { path: 'payment/summary/:bookingId', component: SummaryComponent },
    { path: 'success', component: SuccessComponent },
    { path: 'flight-search', component: FlightSearchComponent },
    { path: 'my-trips', component: MyTripsComponent },
    { path: 'home', component: HomePageComponent },
    { path: 'explore', component: FlightResultsComponent },
    { path: 'booking/:flightId/:guests', component: PassengerListComponent },

     { path: '', redirectTo: '/home', pathMatch: 'full' } // Default route
  ];


 

  