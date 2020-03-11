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
    ir: 1,
    touch: true,
    heart: 60,
    buzzer: false,
    buzzText : 'Off',
    frontWarn: false,
    rightWarn: false,
    leftWarn: false,
    irWarn: false
  };

  value: any;
  url = 'http://10.16.26.188:5000/data';
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
    if (this.value.usrfb <= 3 || this.value.usrft <= 3 ) {
      this.data.frontWarn = true;
    } else {
      this.data.frontWarn = false;
    }
    this.data.usrl = this.value.usrl;
    if (this.data.usrl <= 3) {
      this.data.leftWarn = true;
    } else {
      this.data.leftWarn = false;
    }
    this.data.usrr = this.value.usrr;
    if (this.data.usrr <= 3) {
      this.data.rightWarn = true;
    } else {
      this.data.rightWarn = false;
    }
    this.data.touch = this.value.touch;
    this.data.ir = this.value.ir;
    if (this.data.ir > 1) {
      this.data.irWarn = true;
    } else {
      this.data.irWarn = false;
    }
    this.data.heart = this.value.heart;
    if (this.value.usrfb <= 3 || this.value.usrft <= 3 || this.data.usrl <= 3 || this.data.usrr <= 3 || this.value.ir > 1) {
      this.data.buzzText = 'On';
      this.data.buzzer = true;
    } else {
      this.data.buzzText = 'Off';
      this.data.buzzer = false;
    }
  }
}
