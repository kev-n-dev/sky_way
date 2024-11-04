import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-destination-card',
  standalone: true,
  templateUrl: './destination-card.component.html',
  styleUrl: './destination-card.component.css'
})
export class DestinationCardComponent {
  @Input() cityName: string = '';
  @Input() description: string = '';
  @Input() price: number | string = '';
  @Input() imageUrl: string = '';
  @Input() searchLink: string = '';

  constructor(private router: Router) {}

  navigateToSearch(searchLink: string) {
    const link = this.searchLink.split('?'); // Split the link into path and query string
    const route = link[0]; // The path (e.g., 'search')
    const queryParams = link[1] ? { to: link[1].split('=')[1] } : {}; // Extract query params if they exist

    this.router.navigate([route], { queryParams }); // Navigate with query parameters
  }
}
