"use client";

import { exchangeAuthCode, test } from "@/utils/actions";
import { useSearchParams } from "next/navigation";
import { useEffect } from "react";

export default function authorize() {
    const params = useSearchParams();

    useEffect(() => {
        const code = params.get("code");
        if (code) {
            console.log(code)
            exchangeAuthCode(code); // Call the function inside useEffect
            // test()
        }
    }, [params]); // Dependency array ensures this runs when params change

    return null; // Optionally, render a loading state or redirect
}