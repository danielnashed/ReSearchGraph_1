// import Modal from './Modal';
import axios from 'axios';
import { API_ENDPOINTS } from "../Endpoints.js";
import { useState, useEffect } from 'react';

export default function NavBar({onClustersReceived}) {

    const [isRetrieverActive, setIsRetrieverActive] = useState(false);

    const handleRetrieverClick = () => {
        handleRetriever();
        setIsRetrieverActive(!isRetrieverActive);
    };


    const handleRetriever = async () => {
        const userId = localStorage.getItem('userId');
        const url = API_ENDPOINTS.POST_SCHEDULER.replace(':userId', userId);
        // Start or stop retriever
        const response = await axios.post(`${url}`, { scheduler_on: !isRetrieverActive });
        if (response.status !== 200) {
            console.error("Failed to change status of scheduler");
            return;
        }
    };

    const handleLogOut = () => {
        localStorage.clear();
        window.location.href = '/';
    };

    const updateDashboard = async () => {
        try {
            const userId = localStorage.getItem('userId');
            const url = API_ENDPOINTS.GET_CLUSTERS.replace(':userId', userId);
            const response = await axios.get(`${url}`);
            if (response.status === 200) {
                const clusters = response.data.clusters;
                onClustersReceived(clusters);
            } else {
                console.error('Failed to update dashboard');
            }
        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
      };

    return (
        <div className="navbar bg-base-100 bg-zinc-800/0 absolute top-0 w-full z-50">
            <div className="flex-none">
                <button onClick={updateDashboard} className="btn btn-square btn-ghost">
                    <img src="/refresh.png" alt="Update Dashboard" className="inline-block h-5 w-5" />
                </button>
            </div>
            <div className="flex-1">
                <span className="text-xl font-normal font-['Montserrat']">AI Research Trends</span>
            </div>
            <div className="flex-none">
                <div className="dropdown dropdown-left dropdown-hover">
                    <button tabIndex={0} className="btn btn-square btn-ghost">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            className="inline-block h-5 w-5 stroke-current">
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z">
                            </path>
                        </svg>
                    </button>
                    <ul tabIndex={0} className="dropdown-content menu bg-neutral-400/100 rounded-box z-30 w-52 p-2 shadow-zinc-800 shadow-lg">
                        <li>
                            <a onClick={handleRetrieverClick}
                                className={`px-4 py-2 rounded ${isRetrieverActive ? 'bg-red-500 text-white' : 'bg-emerald-500 text-white'}`}>
                                {isRetrieverActive ? 'Stop Retriever' : 'Start Retriever'}
                            </a>
                        </li>
                        <li><a onClick={handleLogOut}>Logout</a></li>
                    </ul>
                </div>
            </div>
        </div>
    );
}