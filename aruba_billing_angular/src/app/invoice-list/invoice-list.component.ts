import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-invoice-list',
  templateUrl: './invoice-list.component.html',
  styleUrls: ['./invoice-list.component.css']
})
export class InvoiceListComponent implements OnInit {
  invoices: any[] = [];
  startDateFilter: string = '';
  endDateFilter: string = '';
  searchFilter: string = '';

  constructor(private http: HttpClient, private oauthService: OAuthService) { }

  ngOnInit(): void {
    if (!this.oauthService.hasValidAccessToken()) {
      this.login();
    } else {
      this.loadInvoices();
    }
  }

  login() {
    this.oauthService.initImplicitFlow();
  }

  loadInvoices() {
    let filter_url = "http://localhost:8000/invoices/";

    if (this.startDateFilter && this.endDateFilter) {
      filter_url = `http://localhost:8000/invoices/invoices_in_interval/?start_date=${this.startDateFilter}&end_date=${this.endDateFilter}`;
    } else if (this.startDateFilter) {
      filter_url = `http://localhost:8000/invoices/invoices_in_interval/?start_date=${this.startDateFilter}`;
    } else if (this.endDateFilter) {
      filter_url = `http://localhost:8000/invoices/invoices_in_interval/?end_date=${this.endDateFilter}`;
    }

    if (this.searchFilter){
      filter_url = `http://localhost:8000/invoices/invoices_in_interval/?invoice_id=${this.searchFilter}&start_date=${this.startDateFilter}&end_date=${this.endDateFilter}`;
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${this.oauthService.getAccessToken()}`
    });
    
    this.http.get<any[]>(filter_url, { headers }).subscribe(
      (invoices: any[]) => {
        this.invoices = invoices;
      },
      (error: any) => {
        console.error('Error fetching invoices:', error);
      }
    );
  }

  applyFilters() {
    this.loadInvoices();
  }
}