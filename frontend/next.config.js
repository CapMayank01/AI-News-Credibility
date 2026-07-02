/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  pageExtensions: ['tsx', 'ts', 'jsx', 'js'],
  typescript: {
    tsconfigPath: './tsconfig.json',
  },
}

module.exports = config
