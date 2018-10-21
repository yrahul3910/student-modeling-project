import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'client-app';
}

function myfunc(username,password) {

(async () => {
  const rawResponse = await fetch('/api/user/login', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({a: username, b: password})
  });
  const content = await rawResponse.json();

  console.log(content);
})();
	


}

