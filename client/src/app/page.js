"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
<<<<<<< HEAD
import { useGeolocated } from "react-geolocated";
import { useEffect } from "react";
=======
import { useEffect,useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from "axios";
>>>>>>> 1c8fd494c15d6175e4de0394628f235f5e858ae7
export default function Home() {
  const [button_status, setButtonStatus] = useState(true);
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();
  const { coords, isGeolocationAvailable, isGeolocationEnabled,watchPosition = true } =
    useGeolocated({
      positionOptions: {
        enableHighAccuracy: false,
      },
      userDecisionTimeout: 5000,
    });
  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
<<<<<<< HEAD
  console.log(watchPosition)
=======
  
>>>>>>> 1c8fd494c15d6175e4de0394628f235f5e858ae7
  useEffect(() => {
    if (transcript.includes("describe")) {
  
      
    }
    if (transcript.includes("help")) {
      console.log("You are right1");
    }
  }, [transcript]);
  useEffect(() => {
    SpeechRecognition.startListening({ continuous: true });
  },[])
  const notify = () => toast("Wow so easy!");
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <video class="w-[40rem] rounded-lg" autoPlay controls>
        <source src="video4.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div>
        <p>Microphone: {listening ? "on" : "off"}</p>
        <button
          onClick={SpeechRecognition.startListening({ continuous: true })}
        >
          Start
        </button>
        <button onClick={SpeechRecognition.stopListening}>Stop</button>
        <button onClick={resetTranscript}>Reset</button>
        <p>{transcript}</p>
      </div>
      {!isGeolocationAvailable ? (
        <div>Your browser does not support Geolocation</div>
      ) : !isGeolocationEnabled ? (
        <div>Geolocation is not enabled</div>
      ) : coords ? (
        <table>
          <tbody>
            <tr>
              <td>latitude</td>
              <td>{coords.latitude}</td>
            </tr>
            <tr>
              <td>longitude</td>
              <td>{coords.longitude}</td>
            </tr>
            <tr>
              <td>altitude</td>
              <td>{coords.altitude}</td>
            </tr>
            <tr>
              <td>heading</td>
              <td>{coords.heading}</td>
            </tr>
            <tr>
              <td>speed</td>
              <td>{coords.speed}</td>
            </tr>
          </tbody>
        </table>
      ) : (
        <div>Getting the location data&hellip; </div>
      )}
      <img class="w-[40rem] rounded-lg" src="http://127.0.0.1:8000/stream/"/>
    <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" >Start</button>
    </main>
        
  );
}
