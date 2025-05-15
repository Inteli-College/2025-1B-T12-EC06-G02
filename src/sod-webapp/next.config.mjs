/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)', // Aplica a todas as rotas
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: 'https://local-origin.dev, https://*.local-origin.dev, https://*.ngrok-free.app',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, OPTIONS',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
