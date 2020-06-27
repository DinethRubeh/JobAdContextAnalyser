import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { JobDetailsService } from 'src/app/services/job-details.service';
import { JobDetails } from 'src/app/models/JobDetails';

@Component({
  selector: 'app-main-content',
  templateUrl: './main-content.component.html',
  styleUrls: ['./main-content.component.css']
})
export class MainContentComponent implements OnInit {

  jobDetails: JobDetails[];

  constructor(private jobDetailsService: JobDetailsService) { }

  ngOnInit(): void {
    this.jobDetailsService.getJobDetails().subscribe(data => {
      this.jobDetails = data.object.jobDetails;
    });
  }

}
