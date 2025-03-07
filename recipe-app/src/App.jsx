import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import React from "react";
import ResultsDisplay from "./components/ResultsDisplay";

export default function App() {
    return <>
        <main>
            <Header />
            <GetRecipeSection />
            <ResultsDisplay />
        </main>
    </>;
}

