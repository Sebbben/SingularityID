"use client"
import { useRouter } from "next/navigation";

export const RedirectButton = (props) => {
    const router = useRouter();

    return (
        <button
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => router.push(props.url)}
        >
            {props.text}
        </button>
    );
};