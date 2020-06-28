import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { MainResponse } from '../models/MainResponse';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobDetailsService {

  url = "https://job-ad-context-analyser.herokuapp.com/search/?keyWord="

  response:MainResponse;

  constructor(private http:HttpClient) { }

  getJobDetails(keyword:string):Observable<MainResponse>{
    let search_url = `${this.url}${keyword}`
    return this.http.get<MainResponse>(search_url)
  }
}
