export interface PagedArtist {
    items: Array<Artist>
    total: number,
    page: number,
    size: number,
    pages: number
}


export interface Artist {
    id: number;
    poster_img: string;
    name: string;
    creation_year: string;
}