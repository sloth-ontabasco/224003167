import "./App.css";
import TrainCard from "./components/TrainCard";
import { useEffect, useState } from "react";

function App() {
    const [train, setTrain] = useState([]);

    useEffect(() => {
        console.log('use efffecting')
        fetch("http://127.0.0.1:5000/api/auth").then((response) =>
            response.json()
        );
        fetch("http://127.0.0.1:5000/api/trains")
            .then((response) => response.json())
            .then((data) => setTrain(data.trains));
    }, []);

    console.log(train);
    return (
        <>
            <div></div>
            <h1>Upcoming Trains</h1>
            {train !== [] ? (
                train.map((tr, index) => (
                    <TrainCard key={index}
                               trainName={tr.trainName}
                               trainNumber={tr.trainNumber}
                               delayedBy={tr.delayedBy}
                               seatsAvailable={[tr.seatsAvailable.sleeper, tr.seatsAvailable.AC]} 
                               departureTime={tr.departureTime}
                               price={[tr.price.sleeper, tr.price.AC]}
                     />
                ))
            ) : (
                <h2>Loading...</h2>
            )}
        </>
    );
}

export default App;
