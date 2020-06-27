import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MainResponse } from '../models/MainResponse';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobDetailsService {

  url = "http://127.0.0.1:5000/search/?keyWord=php"

  constructor(private http:HttpClient) { }

  getJobDetails():Observable<MainResponse>{
    return this.http.get<MainResponse>(this.url)
  }
}
