import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent {
    token: string;
    constructor(private http: HttpClient, private router: Router) { }
    onClickSubmit(data) {
        console.clear();
        const options = {
            headers: { 'Content-Type': ['application/json'], 'Accept': ['application/json'] }
        };
        this.http.post('/api/user/login', data, options).subscribe(
            suc => {
                if (data['userType'] === 'Student') {
                    this.token = suc['token'];
                    this.router.navigate(['/student'], { queryParams: {'token': this.token}});
                } else if (data['userType'] === 'Teacher') {
                    this.token = suc['token'];
                    this.router.navigate(['/teacher'], { queryParams: {'token': this.token}});
                } else {
                    console.log('Invalid User Type');
                }
            },
            err => {
                console.log(err);
            }
        );
    }
}
