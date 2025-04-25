"use client"
import { useState } from "react";

export function MultiSelect({ options, value, onChange }) {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOption = (option) => {
        const newValue = value.includes(option)
            ? value.filter((v) => v !== option)
            : [...value, option];
        onChange(newValue);
    };

    const handleBlur = (e) => {
        // Check if the blur event is related to the dropdown
        if (!e.currentTarget.contains(e.relatedTarget)) {
            setIsOpen(false);
        }
    };

    return (
        <div className="relative" onBlur={handleBlur} tabIndex={-1}>
            <div
                className="border p-2 cursor-pointer bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                onClick={() => setIsOpen(!isOpen)}
            >
                {value.length > 0 ? value.join(", ") : "Select options"}
            </div>
            {isOpen && (
                <div className="absolute border bg-white dark:bg-gray-800 z-10">
                    {options.map((option) => (
                        <div
                            key={option}
                            className="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 cursor-pointer text-gray-900 dark:text-gray-100"
                            onClick={() => toggleOption(option)}
                        >
                            <input
                                type="checkbox"
                                checked={value.includes(option)}
                                readOnly
                                className="mr-2"
                            />
                            {option}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}