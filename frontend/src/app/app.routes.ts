import { Routes } from '@angular/router';
import { CreateComponent } from './features/documents/components/create/create.component';
import { ListComponent } from './features/documents/components/list/list.component';

export const routes: Routes = [
    { path: '', component: ListComponent },
    { path: 'criar', component: CreateComponent }
];
