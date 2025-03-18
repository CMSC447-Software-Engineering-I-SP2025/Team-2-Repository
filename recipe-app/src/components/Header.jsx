import { Link } from "react-router-dom";

export default function Header () {
    return <header>
        <div className="logo-container"> 
        <Link to="/"> {/* Make the logo return to home */} 
        <img src="/logo-with-name.svg" /> 
        </Link></div>
        <h1>Digital Cookbook</h1>
        <NavBar/>
    </header>
}

function NavBar() {
    return <nav>
        <div><a href="#">My Pantry</a></div>
        <div><a href="#">Account</a></div>
    </nav>
}