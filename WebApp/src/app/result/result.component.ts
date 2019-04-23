import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  student: string;
  concept: string;
  constructor(public http: HttpClient, public route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
        this.concept = params['concept'];
        this.student = params['student'];
    });
    const postData = {
      student: this.student,
      concept: this.concept
    };
    const options = {
      headers: { 'Content-Type': ['application/json'], 'Accept': ['application/json'] }
    };
    this.http.post('/api/user/performance', postData, options).subscribe(
      suc => {
        console.log(suc);
      },
      err => {
        console.log(err);
      }
    );
  }

  ngOnInit() { }
}
