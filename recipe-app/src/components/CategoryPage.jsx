// CategoryPage.jsx
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { CATEGORY_STRUCTURE } from './categoryData'; // import category data

const normalize = (str) => 
    str.toLowerCase().replace(/\s+/g, '-'); // "Under 30 Mins" → "under-30-mins"

const CategoryPage = () => {
    const { category, subcategory } = useParams();

    const currentCategory = CATEGORY_STRUCTURE.find(cat => cat.key === category);

    if (!currentCategory) {
        return <p>Category not found.</p>;
    }

    // If subcategory selected, find its display name
    let subcategoriesToShow;
    if (subcategory) {
        const matchedSubcategory = currentCategory.links.find(link => normalize(link) === subcategory);
        if (!matchedSubcategory) {
            return <p>Subcategory not found.</p>;
        }
        subcategoriesToShow = [matchedSubcategory];
    } else {
        subcategoriesToShow = currentCategory.links.slice(0, 4);
    }

    return (
        <div className="category-page">
            <div className="subcategories">
                {subcategoriesToShow.map(sub => (
                    <div key={sub} className="subcategory">
                        <h2>{sub}</h2> {/* Now using the correct display name */}
                        <div className="recipes">
                            {/* Replace with dynamic recipe fetching */}
                            <p>Recipe 1 for {sub}</p>
                            <p>Recipe 2 for {sub}</p>
                            <p>Recipe 3 for {sub}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CategoryPage;
