"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useGeolocated } from "react-geolocated";
import { useEffect,useState,useCallback ,useRef} from "react";
import axios from "axios";



const convertTextToAudio = async (textToConvert) => {
  // Set the API key for ElevenLabs API
  const apiKey = "1f054de594b0608dd0c970202f666bdb";
  // ID of voice to be used for speech
  const voiceId = '21m00Tcm4TlvDq8ikWAM';

  // API request options
  const apiRequestOptions = {
    method: 'POST',
    url: `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
    headers: {
      accept: 'audio/mpeg',
      'content-type': 'application/json',
      'xi-api-key': apiKey,
    },
    data: {
      text: textToConvert,
    },
    responseType: 'arraybuffer', // To receive binary data in response
  };

  // Sending the API request and waiting for response
  const apiResponse = await axios.request(apiRequestOptions);

  // Return the binary audio data received from API
  return apiResponse.data;
};





export default function Home() {
  const [sourceUrl, setSourceUrl] = useState(null);
  const [socketUrl, setSocketUrl] = useState('ws://127.0.0.1:8000/stream/ws');
  const [messageHistory, setMessageHistory] = useState([]);
  const [imgsrc, setimg] = useState(null);
  const [previousMessage, setPreviousMessage] = useState(null);
  const audioRef = useRef(null);
 

  useEffect(() => {
    if (sourceUrl) {
      // Play audio when sourceUrl is set
      audioRef.current.play();
    }
  }, [sourceUrl]);
  useEffect(() => {
    setimg("http://127.0.0.1:8000/stream")

  },[ReadyState])
  console.log(imgsrc)
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage]);

  useEffect(() => {
    if (lastMessage && lastMessage.data !== previousMessage) { // Check if the current message is different from the previous one
      fetchAndUpdateAudioData(lastMessage.data);
      setPreviousMessage(lastMessage.data); // Update previous message
    }
  }, [lastMessage, previousMessage]);

  
  const handleClickSendMessage = useCallback(() => sendMessage('Hello'), []);
  

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  const fetchAndUpdateAudioData = async (text) => {
    const audioData = await convertTextToAudio(text);
    const audioBlob = new Blob([audioData], { type: 'audio/mpeg' });

    // Create a URL for the audio blob
    const blobUrl = URL.createObjectURL(audioBlob);

    // Update the sourceUrl state variable with the generated URL for the audio blob
    setSourceUrl(blobUrl);
    audioElement.play();
  }
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
    <div>
  
      <button
        onClick={handleClickSendMessage}
        disabled={readyState !== ReadyState.OPEN}
      >
        Click Me to send 'Hello'
      </button>
      <span>The WebSocket is currently {connectionStatus}</span>
      
      {/* {lastMessage ?      fetchAndUpdateAudioData(lastMessage.data) : null} */}
      <ul>
        {messageHistory.map((message, idx) => (
          <span key={idx}>{message ? message.data : null}</span>
        ))} 
      </ul>
    </div>
      <img class="w-[40rem] rounded-lg" src={imgsrc}/>
      {sourceUrl && (
        <audio ref={audioRef}>
          <source src={sourceUrl} type='audio/mpeg' />
        </audio>
      )}
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
    </div>
        
  );
}
