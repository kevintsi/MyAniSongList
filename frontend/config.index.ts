import { writeFile } from 'fs';

const targetPath = './src/environments/environment.ts';

const envConfigFile = `export const environment = {
   production: true,
   REST_API_URL : '${process.env?.['REST_API_URL']}'
};
`;

writeFile(targetPath, envConfigFile, 'utf8', (err) => {
    if (err) {
        return console.log(err);
    }
});