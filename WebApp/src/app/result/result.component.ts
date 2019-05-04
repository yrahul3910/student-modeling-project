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

  hidden_states = ["unlearned", "learned"];
  emission_states = [["Concept unlearned, wrong answer", "Guess"], ["Slip", "Knows concept, correct answer"]]

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
        if (suc['success']){
          this.start_probs = suc['start_probs'];
          this.transition_probs = suc['transition_probs'];
          this.emission_probs = suc['emission_probs'];
        }
      },
      err => {
        console.log(err);
      }
    );
  }

  ngOnInit() { }
}
