import { Injectable } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class ImagesService {
  selected = '';

  constructor() { }

  getImage() {
    return this.selected;
  }

  setImage(file) {
    this.selected = file;
  }
}
