"use client";
import { makeParamsString } from "@/utils/general";
import { Form, Input, Checkbox, Button, Link } from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

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

    // Submit data to api endpoint
    fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginFormData),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.error) {
          console.error(res.error);
        } else {
          if (res.redirect_uri) {
            router.push(res.redirect_uri)
          }
        }
      })
      .catch((err) => console.error);
  };

  const handleRedirectRegister = (e) => {
    e.preventDefault(true);
    router.push("/register?"+makeParamsString(params));
  };

  return (
    <Form
      className="w-full justify-center items-center space-y-4"
      validationBehavior="native"
      validationErrors={errors}
      onSubmit={onSubmit}
    >
      <div className="flex flex-col gap-4 max-w-md">
        <Input
          isRequired
          errorMessage={({ validationDetails }) => {
            if (validationDetails.valueMissing) {
              return "Please enter your username";
            }
            return errors.name;
          }}
          label="Username"
          labelPlacement="outside"
          name="username"
          placeholder="Enter your username"
        />

        <Input
          isRequired
          label="Password"
          labelPlacement="outside"
          name="password"
          placeholder="Enter your password"
          type="password"
          value={password}
          onValueChange={setPassword}
        />

        
        <div className="flex gap-4">
          <Button className="w-full" color="primary" type="submit">
            Submit
          </Button>
          <Button type="reset" variant="bordered">
            Reset
          </Button>
        </div>
        <div className="flex justify-center align-items-center text-sm">
          <p className="flex items-center">
            Not a user? &nbsp;
            <Link className="text-small" href="/register" onClick={handleRedirectRegister}>
              Register here
            </Link>
          </p>
        </div>
      </div>
    </Form>
  );
}
