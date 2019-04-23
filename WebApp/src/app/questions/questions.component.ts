import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-questions',
  templateUrl: './questions.component.html',
  styleUrls: ['./questions.component.css']
})
export class QuestionsComponent implements OnInit {
  question: string;
  options = new Array<string>(4);
  answer: string;
  conceptType: string;
  token: string;
  selectedAnswer: any;
  questionId: any;
  constructor(public route: ActivatedRoute, public http: HttpClient, public router: Router) {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'];
      this.conceptType = params['conceptType'];
    });
    const postData = {
      token: this.token,
      concept: this.conceptType
    };
    const options = {
      headers: { 'Content-Type': ['application/json'], 'Accept': ['application/json'] }
    };

    this.http.post('/api/session/get_question', postData, options).subscribe(
      suc => {
        this.answer = suc['answer'];
        this.question = suc['question'];
        this.questionId = suc['_id'];
        for (let i = 0; i < suc['options']['length']; i++) {
          this.options[i] = suc['options'][i];
        }
      },
      err => {
        console.log(err);
      }
    );
  }

  ngOnInit() { }

  checkAnswer() {
    const postData = {
      question_id: this.questionId,
      response: this.selectedAnswer,
      correct: this.answer,
      token: this.token
    };
    const options = {
      headers: { 'Content-Type': ['application/json'], 'Accept': ['application/json'] }
    };
    this.http.post('/api/session/submit', postData, options).subscribe(
      suc => {
        console.log(suc);
      },
      err => {
        console.log(err);
      }
    );
    if (this.selectedAnswer === this.answer) {
      alert('Correct Answer!');
      if (confirm('Do you want another question?')) {
        this.router.navigate(['/student'], { queryParams: { 'token': this.token } });
      } else {
        this.router.navigate(['/student'], { queryParams: { 'token': this.token } });
      }
    } else {
      alert('Wrong Answer');
      if (confirm('Do you want another question?')) {
        this.router.navigate(['/student'], { queryParams: { 'token': this.token } });
      } else {
        this.router.navigate(['/student'], { queryParams: { 'token': this.token } });
      }
    }
  }
}
