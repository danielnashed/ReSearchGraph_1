"use client";

import Head from "next/head";
// import TextInput from "../components/TextInput";
import NavBar from "../components/NavBar";
// import Drawer from "../components/Drawer";
// import ChatBox from '../components/ChatBox';
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Cluster from '../components/Cluster';
import { API_ENDPOINTS } from "../Endpoints.js";

const Page = () => {
  const [userId, setUserId] = useState(null);
  const [convId, setConvId] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const [messages, setMessages] = useState([]);
  const mainContentRef = useRef(null);

  const papersExample = [
    { title: 'Paper 1', url: 'https://example.com/paper1' },
    { title: 'Paper 2', url: 'https://example.com/paper2' },
    // Add more papers as needed
];

//   // upon initial mount (first time only), create user and conversation
//   useEffect(() => {
//     const initializeChat = async () => {
//       try {
//         // Create user
//         const userResponse = await axios.post(API_ENDPOINTS.POST_CREATE_USER);
//         if (userResponse.status !== 201) {
//           console.error("Failed to create user");
//           return;
//         }
//         const newUserId = userResponse.data.user_id;
//         setUserId(newUserId);
//         localStorage.setItem('userId', newUserId);

//         // Create conversation
//         const convResponse = await axios.post(
//           API_ENDPOINTS.POST_CREATE_CONV,
//           { user_id: newUserId }
//         );
//         if (convResponse.status !== 201) {
//           console.error("Failed to create conversation");
//           return;
//         }
//         const newConvId = convResponse.data.conv_id;
//         setConvId(newConvId);
//       } catch (error) {
//         console.error("Error initializing chat:", error);
//       }
//     };
//     initializeChat();
//   }, []);

//   // open and close drawer
//   const handleDrawerToggle = () => {
//     setIsDrawerOpen(!isDrawerOpen);
//   };

//   // close drawer when clicking outside the drawer (CAREFUL)
//   const handleClickOutside = (event) => {
//     if (
//       isDrawerOpen && 
//       mainContentRef.current && 
//       event.target instanceof Node && // Type guard for event.target
//       mainContentRef.current.contains(event.target)
//     ) {
//       setIsDrawerOpen(false);
//     }
//   };

//   // if drawer is open, listen to mouse clicks outside the drawer
//   useEffect(() => {
//     document.addEventListener('mousedown', handleClickOutside);
//     return () => {
//       document.removeEventListener('mousedown', handleClickOutside);
//     };
//   }, [isDrawerOpen]);

//   const handleSendMessage = async () => {
//     try {
//         // Add user message
//         setMessages((prev) => [...prev, { type: 'user', content: inputValue }]);
//         const userMessage = inputValue;
//         setInputValue('');
//         const url = API_ENDPOINTS.PUT_UPDATE_CONV.replace(':convId', convId);
//         const response = await axios.put(`${url}`,
//           { user_id: userId, message: userMessage }
//         );
//         if (response.status !== 200) {
//           console.error("Failed to get message from agent.");
//           return;
//         }
//         // Add LLM response
//         setMessages((prev) => [...prev, { type: 'agent', content: response.data.message }]);
//     } catch (error) {
//         console.error("Error fetching data:", error);
//     }
// };

  return (
    <div 
      className="relative min-h-screen before:content-[''] before:absolute before:inset-0 before:bg-black/10"
      >
        {/* <NavBar 
          onMenuClick={handleDrawerToggle}
          setConvId={setConvId}
          setMessages={setMessages}
          convId={convId}
          messages={messages} /> */}
        <div className="p-4">
          <Head>
            <title>Next.js + Tailwind CSS</title>
            <meta name="description" content="Next.js + Tailwind CSS" />
            <link rel="icon" href="/favicon.ico" />
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet" />
          </Head>
          <main className="text-center pt-16">
            {/* <div className="w-[100%] mx-auto h-[calc(100vh-300px)] mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm"> */}
            <div className="w-[100%] mx-auto h-[calc(100vh-100px)] mb-4 rounded-lg border border-zinc-400/30 bg-zinc-800/10 shadow-2xl shadow-zinc-950/90 backdrop-blur-sm flex flex-wrap gap-4 p-4 overflow-auto">
                <Cluster title="Cluster 1" papers_count={10} summary="text" papers={papersExample}/>
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
                <Cluster title="Cluster 2" papers_count={100} summary="text" papers={papersExample}/>
            </div>
            {/* <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 p-4 w-[60%] mb-4">
              <div className="relative flex items-center w-full">
              </div>
            </div> */}
          </main>
        </div>
      </div>
  );
};

export default Page;