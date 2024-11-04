import { Component } from '@angular/core';
import { FlightSearchComponent } from '../flight-search/flight-search.component';
import { WhyChooseUsComponent } from '../../why-choose-us/why-choose-us.component';
import { FeaturedDestinationsComponent } from '../featured-destinations/featured-destinations.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [FlightSearchComponent,WhyChooseUsComponent,FeaturedDestinationsComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {
 

}
