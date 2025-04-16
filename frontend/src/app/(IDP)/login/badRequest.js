import React from "react";
import { requiredParams } from "./page";

/**
 * BadRequest component to display required URL parameters.
 *
 * @returns {JSX.Element} A styled component listing required URL parameters.
 */
export default function BadRequest() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <div className="bg-white shadow-md rounded-lg p-6 max-w-md w-full">
                <h1 className="text-xl font-semibold mb-4 text-center text-gray-800">
                    Missing URL Parameters
                </h1>
                <p className="text-gray-600 mb-4 text-center">
                    This page requires the following URL parameters:
                </p>
                <ul className="list-disc list-inside text-gray-700">
                    {requiredParams.map((param, index) => (
                        <li key={index} className="text-sm">
                            {param}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}