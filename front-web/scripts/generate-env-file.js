const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

const ENV_VARS_PREFIX = 'VUE_APP';

/**
 * pre-run script
 * Читает переменные окружения и пишет их в OUTPUT_DIR или в public/env-config.js
 *
 */

const outputDir = process.argv[2];

if (!outputDir) {
    console.log(`Usage: node ${process.argv[1]} OUTPUT_DIRECTORY`);
    return;
}

if (!fs.existsSync(process.argv[0])) {
    console.error('Specified directory does not exists');
    return;
}

const vars = {};

// read from .env file
const result = dotenv.config();

if (result.error) {
    console.warn('Can\'t find .env file. Using environment variables only');
} else {
    // read only those vars that starts from REACT_APP
    for (const prop of Object.keys(result.parsed)) {
        if (prop.startsWith(ENV_VARS_PREFIX)) {
            vars[prop] = result.parsed[prop];
        }
    }
}

// read env that starts from REACT_APP
for (const prop of Object.keys(process.env)) {
    if (prop.startsWith(ENV_VARS_PREFIX)) {
        vars[prop] = process.env[prop];
    }
}

const envFileLocation = path.join(outputDir || 'public/', 'env-config.js');
const envFileData = `// DO NOT EDIT
//this file was generated automatically
window.__ENV__ = ${JSON.stringify(vars)};`;

fs.writeFile(envFileLocation, envFileData, err => {
    if (err) {
        console.error(err);
        return;
    }

    console.log(`Write env vars to ${envFileLocation}`);
});
