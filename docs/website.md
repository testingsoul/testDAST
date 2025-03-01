Follow this instructions to install and run the e-commerce application locally.


1. Create the project structure:
```bash
mkdir ecommerce-app
cd ecommerce-app
mkdir backend frontend
```

2. Set up the backend:
```bash
cd backend
npm init -y
npm install express sqlite3 bcrypt jsonwebtoken cors
```

3. Set up the frontend:
```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install
npm install lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

5. Start the applications:

For the backend:
```bash
cd backend
node server.js
```

For the frontend (in a new terminal):
```bash
cd frontend
npm run dev
```

The application is running at:
- Frontend: http://localhost:5173
- Backend: http://localhost:3001

Default admin credentials are:
- Username: admin
- Password: admin123