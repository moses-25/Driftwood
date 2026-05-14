# Driftwood Café

A premium coffee shop website built with React, Vite, and Tailwind CSS. Features an elegant design, interactive menu, shopping cart, and contact forms.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd driftwood

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables
Create a `.env` file in the root directory:
```bash
# Backend API URL (optional, defaults to localhost:5000)
VITE_API_URL=https://your-api-url.com
```

## 🏗️ Build & Deploy

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

The project includes a `vercel.json` configuration for:
- SPA routing support
- Security headers
- Asset caching

### Environment Variables for Production
Set these in your Vercel dashboard:
- `VITE_API_URL`: Your backend API URL

## 🛠️ Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure
```
src/
├── components/     # Reusable UI components
├── pages/         # Main page components
├── hooks/         # Custom React hooks
├── context/       # React context providers
├── data/          # Static data and content
├── utils/         # Utility functions
├── assets/        # Images and media files
└── animations/    # Framer Motion components
```

## 🔧 Backend Setup (Optional)

The frontend works standalone, but for contact forms and newsletter signup:

1. Navigate to `server/` directory
2. Copy `.env.example` to `.env`
3. Add your Resend API key and email
4. Run: `npm install && npm start`

## 🎨 Features

- **Responsive Design** - Mobile-first approach
- **Interactive Menu** - Dynamic filtering and cart
- **Smooth Animations** - Framer Motion powered
- **Contact Forms** - Email integration via Resend
- **Gallery** - Lightbox image viewer
- **Shopping Cart** - Persistent local storage
- **SEO Optimized** - Meta tags and semantic HTML

## 🔒 Security

- Environment variables for sensitive data
- Input validation and sanitization
- Security headers via Vercel configuration
- No hardcoded secrets in codebase

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `npm run lint` to check code quality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.