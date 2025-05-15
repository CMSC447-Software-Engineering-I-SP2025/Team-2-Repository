import { Link } from "react-router-dom";
import { CATEGORY_STRUCTURE } from "./categoryData"; // mport the category data
import clsx from 'clsx'

export default function Header({ onLoginIconClick, isLoggedIn }) {
    const accountIconClass = clsx({"icon-not-logged-in": !isLoggedIn});
    return (
        <header className="header">
            {/* Logo and Name */}
            <div className="logo-container">
                <Link to="/">
                    <img src="/logo-with-name.svg" alt="Digital Cookbook Logo" />
                </Link>
            </div>

            <nav className="main-nav">
                {CATEGORY_STRUCTURE.map(({ name, links, basePath, key }) => (
                    <div className="nav-item" key={key}>
                        <Link to={basePath}>{name}</Link>
                        <div className="dropdown">
                            {links.map((link) => (
                                <Link
                                    to={`${basePath}/${link.toLowerCase().replace(/\s+/g, '-')}`}
                                    key={link}
                                >
                                    {link}
                                </Link>
                            ))}
                        </div>
                    </div>
                ))}
            </nav>

            {/* Log Ingredients Link */}
            
            <div className={"log-ingredients " + accountIconClass}>
                { isLoggedIn ?
                <Link to="/pantry">My Pantry</Link> :
                <button onClick={onLoginIconClick}>
                    My Pantry
                </button>
                }
            </div>

            {/* Icons for Search, Saved Recipes, and Account w/ Modal Trigger */}
            <div className="icon-group">
                
                <Link to="/search" className="search-icon ">
                    <img src="/search-icon.png" alt="Search" />
                </Link>
                
                {isLoggedIn ?
                    <Link to="/saved-recipes" className={"icon " + accountIconClass}>
                        <img src="/save-icon.png" alt="Saved Recipes" />
                    </Link> :
                    <button onClick={onLoginIconClick} className={"icon " + accountIconClass}>
                        <img src="/save-icon.png" alt="Saved Recipes"/>
                    </button>
                }                

                <button onClick={onLoginIconClick} className={"icon " + accountIconClass}>
                    <img src="/person-icon.svg" alt="Account" />
                </button>
            </div>
        </header>
    );
}
