import { CommonModule } from '@angular/common';
import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-price-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './price-summary.component.html',
  styleUrls: ['./price-summary.component.css']
})
export class PriceSummaryComponent implements OnInit, OnChanges {
  @Input() baseFee: string; 
  @Input() ReturnBaseFee: string; 
  @Input() taxes: string; 

  baseFeeNumber: number;
  returnBaseFeeNumber: number;
  taxAmount: number;
  sub_total: number;
  new_total: number;

  ngOnInit(): void {
    // This will only be called once when the component is initialized
    console.log('ngOnInit called');
  }

  ngOnChanges(changes: SimpleChanges): void {
    // This is called whenever input values change or are initialized
    if (changes['baseFee'] || changes['ReturnBaseFee'] || changes['taxes']) {
      this.calculateValues();
    }
  }

  private calculateValues(): void {
    // Handle currency strings, remove dollar sign and commas
    this.baseFeeNumber = this.parseCurrency(this.baseFee);
    this.returnBaseFeeNumber = this.parseCurrency(this.ReturnBaseFee);

    console.log('Base Fee:', this.baseFeeNumber);
    console.log('Return Base Fee:', this.returnBaseFeeNumber);
    console.log('Taxes:', this.taxes);

    // Extract the percentage value from the taxes string (e.g., "10%" => 10)
    const taxPercentage = parseFloat(this.taxes.replace('%', ''));

    // Calculate the sub_total (sum of baseFee and returnBaseFee)
    this.sub_total = this.baseFeeNumber + this.returnBaseFeeNumber;

    // Calculate the tax amount
    this.taxAmount = this.sub_total * (taxPercentage / 100);

    // Calculate the new total (base fees + tax)
    this.new_total = this.sub_total + this.taxAmount;
  }

  private parseCurrency(value: string): number {
    if (!value) {
      return 0; // Return 0 if value is undefined or empty
    }

    let sanitizedValue = '';
    
    // Iterate through each character and append only valid characters (digits, decimal, and minus)
    for (let i = 0; i < value.length; i++) {
      const char = value[i];
      if ((char >= '0' && char <= '9') || char === '.' || char === '-') {
        sanitizedValue += char;
      }
    }

    console.log("sanitizedValue", sanitizedValue);

    // Parse the sanitized value as a float
    const parsedValue = parseFloat(sanitizedValue);

    // If the parsed value is NaN, return 0 as a fallback
    return isNaN(parsedValue) ? 0 : parsedValue;
  }
}
