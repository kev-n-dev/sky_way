import { Component } from '@angular/core';
import { RouterOutlet, RouterModule, NavigationEnd, Router } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { filter } from 'rxjs/operators'; // Import filter operator
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterModule, HeaderComponent,CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], // Change styleUrl to styleUrls
})
export class AppComponent {
  showHeader: boolean = true;
  title = 'SkyWay';

  constructor(private router: Router) {
    // Listen to route changes and update showHeader accordingly
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(event => {
        // Check if the current route is 'login' to hide the header
        this.showHeader = this.router.url !== '/sw/login';
      });
  }
}
