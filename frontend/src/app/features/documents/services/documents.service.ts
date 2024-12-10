import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root'
})
export class DocumentsService {

  constructor(
    private http: HttpClient
  ) { }

  private url = 'http://localhost:8000/api/docs/';

  createDocument(createData: Document): Observable<Document> {
    return this.http.post<Document>(this.url, createData);
  }

  getAllDocuments(): Observable<any> {
    return this.http.get<any>(this.url);
  }

  updateDocument(id: number, documentData: any): Observable<any> {
    return this.http.put<any>(`${this.url}${id}/`, documentData);
  }

  deleteDocument(id: number): Observable<any> {
    return this.http.delete<any>(`${this.url}${id}/`);
  }

}
