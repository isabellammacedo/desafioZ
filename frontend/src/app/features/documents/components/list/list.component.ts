import { Component, OnInit } from '@angular/core';
import { DocumentsService } from '../../services/documents.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-list',
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss'
})
export class ListComponent implements OnInit {
  documents: any[] = [];
  documentToUpdate: any = null;

  constructor(
    private documentService: DocumentsService
  ) { }

  ngOnInit(): void {
    this.loadDocuments();
  }

  loadDocuments(): void {
    this.documentService.getAllDocuments().subscribe((data: any) => {
      this.documents = data;
    });
  }

  onEdit(document: any): void {
    this.documentToUpdate = { ...document };
  }

  onSaveEdit(): void {
    if (this.documentToUpdate) {
      this.documentService.updateDocument(this.documentToUpdate.id, this.documentToUpdate).subscribe(response => {
        console.log('Documento atualizado com sucesso!', response);
        this.loadDocuments();
        this.documentToUpdate = null;
      });
    }
  }

  onDelete(id: number): void {
    if (confirm('Você confirma a exclusão deste documento?')) {
      this.documentService.deleteDocument(id).subscribe(response => {
        console.log('Documento excluído com sucesso!', response);
        this.loadDocuments();
      });
    }
  }
}