"use client";
import { makeParamsString } from "@/utils/general";
import { CustomForm } from "@/components/CustomForm";
import { useRouter } from "next/navigation";
import { useState } from "react";
import API from "@/utils/api";

export default function LoginForm({params}) {
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const router = useRouter();

  const onSubmit = (e) => {
    e.preventDefault(true);
    const data = Object.fromEntries(new FormData(e.currentTarget));

    const loginFormData = {
      username: data.username,
      password: data.password,
      client_id: params.client_id,
      response_type: params.response_type,
      redirect_uri: params.redirect_uri,
      state: params.state
    };

    // Submit data to api endpoint using API utility
    API.POST("/api/auth/login", loginFormData, {}, 
      (res) => {
        if (res.redirect_uri) {
          router.push(res.redirect_uri);
        }
      },
      (status, error) => {
        console.error(error);
      }
    );
  };

  const handleRedirectRegister = (e) => {
    e.preventDefault(true);
    router.push("/register?"+makeParamsString(params));
  };

  const fields = [
    {
      isRequired: true,
      errorMessage: ({ validationDetails }) => {
        if (validationDetails.valueMissing) {
          return "Please enter your username";
        }
        return errors.name;
      },
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
      value: password,
      onValueChange: setPassword,
    }
  ];

  return (
    <CustomForm
      fields={fields}
      onSubmit={onSubmit}
      onReset={() => setPassword("")}
      submitButtonText="Submit"
      resetButtonText="Reset"
      linkText="Not a user? Register here"
      linkHref="/register"
      linkOnClick={handleRedirectRegister}
      errors={errors}
    />
  );
}
