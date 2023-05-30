import { Anime } from "./Anime";
import { Artist } from "./Artist";
import { Type } from "./Type";

export interface Music {
    id: number,
    name?: string,
    poster_img?: string,
    release_date?: string,
    anime?: Anime,
    type?: Type,
    authors?: Artist[]
}