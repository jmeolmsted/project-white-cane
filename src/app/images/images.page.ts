import { SensorsService } from './../services/sensors.service';
import { IpAddressService } from './../services/ip-address.service';
import { IpService } from './../services/ip.service';
import { ImagesService } from './../services/images.service';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';




@Component({
  selector: 'app-images',
  templateUrl: 'images.page.html',
  styleUrls: ['images.page.scss']
})
export class ImagesPage {
  title = 'app';

  fileData: JSON;
  data = {
    usfText: '',
    irText: '',
    ir: 1,
    usf: 20,
    usfCamera: false,
    irCamera: false,
    camera: false,
    image: './assets/images/favicon.png'
  };

  value: any;
  server: Observable<any>;

  selected = '';

  showImage = false;
  ipAddress: string;
  endpoint: string;
  fileURL = 'http://10.16.26.188:5000/files';
  dataURL = 'http://10.16.26.188:5000/data';
  results = {};
  check: any;

  constructor(private http: HttpClient, private imageService: ImagesService, private ipService: IpService, private ip: IpAddressService,
              private sensor: SensorsService) {
  }

  // tslint:disable-next-line: use-lifecycle-interface
  ngOnInit() {
    // tslint:disable-next-line: no-console
    this.ipAddress = window.location.hostname;
    this.getStatus();
    this.http.get(this.fileURL).subscribe(files => {
      this.fileData = files as JSON;
    });
    this.server = this.http.get(this.fileURL);
    console.log(this.server);

    setInterval(() => {
      this.getStatus(); // Now the "this" still references the component
    }, 250);

  }

  getIP() {
    this.ip.getIPAddress().subscribe((res: any) => {
      this.ipAddress = res.ip;
    });
  }

  getStatus() {
    this.http.get(this.dataURL).subscribe(data => {
      this.sensor.setData(data);
      this.value = this.sensor.getData();
      if ( this.value.usrft <= 4 && this.value.usrfb <= 2) {
        this.data.usf = (this.value.ursft + this.value.usrfb) / 2;
        this.data.usfCamera = true;
        this.data.usfText = 'Obstacle Detected By Top and Bottom USR!';
      } else if ( this.value.usrft <= 4 && this.value.usrfb > 2) {
        this.data.usf = this.value.usrft;
        this.data.usfCamera = true;
        this.data.usfText = 'Obstacle Detected By Top USR!';
      } else if ( this.value.usrft > 4 && this.value.usrfb <= 2) {
        this.data.usf = this.value.usrfb;
        this.data.usfCamera = true;
        this.data.usfText = 'Obstacle Detected By Bottom USR!';
      } else {
        this.data.usfCamera = false;
        this.data.usfText = 'No Obstacle Detected.';
      }
      if (this.value.ir > 2) {
        this.data.ir = this.value.ir;
        this.data.irCamera = true;
        this.data.irText = 'Stair or Slope Detected by IR Sensor!';
      } else {
        this.data.irCamera = false;
        this.data.irText = 'No Stair or Slope Detected.';
      }
      this.data.camera = this.data.irCamera || this.data.usfCamera;
    });
    if (this.data.camera) {
      this.http.get(this.fileURL).subscribe(files => {
        this.fileData = files as JSON;
        // tslint:disable-next-line: no-string-literal
        this.openImage(this.fileData['files'][this.fileData['files'].length - 1].name);
      });
      this.server = this.http.get(this.fileURL);
    }
  }

  openImage(file) {
    this.imageService.setImage(file);
    if (file === this.selected) {
      this.showImage = false;
      this.selected = '';
    } else {
      this.showImage = true;
      this.selected = file;
    }
    this.data.image = './assets/images/' + this.imageService.getImage();
  }

}
