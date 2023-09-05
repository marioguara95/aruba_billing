import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InvoiceListComponent } from './invoice-list/invoice-list.component';
import { OAuthModule, OAuthService, OAuthModuleConfig, OAuthStorage, AuthConfig } from 'angular-oauth2-oidc';

@NgModule({
  declarations: [
    AppComponent,
    InvoiceListComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    OAuthModule.forRoot(),
  ],
  providers: [

  ],
  bootstrap: [AppComponent]
})

export class AppModule {}
