import { Component, OnInit, Input } from '@angular/core';
import { JobDetailsService } from 'src/app/services/job-details.service';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {

  hits:number;

  constructor(private jobDetailsService:JobDetailsService) { }

  ngOnInit(): void {
    this.jobDetailsService.getJobDetails().subscribe(data => this.hits = data.object.jobDetails.length)
  }

}
