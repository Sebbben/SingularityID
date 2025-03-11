"use client";
import { Card } from "@nextui-org/react";
import LoginForm from "./form";
import { useSearchParams } from "next/navigation";

export default function LoginPage() {

  const searchParams = useSearchParams();
  const params = Object.fromEntries(searchParams.entries());

  const requiredParams = ["response_type", "client_id", "redirect_uri", "state"];
  const hasAllRequiredParams = requiredParams.every(param => param in params);
  const hasOnlyRequiredParams = Object.keys(params).every(param => requiredParams.includes(param));

  if (!hasAllRequiredParams || !hasOnlyRequiredParams) {
    return <div>Bad request</div>;
  }

  return (
    <div className="flex items-center justify-center h-full">
      <Card className="p-8">
        <LoginForm params={params} />
      </Card>
    </div>
  );
}
