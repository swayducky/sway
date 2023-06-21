import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [images, setImages] = useState({});
    const [currentDirIndex, setCurrentDirIndex] = useState(0);

    useEffect(() => {
        axios.get('http://localhost:5000/api/images')
            .then(response => {
                setImages(response.data);
            })
            .catch(error => {
                console.error('Error fetching data', error);
            });
    }, []);

    const dirs = Object.keys(images);

    const nextDirectory = () => {
        setCurrentDirIndex((prevIndex) => {
            return (prevIndex + 1) % dirs.length;
        });
    };

    const prevDirectory = () => {
        setCurrentDirIndex((prevIndex) => {
            return (prevIndex - 1 + dirs.length) % dirs.length;
        });
    };

    return (
        <div className="App" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh'}}>
            {dirs.length > 0 && (
                <div style={{textAlign: 'center'}}>
                    <h2>{dirs[currentDirIndex]}</h2>
                    <div style={{margin: '30px'}}>
                        <button onClick={prevDirectory}>Previous</button>
                        <button onClick={nextDirectory}>Next</button>
                    </div>
                    {images[dirs[currentDirIndex]].map(image => (
                        <img 
                            key={image} 
                            src={`http://localhost:5000/${image}`} 
                            alt={image} 
                            style={{
                                borderRadius: "50%",
                                width: "200px",
                                margin: "20px",
                                boxShadow: "0px 0px 10px 5px rgba(10, 173, 10, 1.0)"
                            }}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}

export default App;