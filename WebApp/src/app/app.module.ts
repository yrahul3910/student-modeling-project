import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { TeacherComponent } from './teacher/teacher.component';
import { StudentComponent } from './student/student.component';
import { TestComponent } from './test/test.component';
import { QuestionsComponent } from './questions/questions.component';
import { ResultComponent } from './result/result.component';

const appRoutes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'teacher', component: TeacherComponent},
  { path: 'student', component: StudentComponent},
  { path: 'test', component: TestComponent},
  { path: 'question', component: QuestionsComponent},
  { path: 'result', component: ResultComponent}
];
@NgModule({
  declarations: [
    AppComponent,
    SignupComponent,
    LoginComponent,
    TeacherComponent,
    StudentComponent,
    TestComponent,
    QuestionsComponent,
    ResultComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes, { enableTracing: true}),
    FormsModule
  ],
  exports: [
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
