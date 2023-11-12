# Use Node.js LTS as the base image
FROM node:14

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the TypeScript files
COPY . .

# Compile TypeScript
RUN npx tsc

# Expose port 3000 (adjust as needed)
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
