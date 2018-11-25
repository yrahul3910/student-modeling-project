import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {HttpClientModule} from '@angular/common/http';

@Component({
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent{
	constructor(private http: HttpClient) {}
	onClickSubmit(data) {

		var x = '{"username":"'+data.username+'","password":"'+data.password+'"}';
		var obj = JSON.parse(x);
		var options = {
  			headers: { 'Content-Type': ['application/json'], 
  					   'Accept': ['application/json'] }
		};
		this.http.post('/api/user/login', obj,options).subscribe(
      		suc => {
            	console.log(suc);
	        },
	        err => {
	            console.log(err);
	        }
    	);
   }
}
