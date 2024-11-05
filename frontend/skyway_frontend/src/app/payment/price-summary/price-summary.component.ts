import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-price-summary',
  standalone: true,
  imports: [],
  templateUrl: './price-summary.component.html',
  styleUrl: './price-summary.component.css'
})
export class PriceSummaryComponent {
  @Input() baseFee: number = 0; // Default value if not provided
  @Input() taxes: number = 0; // Default value if not provided

  get total(): number {
    return this.baseFee + this.taxes; // Calculate total
  }
}
