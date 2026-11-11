"use client";

import { useEffect, useState } from "react";


export default function Home() {

  const [message, setMessage] = useState("")

  useEffect(() => {

  async function fetchApi(){
    try {
      console.log(process.env.NEXT_PUBLIC_API_URL)
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/`
      );

      if(!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      setMessage(data.message);
    } catch (error){
      console.error(error);
      setMessage("Error connecting to API");
    }

  }

  fetchApi();
}, [])
  return (
    <div className="flex flex-col flex-1 items-center justify-center font-sans">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 sm:items-start">
       <h1 className="text-black"> {message}, Juliet</h1>
      </main>
    </div>
  );
}
