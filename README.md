# Research Graph Project

This repository contains the implementation of a cloud-native architecture for a research graph application. The project is designed using microservices and follows best practices for scalability, modularity, and maintainability.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Services](#services)
  - [User Service](#user-service)
  - [Fetch Service](#fetch-service)
  - [Embed Service](#embed-service)
  - [Cluster Service](#cluster-service)
- [Frontend](#frontend)
- [Setup and Deployment](#setup-and-deployment)
  - [Local Development](#local-development)
  - [Deployment to AWS](#deployment-to-aws)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Research Graph Project is a cloud-native application that enables users to fetch, embed, and cluster research papers from external sources like Arxiv. The application is built using a microservices architecture, with each service handling a specific responsibility.

---

## Architecture

The system consists of the following components:

1. **Frontend**: A React-based web application built with Next.js and Tailwind CSS.
2. **Backend Services**: Four microservices implemented using FastAPI:
   - User Service
   - Fetch Service
   - Embed Service
   - Cluster Service
3. **AWS Services**: The application leverages AWS ECS, SQS, EventBridge, and Bedrock for deployment and functionality.

---

## Services

### User Service

- **Purpose**: Manages user authentication and scheduling tasks.
- **Endpoints**:
  - `/users/signup`: Create a new user.
  - `/users/login`: Authenticate a user.
  - `/scheduler/{user_id}`: Enable or disable the scheduler for fetching papers.

### Fetch Service

- **Purpose**: Fetches research papers from external sources like Arxiv.
- **Endpoints**:
  - `/fetch-papers`: Fetches papers based on predefined categories and date ranges.

### Embed Service

- **Purpose**: Generates embeddings for research papers using AWS Bedrock.
- **Functionality**:
  - Processes messages from SQS to create embeddings for fetched papers.

### Cluster Service

- **Purpose**: Clusters research papers based on their embeddings.
- **Functionality**:
  - Processes messages from SQS to create and update clusters.
  - Uses IncrementalDBSCAN for clustering.

---

## Frontend

The frontend is a React-based web application built with Next.js and Tailwind CSS. It provides the following features:

- User authentication (login/signup).
- Dashboard to view and manage research clusters.
- Integration with backend services for fetching, embedding, and clustering papers.

---

## Setup and Deployment

### Local Development

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project3-danielnashed


2. **Backend Setup**:

- Navigate to the backend directory.
- Install dependencies:
    ```bash
    pip install -r requirements.txt
- Run each service locally using uvicorn:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port <port>


3. **Frontend Setup**:

- Navigate to the frontend directory.
- Install dependencies:
    ```bash
    npm install
- Start the development server:
    ```bash
    npm run dev

4. **Deployment to AWS**:

The application is deployed to AWS using ECS and GitHub Actions workflows. Each service has a dedicated workflow file for deployment:

- User Service: deploy_user_service.yaml
- Fetch Service: deploy_fetch_service.yaml
- Embed Service: deploy_embed_service.yaml
- Cluster Service: deploy_cluster_service.yaml

To deploy, push changes to the project3 branch, and the workflows will automatically build and deploy the services.

## Environment Variables
The application requires the following environment variables:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- MONGODB_URI
- AWS_SQS_EMBED_URL
- AWS_SQS_CLUSTER_URL
- AWS_TARGET_ARN
- AWS_TARGET_ROLE_ARN

## Technologies Used

Frontend:
- React
- Next.js
- Tailwind CSS
- DaisyUI

Backend:
- FastAPI
- MongoDB (via Beanie ODM)
- AWS (ECS, SQS, EventBridge, Bedrock)

Other:
- Docker
- GitHub Actions