import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { JobDetailsService } from 'src/app/services/job-details.service';
import { MainResponse } from 'src/app/models/MainResponse';
import { JobDetails } from 'src/app/models/JobDetails';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {

  hits:number;
  keyword:string;
  result:JobDetails[];

  @Output() jobDetails = new EventEmitter();

  constructor(private jobDetailsService:JobDetailsService) { }

  ngOnInit(): void {
    this.jobDetailsService.getJobDetails(this.keyword).subscribe(data => this.hits = data.object.jobDetails.length);
  }

  onSubmit(){
    this.jobDetailsService.getJobDetails(this.keyword).subscribe(data => {
      this.hits = data.object.jobDetails.length;
      this.result = data.object.jobDetails;
      this.jobDetails.emit(this.result);
    });
  }

}
