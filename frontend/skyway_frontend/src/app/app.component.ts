import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { FlightResultsComponent } from './booking/flight-results/flight-results.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet ,RouterModule, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'SkyWay';
  items = [
    { title: 'search', link: '/flight-search' }
  ];
}
