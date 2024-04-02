import { environment } from "src/environments/environment";

export const LANGUAGE_STORAGE_KEY = "STORAGE_LANG_KEY" in environment ? environment.STORAGE_LANG_KEY as string : "lang"
export const ACCESS_TOKEN_STORAGE_KEY = "STORAGE_ACCESS_TOKEN_KEY" in environment ? environment.STORAGE_ACCESS_TOKEN_KEY as string : "access_token" 