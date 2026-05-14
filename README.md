# Driftwood Café

A premium coffee shop application with React frontend and Express backend.

## 🏗️ Project Structure

```
driftwood/
├── client/          # React frontend (Vite + Tailwind)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── server/          # Express backend API
│   ├── index.js
│   └── package.json
├── package.json     # Root package.json for scripts
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm

### Installation & Development
```bash
# Install all dependencies (root, client, and server)
npm run install:all

# Start both frontend and backend
npm run dev
```

This will start:
- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend**: http://localhost:3000 (Express API)

### Individual Commands
```bash
# Frontend only
npm run dev:client

# Backend only  
npm run dev:server

# Build frontend for production
npm run build

# Start production server
npm start
```

## 🛠️ Development

### Environment Variables

**Client (.env in client/ directory):**
```bash
VITE_API_URL=http://localhost:3000
```

**Server (.env in server/ directory):**
```bash
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=your_email@domain.com
```

### Project Features
- **Frontend**: React + Vite + Tailwind CSS + Framer Motion
- **Backend**: Express.js + CORS + Resend (email)
- **Interactive Menu** with shopping cart
- **Contact Forms** with email integration
- **Responsive Design** and smooth animations

## 🚀 Deployment

### Vercel (Recommended)
The project is configured for Vercel with:
- Static frontend served from `/client/dist`
- API routes served from `/server` at `/api/*`

```bash
# Deploy to Vercel
vercel
```

Set environment variables in Vercel dashboard:
- `RESEND_API_KEY`
- `FROM_EMAIL`

## 🔧 API Endpoints

- `POST /api/contact` - Contact form submission
- `POST /api/newsletter` - Newsletter signup

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both client and server
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.