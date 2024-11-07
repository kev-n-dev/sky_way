import { Component } from '@angular/core';
import { DestinationCardComponent } from '../destination-card/destination-card.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-featured-destinations',
  standalone: true,
  imports: [DestinationCardComponent,CommonModule],
  templateUrl: './featured-destinations.component.html',
  styleUrl: './featured-destinations.component.css'
})
export class FeaturedDestinationsComponent {
  cities = [
    {
      cityName: 'New York',
      description: 'Experience the city that never sleeps',
      price: '299',
      imageUrl: '/assets/ny.jpg',
      searchLink: 'sw/explore?to=JFK',
    },
    {
      cityName: 'Paris',
      description: 'Embrace the city of love and lights',
      price: '399',
      imageUrl: 'assets/paris.avif',
      searchLink: 'sw/explore?to=CDG',

    },
    {
      cityName: 'Tokyo',
      description: 'Discover the blend of tradition and future',
      price: '499',
      imageUrl: 'assets/tokyo.jpg',
      searchLink: 'sw/explore?to=NRT',
    }
    // Add more city objects as needed
  ];
}
