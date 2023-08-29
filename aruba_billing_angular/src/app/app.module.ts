import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InvoiceListComponent } from './invoice-list/invoice-list.component';
import { OAuthModule, OAuthService, OAuthModuleConfig, OAuthStorage, AuthConfig } from 'angular-oauth2-oidc';

export function authModuleConfigFactory(): OAuthModuleConfig {
  return {
    resourceServer: {
      allowedUrls: ['http://127.0.0.1:8000/'],
      sendAccessToken: true,
    },
  };
}
const authConfig: AuthConfig = {
  issuer: 'http://127.0.0.1:8000/', // URL dell'endpoint di token di autorizzazione
  clientId: 'Sla8EStkKqYCYVgImK9UuyOOb8RBYsxsH3w9dUna',
  redirectUri: 'http://localhost:4200/', // L'URL di callback che hai definito nell'app Django
  responseType: 'code', // Usa 'code' per il flusso di concessione del codice
};

@NgModule({
  declarations: [
    AppComponent,
    InvoiceListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    OAuthModule.forRoot(),
  ],
  providers: [
    { provide: OAuthModuleConfig, useFactory: authModuleConfigFactory },
    OAuthService,
  ],
  bootstrap: [AppComponent]
})

export class AppModule {
  constructor(private oauthService: OAuthService) {
      this.oauthService.configure(authConfig);
      this.oauthService.setupAutomaticSilentRefresh(); // Se supportato dal tuo backend
  }
}
