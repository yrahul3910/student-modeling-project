import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {HttpClientModule} from '@angular/common/http';
@Component({
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent{
	constructor(private http: HttpClient) {
        
    }
	onClickSubmit(data) {	
		const options = {
  			headers: { 'Content-Type': ['application/json'],'Accept': ['application/json'] }
		};
		this.http.post('/api/user/signup',data,options).subscribe(
      		suc => {
            	console.log(suc);
	        },
	        err => {
	            console.log(err);
	        }
    	);
   }
}
