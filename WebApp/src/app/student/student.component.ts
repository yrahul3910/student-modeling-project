import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-student',
  templateUrl: './student.component.html',
  styleUrls: ['./student.component.css']
})
export class StudentComponent implements OnInit {
  token: string;
  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {
    console.clear();
    this.route.queryParams.subscribe(params => {
        this.token = params['token'];
    });
   console.log(this.token);
  }
  ngOnInit() { }
  onClickSubmit(data) {
     this.router.navigate(['/question'], { queryParams: {'token': this.token, 'conceptType': data['conceptType']}});
  }
}
