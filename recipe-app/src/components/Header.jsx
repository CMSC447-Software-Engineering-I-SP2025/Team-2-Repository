export default function Header () {
    return <header>
        <div className="logo-container"><img src="/logo-with-name.svg" /></div>
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