import { Component } from '@angular/core';
import { RouterOutlet, RouterModule, NavigationEnd, Router } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { filter } from 'rxjs/operators'; // Import filter operator
import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AuthInterceptor } from '../services/authInterceptor.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterModule, HeaderComponent,CommonModule,HttpClientModule],
  templateUrl: './app.component.html',
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }  // Provide the interceptor globally
  ],
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
