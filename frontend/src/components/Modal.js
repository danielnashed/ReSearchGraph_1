export default function Modal({ title, summary, papers, backgroundColor, onClose }) {

    // Function to convert hex to RGBA
    const hexToRgba = (hex, alpha = 0.95) => {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    };

    const translucentBackgroundColor = hexToRgba(backgroundColor);

    return (
        <div 
            // className="fixed inset-0 flex flex-col items-center justify-center z-50"
            className="fixed inset-0 flex flex-col items-center justify-center z-50"
            style={{ backgroundColor: translucentBackgroundColor
             }}
        >
                <button onClick={onClose} className="absolute top-4 right-4 text-black">
                    &times;
                </button>
                <h2 className="text-2xl font-semibold mb-4">{title}</h2>
                <p className="mb-4">{summary}</p>
                <ul className="list-disc pl-5">
                    {papers.map((paper, index) => (
                        <li key={index}>
                            <a href={paper.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
                                {paper.title}
                            </a>
                        </li>
                    ))}
                </ul>
        </div>
    );
}