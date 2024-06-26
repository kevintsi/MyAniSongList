import { Music } from "./music.model";
import { User } from "./user.model";

export interface PagedReview {
    items: Array<Review>
    total: number,
    page: number,
    size: number,
    pages: number
}

export interface Review {
    id?: number,
    note_visual: number,
    note_music: number,
    description: string,
    creation_date: Date,
    user: User
    music: Music
}