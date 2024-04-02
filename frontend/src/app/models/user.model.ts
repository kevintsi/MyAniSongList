export interface PagedUser {
    items: Array<User>
    total: number,
    page: number,
    size: number,
    pages: number
}


export interface User {
    id?: number;
    username?: string;
    email?: string;
    password?: string;
    profile_picture?: string;
}