# Dockerfile for React App
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the React port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
