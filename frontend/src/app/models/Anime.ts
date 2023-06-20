export interface PagedAnime {
    items: Array<Anime>
    total: number,
    page: number,
    size: number,
    pages: number
}

export interface Anime {
    id: number;
    name: string;
    description: string;
    poster_img: string;
}