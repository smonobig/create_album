import React, { useState } from 'react';
import './App.css';

function App() {
    const [albums, setAlbums] = useState([]);
    const [status, setStatus] = useState('Файл не выбран');

    const handleUpload = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        const files = event.target.elements.images.files;

        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        setStatus(`${files.length} файл(ов) выбран(о)`);

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (data.albumUrls) {
                setAlbums(data.albumUrls);
                setStatus('Файл не выбран');
            }
        } catch (error) {
            console.error('Error uploading files:', error);
            setStatus('Ошибка при загрузке');
        }
    };

    return (
        <div className="container">
            <h1>Загрузить фото</h1>
            <form id="uploadForm" onSubmit={handleUpload}>
                <label htmlFor="fileInput">Выбрать файлы</label>
                <input id="fileInput" type="file" name="images" multiple onChange={(e) => setStatus(`${e.target.files.length} файл(ов) выбран(о)`)} />
                <div className="status">{status}</div>
                <button type="submit">Вывести альбомы</button>
            </form>
            <div id="albums">
                {albums.map((url, index) => (
                    <a key={index} href={url} className="album-link">
                        <button className="album-button">
                            {`Album ${index + 1}`}
                        </button>
                    </a>
                ))}
            </div>
        </div>
    );
}

export default App;
