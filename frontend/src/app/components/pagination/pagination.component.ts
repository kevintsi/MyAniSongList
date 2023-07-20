import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent {
  @Input() pagedObject: any
  @Input() currentPage!: number
  @Output() onPageChange: EventEmitter<number> = new EventEmitter<number>()



  onClick(value: number) {
    this.onPageChange.emit(value)
  }

}
