import { Component } from '@angular/core';
import { MainResponse } from './models/MainResponse';
import { JobDetails } from './models/JobDetails';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'angular-frontend';

  jobDetails:JobDetails[]

  displaySearchResults(jobDetails:JobDetails[]){
    this.jobDetails = jobDetails;
  }

}
