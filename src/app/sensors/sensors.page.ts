import { Component } from '@angular/core';

@Component({
  selector: 'app-sensors',
  templateUrl: 'sensors.page.html',
  styleUrls: ['sensors.page.scss']
})
export class SensorsPage {
  data = { distance1: 200,
    distance2: 200,
    distance3: 200,
    drct: 'North',
    motion: true,
    buzzer: false,
    buzzText : 'Off',
    dist1Warn: false,
    dist2Warn: false,
    dist3Warn: false
  };

  constructor() {}

}
