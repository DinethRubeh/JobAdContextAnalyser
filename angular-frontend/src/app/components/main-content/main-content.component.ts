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

  constructor() { }

  ngOnInit(): void {  }

}
