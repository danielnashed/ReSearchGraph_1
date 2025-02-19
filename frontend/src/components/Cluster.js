import { useState, useEffect } from 'react';
import Modal from './Modal';

export default function Cluster({ title, papers_count, summary, papers }) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [randomColor, setRandomColor] = useState('#000000');

    // Calculate the radius based on the paper count
    const radius = 175 + papers_count * 0.6;

    useEffect(() => {
        // Function to generate a random color and ensure it's not too dark
        const generateRandomColor = () => {
            let color;
            do {
                color = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
            } while (isColorTooDark(color));
            return color;
        };

        // Function to check if a color is too dark
        const isColorTooDark = (color) => {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            // Calculate brightness (0-255)
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            return brightness < 50;
        };

        // Generate a random color on the client side
        setRandomColor(generateRandomColor());
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
                <div className="text-center text-wrap p-4">
                    <h2 className="text-sm font-semibold">{title}</h2>
                    <p className="text-sm">{papers_count} papers</p>
                </div>
            </div>
            {isModalOpen && (
                <Modal title={title} summary={summary} papers={papers} backgroundColor={randomColor} onClose={handleClose} />
            )}
        </>
    );
}