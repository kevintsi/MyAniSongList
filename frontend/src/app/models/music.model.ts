import { Anime } from "./anime.model";
import { Artist } from "./artist.model";
import { Type } from "./type.model";

export interface PagedMusic {
    items: Array<Music>
    total: number,
    page: number,
    size: number,
    pages: number
}

export interface Music {
    id: number,
    name: string,
    poster_img: string,
    release_date: Date,
    avg_note: number,
    id_video: string,
    anime: Anime,
    type: Type,
    artists: Artist[]
}