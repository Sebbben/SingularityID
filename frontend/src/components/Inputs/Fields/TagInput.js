"use client"
import { useState } from "react";

export function TagInput({ value, onChange, placeholder = "Add a tag" }) {
    const [inputValue, setInputValue] = useState("");

    const addTag = () => {
        if (inputValue.trim() && !value.includes(inputValue.trim())) {
            onChange([...value, inputValue.trim()]);
            setInputValue("");
        }
    };

    const removeTag = (tag) => {
        onChange(value.filter((v) => v !== tag));
    };

    return (
        <div className="border p-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
            <div className="flex flex-wrap gap-2">
                {value.map((tag) => (
                    <div
                        key={tag}
                        className="bg-gray-200 dark:bg-gray-600 p-1 rounded flex items-center text-gray-900 dark:text-gray-100"
                    >
                        {tag}
                        <button
                            className="ml-2 text-red-500 dark:text-red-400"
                            onClick={() => removeTag(tag)}
                        >
                            x
                        </button>
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addTag()}
                placeholder={placeholder}
                className="mt-2 w-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600 rounded-md"
            />
        </div>
    );
}

