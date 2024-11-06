import { Component } from '@angular/core';
import { FlightSearchComponent } from '../flight-search/flight-search.component';

@Component({
  selector: 'app-search-page',
  standalone: true,
  imports: [FlightSearchComponent],
  templateUrl: './search-page.component.html',
  styleUrl: './search-page.component.css'
})
export class SearchPageComponent {

}
