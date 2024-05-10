"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { useGeolocated } from "react-geolocated";
import { useEffect } from "react";
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
      console.log("You are right");
    }
    if (transcript.includes("help")) {
      console.log("You are right1");
    }
    if (transcript.includes("great")) {
      console.log("You are right2");
    }
  }, [transcript]);
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
    </main>
  );
}
