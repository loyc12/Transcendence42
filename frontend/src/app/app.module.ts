import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { TopBarComponent } from './top_bar/top_bar.component';
import { ListComponent } from './list/list.component';
import { MainComponent } from './main/main.component';

@NgModule({
    import: [
        BrowserModule,
        ReactiveFormsModule,
        RouterModule.forRoot([
            { path: '', component: ListComponent },
        ])
    ],
    declarations: [
        AppComponent,
        TopBarComponent,
        ListComponent
    ],
    bootstrap: [
        AppComponent
    ]
})
export class AppModule { }