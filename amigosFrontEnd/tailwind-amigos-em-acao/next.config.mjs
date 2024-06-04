// next.config.mjs
import { fileURLToPath } from 'url';
import { dirname } from 'path';

export default {
  pageExtensions: ['js', 'jsx', 'ts', 'tsx'],
  webpack: (config) => {

    const __dirname = dirname(fileURLToPath(import.meta.url));

    config.resolve.modules.push(__dirname);
    return config;
  },
};
