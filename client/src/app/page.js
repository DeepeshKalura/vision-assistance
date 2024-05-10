"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { useEffect,useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from "axios";
export default function Home() {
  const [button_status, setButtonStatus] = useState(true);
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();
  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
  
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
      <img class="w-[40rem] rounded-lg" src="http://127.0.0.1:8000/stream/"/>
    <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" >Start</button>
    </main>
        
  );
}
