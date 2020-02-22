import { IpAddressService } from './../services/ip-address.service';
import { IpService } from './../services/ip.service';
import { ImagesService } from './../services/images.service';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
import { Observable } from 'rxjs';
import { stringify } from 'querystring';



@Component({
  selector: 'app-images',
  templateUrl: 'images.page.html',
  styleUrls: ['images.page.scss']
})
export class ImagesPage {
  title = 'app';

  fileData: JSON;
  data = {
    dist: 2,
    camera: true,
    image: './assets/images/favicon.png'
  };

  server: Observable<any>;

  selected = '';

  showImage = false;
  ipAddress: string;
  endpoint: string;
  url = 'http://';
  results = {};

  constructor(private http: HttpClient, private imageService: ImagesService, private ipService: IpService, private ip: IpAddressService) {
  }

  // tslint:disable-next-line: use-lifecycle-interface
  ngOnInit() {
    // tslint:disable-next-line: no-console
    this.ipAddress = window.location.hostname;
    console.log(this.ipAddress);
    this.url = this.url.concat('10.16.22.51:5000/files');
    this.http.get(this.url).subscribe(files => {
      this.fileData = files as JSON;
    });

    // this.http.get('http://127.0.0.1:5002/ipAddress').subscribe(data => {
    //   this.ipService.setAddress(data);
    //   this.url = this.url.concat(this.ipAddress, ':5000/files');
    //   this.http.get(this.url).subscribe(files => {
    //     this.fileData = files as JSON;
    //   });
    // this.ip.getIPAddress().subscribe((res: any) => {
    //   this.ipAddress = res.ip;
    //   this.url = this.url.concat(this.ipAddress, ':5000/files');
    //   console.log(this.url);
    //   this.http.get(this.url).subscribe(files => {
    //     this.fileData = files as JSON;
    //   });
    this.server = this.http.get(this.url);

  }

  getIP() {
    this.ip.getIPAddress().subscribe((res: any) => {
      this.ipAddress = res.ip;
      console.log(this.ipAddress);
    });
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
