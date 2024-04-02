import { AppLanguage } from "../interfaces/app-language.interface";
import { LANGUAGE_STORAGE_KEY } from "./storage.config";

export const AppLanguages: AppLanguage[] = [{
    "id": "fr",
    "code": "Français",
},
{
    "id": "en",
    "code": "English",
},
{
    "id": "jp",
    "code": "日本語",
}
]

export const getLangFromStorage = () => {
    const storage = localStorage.getItem(LANGUAGE_STORAGE_KEY)
    try {
        if (!storage) throw new Error()
        const lang = AppLanguages.find(l => l.id == storage)
        if (!lang) throw new Error()
        return lang
    } catch (error) {
        return AppLanguages[0]
    }

}