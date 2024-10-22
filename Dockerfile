# Use the official Node.js image as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code to the container
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port 3000 for the Next.js app
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "run", "start"]