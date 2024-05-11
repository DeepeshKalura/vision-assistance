"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { useGeolocated } from "react-geolocated";
import { useEffect,useState } from "react";
import axios from "axios";
export default function Home() {
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
  console.log(watchPosition)
  
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
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <img class="w-[40rem] rounded-lg" src="http://127.0.0.1:8000/stream/"/>
      {/* {!isGeolocationAvailable ? (
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
      )} */}
      <time datetime="2016-10-25" suppressHydrationWarning={true} />
    <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" >Start</button>
    </div>
        
  );
}
