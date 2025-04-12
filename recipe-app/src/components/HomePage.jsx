import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="homepage">

      {/* Video Background */}
      <div className="video-background">
        <video autoPlay loop muted>
          <source src="/background_video.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        </div>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-overlay">
          <h1>Welcome to Your Digital Cookbook</h1>
          <p>Discover, save, and log recipes tailored to your lifestyle.</p>
          <Link to="/search" className="hero-cta">Explore Recipes</Link>
        </div>
      </section>

    </div>
  );
}
