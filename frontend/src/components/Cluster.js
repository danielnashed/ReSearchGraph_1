import { useState, useEffect } from 'react';
import Modal from './Modal';

export default function Cluster({ title, papers_count, summary, papers }) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [randomColor, setRandomColor] = useState('#000000');

    // Calculate the radius based on the paper count
    const radius = 100 + papers_count * 0.5; // Example calculation

    useEffect(() => {
        // Generate a random color on the client side
        setRandomColor(`#${Math.floor(Math.random() * 16777215).toString(16)}`);
    }, []);

    const handleClick = () => {
        setIsModalOpen(true);
    };

    const handleClose = () => {
        setIsModalOpen(false);
    };

    return (
        <>
            <div
                className="flex items-center justify-center text-white rounded-full shadow-xl shadow-zinc-500 m-4 transition-transform transform hover:scale-105 hover:shadow-2xl hover:shadow-zinc-600 cursor-pointer z-10"
                style={{
                    width: `${radius}px`,
                    height: `${radius}px`,
                    backgroundColor: randomColor,
                }}
                onClick={handleClick}
            >
                <div className="text-center">
                    <h2 className="text-lg font-semibold">{title}</h2>
                    <p className="text-sm">{papers_count} papers</p>
                </div>
            </div>
            {isModalOpen && (
                <Modal title={title} summary={summary} papers={papers} backgroundColor={randomColor} onClose={handleClose} />
            )}
        </>
    );
}