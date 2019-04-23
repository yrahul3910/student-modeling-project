import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-teacher',
  templateUrl: './teacher.component.html',
  styleUrls: ['./teacher.component.css']
})
export class TeacherComponent implements OnInit {

  token: string;
  constructor(private http: HttpClient, private route: ActivatedRoute, public router: Router) {
    console.clear();
    this.route.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }
  ngOnInit() { }
  onClickSubmit(data) {
    this.router.navigate(['/result'], { queryParams: {'student': data['student'], 'concept': data['concept']}});
  }
}
