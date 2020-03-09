import { SensorsService } from './../services/sensors.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';


@Component({
  selector: 'app-sensors',
  templateUrl: 'sensors.page.html',
  styleUrls: ['sensors.page.scss']
})
export class SensorsPage {
  data = { usrf: 200,
    usrl: 200,
    usrr: 200,
    touch: true,
    heart: 60,
    buzzer: false,
    buzzText : 'Off',
    frontWarn: false,
    rightWarn: false,
    leftWarn: false
  };

  value: any;
  url = 'http://pitunnel2.com:42877/data';
  server: Observable<any>;


  constructor(private http: HttpClient, private sensors: SensorsService) {}

  // tslint:disable-next-line: use-lifecycle-interface
  ngOnInit() {
    // tslint:disable-next-line: no-console
    this.http.get(this.url).subscribe(data => {
      this.sensors.setData(data);
      this.value = this.sensors.getData();
      this.updateData();
    });

    this.server = this.http.get(this.url);
    setInterval(() => {
      this.getData(); // Now the "this" still references the component
      this.updateData();
    }, 1000);
  }

  getData() {
    this.http.get(this.url).subscribe(data => {
      this.sensors.setData(data);
      this.value = this.sensors.getData();
      this.updateData();
    });

    this.server = this.http.get(this.url);
  }

  updateData() {
    this.data.usrf = (this.value.usrfb + this.value.usrft) / 2;
    this.data.usrl = this.value.usrl;
    this.data.usrr = this.value.usrr;
    this.data.touch = this.value.touch;
    this.data.heart = this.value.heart;
  }
}
