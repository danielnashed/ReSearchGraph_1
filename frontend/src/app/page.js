"use client";

import Head from "next/head";
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import NavBar from "../components/NavBar";
import Cluster from '../components/Cluster';
import Auth from "../components/Auth";
import { API_ENDPOINTS } from "../Endpoints.js";

const Page = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [clusters, setClusters] = useState([]);
  const [userId, setUserId] = useState(null);

  const papersExample = [
    { title: 'Paper 1', url: 'https://example.com/paper1' },
    { title: 'Paper 2', url: 'https://example.com/paper2' },
    // Add more papers as needed
];
  
  const handleAuthSuccess = (userId) => {
    setIsAuthenticated(true);
    setUserId(userId);
  };

  const handleClustersReceived = (clustersData) => {
    setClusters(clustersData);
  };

  if (!isAuthenticated) {
    return <Auth onAuthSuccess={handleAuthSuccess} onClustersReceived={handleClustersReceived}/>;
  }

  return (
    <div 
      className="relative min-h-screen before:content-[''] before:absolute before:inset-0 before:bg-black/10"
      >
        <NavBar onClustersReceived={handleClustersReceived} />
        <div className="p-4">
          <Head>
            <title>Next.js + Tailwind CSS</title>
            <meta name="description" content="Next.js + Tailwind CSS" />
            <link rel="icon" href="/favicon.ico" />
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet" />
          </Head>
          <main className="text-center pt-16">
            {/* <div className="w-[100%] mx-auto h-[calc(100vh-300px)] mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm"> */}
            {/* <div className="w-[100%] mx-auto h-max mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm flex flex-wrap gap-4 p-4 overflow-auto"> */}
            <div className="w-[100%] mx-auto min-h-screen h-auto mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm flex flex-wrap gap-4 p-4 overflow-auto">
              {clusters.map((cluster, index) => (
                <Cluster
                  key={index}
                  title={cluster.title}
                  papers_count={cluster.papers_count}
                  summary={cluster.summary}
                  papers={cluster.papers}
                />
              ))}
                {/* <Cluster title="Cluster 1" papers_count={10} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={200} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={100} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={300} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={40} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={30} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={80} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={200} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={60} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={10} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={50} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={100} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={10} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={400} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={30} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={80} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={200} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 1" papers_count={60} summary="text" papers={papersExample}/>
                <Cluster title="Cluster 2" papers_count={100} summary="text" papers={papersExample}/> */}
            </div>
          </main>
        </div>
      </div>
  );
};

export default Page;