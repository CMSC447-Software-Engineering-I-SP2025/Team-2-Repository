// CategoryPage.jsx
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { CATEGORY_STRUCTURE } from './categoryData'; // import category data

const CategoryPage = () => {
    const { category, subcategory } = useParams();

    // Find the current category based on the URL
    const currentCategory = CATEGORY_STRUCTURE.find(cat => cat.key === category);

    if (!currentCategory) {
        return <p>Category not found.</p>;
    }

    // Determine which subcategories to display
    const subcategoriesToShow = subcategory
        ? [subcategory.replace(/-/g, ' ')] // If subcategory is selected, show only that one
        : currentCategory.links.slice(0, 3); // Otherwise, show the first three subcategories

    return (
        <div className="category-page">
            <div className="subcategories">
                {subcategoriesToShow.map(sub => (
                    <div key={sub} className="subcategory">
                        <h2>{sub}</h2>
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
