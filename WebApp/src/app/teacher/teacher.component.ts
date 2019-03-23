import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-teacher',
  templateUrl: './teacher.component.html',
  styleUrls: ['./teacher.component.css']
})
export class TeacherComponent implements OnInit {

  token:string;
  constructor(private http:HttpClient,private route: ActivatedRoute) { }
  ngOnInit() {
    console.clear();
    this.route.queryParams.subscribe(params =>{
      this.token = params['token'];
    });
    const options = {
      headers: { 'Content-Type': ['application/json'],'Accept': ['application/json'] }
    };
    let data = {
      'token':this.token
    
    }
    console.log(data);
    this.http.post('/api/user/details',data,options).subscribe(
      suc => {
        console.log(suc);
      },
      err => {
          console.log(err);
      }
    );
  }

}
