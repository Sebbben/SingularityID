"use client";

import { exchangeAuthCode } from "@/utils/actions";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect } from "react";

export default function authorize() {
    const params = useSearchParams();
    const router = useRouter();

    useEffect(() => {
        const code = params.get("code");
        if (code) {
            exchangeAuthCode(code); // Call the function inside useEffect
            router.push("/")
        }
    }, [params]); // Dependency array ensures this runs when params change

    return null; // Optionally, render a loading state or redirect
}