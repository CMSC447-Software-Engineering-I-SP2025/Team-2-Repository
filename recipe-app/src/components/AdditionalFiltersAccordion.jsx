import clsx from 'clsx'
import {useState} from "react";

export function AdditionalFiltersAccordion ({constFilterLists, updateFilterBitMap}) {
    //true means block is invisible [cusineFilterIsInvisible, dietFilterIsInvisible, intolerancesFilterIsInvisible]
    const [invisibleBlocks, setInvisibleBlocks] = useState([true, true, true]);
    function toggleVisibility(pos) {
        const arrCopy = invisibleBlocks.slice();
        arrCopy[pos] = !arrCopy[pos];
        setInvisibleBlocks(arrCopy);
    }
    return <div className="additional-filters">
        {
            Array.from(constFilterLists).map((mapping, i) => 
            <AdditionalFilter invisible={invisibleBlocks[i]} toggleVisibility={() => toggleVisibility(i)}  filterType={mapping[0]} filterOptions={mapping[1]} updateFilterBitMap={updateFilterBitMap} key={mapping[0] + "-list"}/>)
        }
    </div>
}

function AdditionalFilter ({invisible, toggleVisibility, filterType, filterOptions, updateFilterBitMap}) {
    const cls = clsx('invisible-wrapper', {'invisible': invisible});
    return <div className="filter">
            <div className="filter-name" onClick={toggleVisibility}>
                <div>{filterType}</div> 
                <div>{invisible?<img src="angle-down-svgrepo-com.svg" alt="expand item icon"/>:<img src="angle-up-svgrepo-com.svg" alt="condense item icon"/>}</div>
            </div>
            <div className={cls}>
                <div className="invisible-block">
                    {filterOptions.map(option =>
                        <Checkbox optionName={option} key={option} filterType={filterType} updateFilterBitMap={updateFilterBitMap} />
                    )}
                </div>
            </div>
    </div>
}

function Checkbox({optionName, filterType, updateFilterBitMap}) {
    return <div className="filter-item">
        <input type="checkbox" id={optionName} name={optionName} onClick={() => updateFilterBitMap(filterType, optionName)}/>
        <label htmlFor={optionName}>{optionName}</label>
    </div>
}