import { User } from "./User";

export interface PagedReview {
    items: Array<Review>
    total: number,
    page: number,
    size: number,
    pages: number
}

export interface Review {
    id: number,
    note_visual: number,
    note_music: number,
    description: string,
    avg_note: number,
    creation_date: Date,
    user: User
    music_id: number
}