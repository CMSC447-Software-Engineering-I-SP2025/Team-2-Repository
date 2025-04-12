import { Link } from "react-router-dom";

export default function Header() {
    return (
        <header className="header">

            {/* Logo and Name */}
            <div className="logo-container">
                <Link to="/">
                    <img src="/logo-with-name.svg" alt="Digital Cookbook Logo" />
                </Link>
            </div>

            <nav className="main-nav">
            {[
                { name: "Dish Type", links: ["Finger Food", "Appetizer", "Lunch", "Main Course", "Dinner", "Dessert"], basePath: "/dish-type" },
                { name: "Diets", links: ["Gluten Free", "Dairy Free", "Vegan", "Vegetarian", "Paleo", "Ketogenic"], basePath: "/diets" },
                { name: "Season", links: ["Winter", "Spring", "Summer", "Autumn"], basePath: "/season" },
                { name: "Cuisines", links: ["Asian", "Chinese", "Indian", "Japanese", "Korean", "Mexican"], basePath: "/cuisines" },
                { name: "Cook Time", links: ["Under 30 Mins", "30-60 Mins"], basePath: "/cook-time" },
            ].map(({ name, links, basePath }) => (
                <div className="nav-item" key={name}>
                <Link to={basePath}>{name}</Link>
                <div className="dropdown">
                    {links.map(link => (
                    <Link to={`${basePath}/${link.toLowerCase().replace(/\s+/g, '-')}`} key={link}>
                        {link}
                    </Link>
                    ))}
                </div>
                </div>
            ))}
            </nav>

            
            {/* Log Ingredients Link */}
            <div className="log-ingredients">
                <Link to="/pantry">Log Ingredients</Link>
            </div>

            {/* Icons for Search, Saved Recipes, and Account w/ Dropdown*/}
            <div className="icon-group">
                {[
                    { path: "/search", icon: "/search-icon.png", alt: "Search", className: "search-icon" },
                    { path: "/saved-recipes", icon: "/save-icon.png", alt: "Saved Recipes", className: "icon" },
                    { path: "/my-account", icon: "/person-icon.svg", alt: "Account", className: "icon", /* dropdown: ["My Account", "Settings", "Logout"] */ },
                ].map(({ path, icon, alt, className }) => (
                    <Link to={path} className={className} key={alt}>
                        <img src={icon} alt={alt} />
                    </Link>
                ))}
            </div>
        </header>
    );
}
