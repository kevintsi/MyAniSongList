import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Subscription, firstValueFrom } from 'rxjs';
import { LanguageService } from 'src/app/services/language/language.service';
import { TypeService } from 'src/app/services/type/type.service';
import { Language } from 'src/app/models/language.model';
import { Type } from 'src/app/models/type.model';

@Component({
  selector: 'app-manage-create-type-translation',
  templateUrl: './manage-create-type-translation.component.html',
  styleUrls: ['./manage-create-type-translation.component.css']
})
export class ManageCreateTypeTranslationComponent implements OnInit, OnDestroy {

  isLoading: boolean = true
  languages!: Language[]
  formTypeGroup!: FormGroup
  addTranslationSubscription: Subscription = new Subscription()

  constructor(
    private languageService: LanguageService,
    private typeService: TypeService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private toast: ToastrService
  ) { }


  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.languages = await this.getLanguages()
      this.formTypeGroup = this.formBuilder.group({
        name: new FormControl('', [Validators.required]),
        language: new FormControl('fr', [Validators.required])
      })
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }
  getLanguages() {
    return firstValueFrom(this.languageService.getAll())
  }

  onSubmit() {
    if (this.formTypeGroup.valid) {
      let type: Type = {
        id: parseInt(String(this.route.snapshot.paramMap.get('id'))),
        name: this.formTypeGroup.get('name')?.value
      }
      this.addTranslationSubscription = this.typeService.addTranslation(type, this.formTypeGroup.get('language')?.value).subscribe({
        next: () => {
          this.toast.success("La traduction a bien été ajoutée", 'Ajout')
        },
        error: (err: HttpErrorResponse) => {
          console.error(err)
          if (err.status == 409) {
            this.toast.error("La traduction pour cette langue existe déjà", 'Ajout')
          }
        }
      })
    }
  }

  ngOnDestroy(): void {
    this.addTranslationSubscription.unsubscribe()
  }

  onChange($event: Event) {
    let lang_code: string = ($event.target as HTMLSelectElement).value
    this.formTypeGroup.patchValue({
      language: lang_code
    })
  }

}
