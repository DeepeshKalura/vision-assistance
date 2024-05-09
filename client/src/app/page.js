"use client";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { useEffect } from "react";
export default function Home() {
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
    </main>
  );
}
