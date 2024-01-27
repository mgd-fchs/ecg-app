# Dockerfile for React Frontend

FROM node:14
WORKDIR /app
COPY ./ /app
RUN npm install
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
