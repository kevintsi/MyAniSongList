import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Artist } from 'src/app/models/Artist';

@Component({
  selector: 'app-form-artist',
  templateUrl: './form-artist.component.html',
  styleUrls: ['./form-artist.component.css']
})
export class FormArtistComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() artist!: Artist; // Existing data for update operation

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  form!: FormGroup;
  previewImage?: any = null

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  initForm() {
    this.form = this.formBuilder.group({
      name: new FormControl("", [Validators.required]),
      creation_year: new FormControl("", [Validators.required]),
      poster_img: new FormControl(null, [this.isUpdate ? Validators.nullValidator : Validators.required])
    });
  }

  populateForm() {
    this.form.patchValue({
      name: this.artist.name,
      creation_year: this.artist.creation_year
    });

    this.previewImage = this.artist.poster_img
  }

  onSubmit() {
    if (this.form.valid) {
      const formData = this.form.value;
      this.submitForm.emit(formData);
    }
  }

  processFile(imageInput: any) {
    const file = imageInput.files[0];
    if (file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(file.type)) {
        this.form.patchValue({
          poster_img: file
        })

        this.previewImage = URL.createObjectURL(file)
      }
    }
  }
}
