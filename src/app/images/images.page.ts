import { ImagesService } from './../services/images.service';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
import { Observable} from 'rxjs';




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

  constructor(private http: HttpClient, private imageService: ImagesService) {
  }

  // tslint:disable-next-line: use-lifecycle-interface
  ngOnInit() {
    this.http.get('http://127.0.0.1:5002/files').subscribe(data => {
      this.fileData = data as JSON;
      console.log(this.fileData);
    });
    this.server = this.http.get('http://127.0.0.1:5002/files');
  }

  openImage(file) {
    this.imageService.setImage(file);
    if (file === this.selected) {
      this.showImage = false;
    } else {
      this.showImage = true;
    }
    this.selected = file;
    this.data.image = './assets/images/' + this.imageService.getImage();
  }

}
