import { Injectable } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class SensorsService {
  data = { usrfb: 200,
    usrft: 200,
    usrl: 200,
    usrr: 200,
    touch: true,
    heart: 60,
    buzzer: false,
    buzzText : 'Off',
    frontWarn: false,
    rightWarn: false,
    leftWarn: false,
    ir: 2
  };
  constructor() { }

  setData(data) {
    this.data.usrfb = data.entries.entry[0].USRFB;
    this.data.usrft = data.entries.entry[1].USRFT;
    this.data.usrl = data.entries.entry[2].USRL;
    this.data.usrr = data.entries.entry[3].USRR;
    this.data.ir = data.entries.entry[4].IR;
    this.data.touch = data.entries.entry[5].touch;
    this.data.heart = data.entries.entry[6].heart;
  }

  getData() {
    return this.data;
  }
}
