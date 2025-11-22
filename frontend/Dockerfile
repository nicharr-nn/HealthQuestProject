# Use Node.js image
FROM node:20-alpine

# Set work directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install --force && npm install @rollup/rollup-linux-arm64-musl --save-optional

# Copy frontend code
COPY . .

# Expose port
EXPOSE 5173

# Run dev server
CMD ["npm", "run", "dev", "--", "--host"]
