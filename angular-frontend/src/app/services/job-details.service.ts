import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MainResponse } from '../models/MainResponse';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobDetailsService {

  url = "http://127.0.0.1:5000/search/?keyWord="

  constructor(private http:HttpClient) { }

  getJobDetails(keyword:string):Observable<MainResponse>{
    let search_url = `${this.url}${keyword}`
    return this.http.get<MainResponse>(search_url)
  }
}
