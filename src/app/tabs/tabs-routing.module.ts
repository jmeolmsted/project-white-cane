import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'sensors',
        children: [
          {
            path: '',
            loadChildren: () =>
              import('../sensors/sensors.module').then(m => m.SensorsPageModule)
          }
        ]
      },
      {
        path: 'images',
        children: [
          {
            path: '',
            loadChildren: () =>
              import('../images/images.module').then(m => m.ImagesPageModule)
          }
        ]
      },
      {
        path: '',
        redirectTo: '/tabs/sensors',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/sensors',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
