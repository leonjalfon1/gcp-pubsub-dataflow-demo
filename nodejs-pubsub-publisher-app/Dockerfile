FROM node:10

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

# Configure GCP Authentication
ENV GOOGLE_APPLICATION_CREDENTIALS="/key/service-account.json"
ENV GOOGLE_PROJECT_ID="your-project-name"
ENV GOOGLE_TOPIC_NAME="demo-topic"

EXPOSE 3000
CMD [ "node", "app.js" ]