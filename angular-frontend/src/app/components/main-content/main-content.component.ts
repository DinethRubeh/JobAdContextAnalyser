import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { JobDetailsService } from 'src/app/services/job-details.service';
import { JobDetails } from 'src/app/models/JobDetails';

@Component({
  selector: 'app-main-content',
  templateUrl: './main-content.component.html',
  styleUrls: ['./main-content.component.css']
})
export class MainContentComponent implements OnInit {

  @Input() jobDetails:JobDetails[];
  limitedJobDetails:JobDetails[] = [];
  not_expanded:boolean;

  constructor() { }

  ngOnChanges(){
    this.limitedJobDetails= (this.jobDetails) ? this.jobDetails.slice(0,4): this.jobDetails;
    if(this.jobDetails.length > 4)
      this.not_expanded = true;
  }

  ngOnInit(): void { 
    this.not_expanded = false;
  }

  showAll(){
    this.limitedJobDetails = this.jobDetails;
    this.not_expanded = false;
  }

}
