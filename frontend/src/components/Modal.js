export default function Modal({ title, summary, papers, backgroundColor, onClose }) {
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-8 w-3/4 max-w-3xl">
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
        </div>
    );
}