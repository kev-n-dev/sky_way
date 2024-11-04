import { CommonModule } from "@angular/common";
import { Router } from '@angular/router';
import { ChangeDetectionStrategy, Component } from "@angular/core";
import { FormsModule } from '@angular/forms'; // Import FormsModule

@Component({
  selector: "app-flight-search",
  templateUrl: "./flight-search.component.html",
  styleUrls: ["./flight-search.component.scss"],
  standalone: true,
  imports: [CommonModule, FormsModule], // Add FormsModule here
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FlightSearchComponent {
  selectedOption: string = 'Roundtrip'; // Default selected option

  constructor(private router: Router) {}

  selectOption(option: string) {
    this.selectedOption = option;
  }

  navigateToSearchRes(form: any) {
    // Get form values
 
    
    const queryParams = {
      type: this.selectedOption ,
      from: form.value.from,
      to: form.value.to,
      guests: form.value.guests,
      depart: form.value.depart,
      return: form.value.return
    };
 

    console.log(queryParams)
    // Navigate to the search page with the constructed search link
    this.router.navigate(['explore'], { queryParams }); // Navigate with query parameters
  }
}
