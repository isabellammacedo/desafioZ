import { Component } from '@angular/core';
import { DocumentsService } from '../../services/documents.service';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-create',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './create.component.html',
  styleUrl: './create.component.scss'
})
export class CreateComponent {

  createForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private documentService: DocumentsService
  ) {
    this.createForm = this.fb.group({
      name: ['', Validators.required],
      url_pdf: ['', [Validators.required, Validators.pattern('(http|https):\/\/.+\.(pdf)$')]],
      signers: this.fb.array([]),
    });
  }

  get signers() {
    return this.createForm.get('signers') as FormArray;
  }

  addSignatario() {
    const signerGroup = this.fb.group({
      name: ['', Validators.required],
      email: ['']
    });
    this.signers.push(signerGroup);
  }

  deleteSignatario(index: number) {
    this.signers.removeAt(index);
  }

  onSubmit() {
    if (this.createForm.valid) {
      this.documentService.createDocument(this.createForm.value).subscribe({
        next: (response) => {
          // TODO: adicionar uma mensagem melhor
          alert('Documento criado com sucesso!');
        },
        error: (err) => {
          console.error('Erro:', err);
          // TODO: adicionar uma mensagem melhor
          alert('Erro ao criar documento!');
        },
      });
    }
  }

}
