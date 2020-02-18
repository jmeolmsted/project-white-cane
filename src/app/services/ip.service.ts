import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class IpService {
  address = '';

  constructor() { }

  getAddress() {
    return this.address;
  }

  setAddress(ip) {
    this.address = ip.ip;
  }
}
