import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PassengerListComponent } from './passengers-list.component';


describe('PassengersListComponent', () => {
  let component: PassengerListComponent;
  let fixture: ComponentFixture<PassengerListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PassengerListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PassengerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
