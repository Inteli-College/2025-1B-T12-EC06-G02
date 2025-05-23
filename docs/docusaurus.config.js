// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'SOD',
  tagline: 'SOD',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://Inteli-College.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/2025-1B-T12-EC06-G02/',

  organizationName: 'Inteli-College', // Usually your GitHub org/user name.
  projectName: '2025-1B-T12-EC06-G02', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: ['@docusaurus/theme-mermaid'],
  markdown: {
    mermaid: true,
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Configure color mode explicitly
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      // Enable mermaid in the theme config
      mermaid: {
        theme: {
          light: 'neutral',
          dark: 'dark',
        },
      },
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'SOD',
        logo: {
          alt: 'logo SOD',
          src: 'img/logo.png',
          srcDark: 'img/logo_dark_mode.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentação',
            // Não adicione "to" aqui, pois isso pode causar comportamento inesperado
          },
          {
            href: 'https://github.com/Inteli-College/2025-1A-T12-EC05-G02',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Github',
                to: 'https://github.com/Inteli-College/2025-1B-T12-EC06-G02',
              },
            ],
          },
          // Resto do footer continua igual
        ],
        copyright: `Copyright © ${new Date().getFullYear()} SOD, todos os direitos reservados`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;