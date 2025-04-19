"use client";
import { makeParamsString } from "@/utils/general";
import { CustomForm } from "@/components/CustomForm";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import API from "@/utils/api";

export default function LoginForm() {

  const params = useSearchParams();
  const formExtraParams = {}

  for (let key of ["response_type", "client_id", "redirect_uri", "state"]) {
    if (params.has(key)) formExtraParams[key] = params.get(key)
  }

  const fields = [
    {
      isRequired: true,
      label: "Username",
      name: "username",
      placeholder: "Enter your username",
      type: "text",
    },
    {
      isRequired: true,
      label: "Password",
      name: "password",
      placeholder: "Enter your password",
      type: "password",
    }
  ];

  return (
    <CustomForm
      fields={fields}
      url = "/api/auth/login"
      hiddenFormFields = {formExtraParams}
    />
  );
}
