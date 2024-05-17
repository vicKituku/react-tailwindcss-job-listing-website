import React, { useEffect, useState } from "react";
import Hero from "../components/Hero";
import HomeCards from "../components/HomeCards";
import JobListings from "../components/JobListings";
import ViewAllJobs from "../components/ViewAllJobs";

const HomePage = () => {
  const [health, setHealth] = useState("not healthy");
  useEffect(() => {
    const fetchHealth = async () => {
      const url = "https://fastapi-joblisting-api.onrender.com/healthcheck";
      try {
        const res = await fetch(url);
        data = res.json();
        setHealth(data);
      } catch (error) {
        console.log("Error fetching data", error);
      }
    };
    fetchHealth();
  }, []);
  return (
    <>
      <Hero />
      <HomeCards />
      <JobListings isHome={true} />
      <ViewAllJobs />
      {health}
    </>
  );
};

export default HomePage;
