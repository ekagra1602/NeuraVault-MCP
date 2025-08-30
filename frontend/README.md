# MCP Frontend

A modern, dynamic React frontend for the Model Context Protocol (MCP) server.

## Features

- ⚡ **Modern Stack**: Built with React 18, TypeScript, and Vite
- 🎨 **Beautiful UI**: Tailwind CSS with custom design system
- 🚀 **Smooth Animations**: Framer Motion for delightful interactions
- 📱 **Responsive Design**: Works perfectly on all devices
- 🌙 **Dark Theme**: Modern dark theme with glass morphism effects
- 🎯 **Accessible**: Built with accessibility best practices

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **UI Components**: Radix UI primitives
- **Routing**: React Router DOM

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── HeroSection.tsx
│   ├── FeaturesSection.tsx
│   ├── CodeExamples.tsx
│   ├── Navigation.tsx
│   └── Footer.tsx
├── pages/              # Page components
│   ├── HomePage.tsx
│   └── DocsPage.tsx
├── lib/                # Utilities
│   └── utils.ts
├── App.tsx             # Main app component
├── main.tsx           # Entry point
└── index.css          # Global styles
```

## Design System

### Colors
- **Primary**: Blue gradient (#3B82F6 to #8B5CF6)
- **Secondary**: Emerald to blue gradient
- **Background**: Dark theme with glass morphism
- **Text**: High contrast for accessibility

### Components
- **Glass Morphism**: Translucent components with backdrop blur
- **Gradients**: Vibrant text and background gradients
- **Animations**: Smooth hover states and entrance animations
- **Typography**: Inter font family with proper hierarchy

## API Integration

The frontend includes a proxy configuration in `vite.config.ts` that forwards API calls to the MCP server:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

## Development

### Adding New Components
1. Create component in `src/components/`
2. Export from component file
3. Import and use in pages or other components

### Styling Guidelines
- Use Tailwind utility classes
- Leverage custom CSS variables for theming
- Follow responsive-first approach
- Use Framer Motion for animations

### Performance
- Components are optimized with React best practices
- Images are optimized and lazy-loaded
- Bundle is code-split automatically by Vite

## Deployment

Build the project and serve the `dist` folder:

```bash
npm run build
npm run preview
```

For production deployment, serve the built files with any static hosting service.
