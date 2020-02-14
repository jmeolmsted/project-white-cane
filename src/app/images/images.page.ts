import { Component } from '@angular/core';



@Component({
  selector: 'app-images',
  templateUrl: 'images.page.html',
  styleUrls: ['images.page.scss']
})
export class ImagesPage {
  data = {
    dist: 2,
    camera: true,
    image: './assets/images/favicon.png'
  };

  constructor() {
  }

  // async getImageFiles() {
  //   await this.platform.ready();
  //   this.file.checkDir('file:///', '').then(_ => console.log('Directory exists')).catch(err =>
  //     console.log('Directory doesn\'t exist'));
  // }

  // tslint:disable-next-line: use-lifecycle-interface
  ngOnInit() {
  }
}
