import { Anime } from "./Anime";
import { Artist } from "./Artist";
import { Type } from "./Type";

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
    anime: Anime,
    type: Type,
    authors: Artist[]
}