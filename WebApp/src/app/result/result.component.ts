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
  start_probs = new Array<string>(2);
  transition_probs = new Array<string>(2);
  emission_probs = new Array<string>(2);
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
        if (suc['success']==='true'){
          for (let i = 0; i < suc['start_probs']['length']; i++) {
            this.start_probs[i] = suc['start_probs'][i];
          }
          for (let i = 0; i < suc['transition_probs']['length']; i++) {
            this.transition_probs[i] = suc['transition_probs'][i];
          }
          for (let i = 0; i < suc['emission_probs']['length']; i++) {
            this.emission_probs[i] = suc['emission_probs'][i];
          }
        }
      },
      err => {
        console.log(err);
      }
    );
  }

  ngOnInit() { }
}
