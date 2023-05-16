import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { User } from '../../models/User';
import { StorageService } from '../../_services/storage.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user: any


  constructor(private authService: AuthService, private storageService: StorageService) { }

  ngOnInit(): void {
    this.user = this.storageService.getUser()
  }

}
