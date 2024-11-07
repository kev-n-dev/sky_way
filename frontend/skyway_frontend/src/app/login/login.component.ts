import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  registerForm: FormGroup;
  isLoginMode = true;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });

    this.registerForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmitLogin() {
    if (this.loginForm.valid) {
      const loginData = this.loginForm.value;
      console.log('Login Data:', loginData);
      this.authService.login(loginData.email, loginData.password).subscribe(
        (response) => {
          console.log('Login Successful', response);
  
          // Get the token directly from the response body
          const token = response.body?.access_token;  // Assuming the token is in the `access_token` field of the response body
          
          if (token) {
            localStorage.setItem('token', token);  // Store the token in local storage
            localStorage.setItem('Bearer', 'Bearer '+token);  // Store the bearer in local storage
            this.router.navigate(['/sw/home']);  // Navigate to the home page
          } else {
            console.error('Token not found in response body', response);
          }
        },
        (error) => {
          console.error('Login failed', error);
          // Optionally display an error message to the user
        }
      );
    }
  }
  
  onSubmitRegister() {
    if (this.registerForm.valid) {
      const registerData = this.registerForm.value;
      console.log('Register Data:', registerData);
      this.authService.register(registerData.name, registerData.email, registerData.password).subscribe(
        (response) => {
          console.log('Registration Successful', response);
          this.switchMode()
        },
        (error) => {
          console.error('Registration failed', error);
          // Optionally display an error message to the user
        }
      );
    }
  }

  switchMode() {
    this.isLoginMode = !this.isLoginMode;
  }
}
